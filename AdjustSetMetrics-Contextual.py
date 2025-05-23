# Adjust/Set Metrics Contextual with percentage support

import ezui
import re
from mojo.subscriber import Subscriber, registerFontOverviewSubscriber
from mojo.UI import CurrentFontWindow, Message

class MetricsAdjuster(ezui.WindowController):

    def build(self, parent):
        window = parent.w
        self.f = RFont(parent._font)
        if not self.f:
            Message("No font open", informativeText="Please open a font first.")
            return
        
        content = """
        (X) Adjust Metrics by Value         @operationRadios
        ( ) Set Metrics to Value
        
        * Box @box
        > Margins
        > * HorizontalStack   @marginStack
        > > [_ _]             @marginLeftField
        > > [_ _]             @marginRightField
        
        > * HorizontalStack   @combMarginStack
        > > [_ _]             @combMarginField
        
        > [ ] Left /= Right   @equalMarginsCheckbox
                
        ===
        
        (Cancel)            @cancelButton
        (Apply)             @applyButton
        """
        
        entry_width = 200
        button_width = (entry_width - 10) / 2
            
        descriptionData = dict(
            box = dict (
                width = entry_width
                ),
            marginStack = dict (
                width = "fill",
                height = "fill"
                ),
            marginLeftField = dict(
                placeholder="Left",
                valueWidth = 75,
                valueFallback = "0"
                ),
            marginRightField = dict(
                placeholder = "Right",
                valueWidth = 75,
                valueFallback = "0"
                ),
            combMarginStack = dict(
                width = entry_width,
                height = "fill"
                ),
            combMarginField = dict(
                placeholder = "Left & Right",
                valueFallback = "0"
                ),
            equalMarginsCheckbox = dict(
                value = 0,
                ),
            cancelButton = dict(
                width = button_width,
                ),
            applyButton = dict(
                width = button_width,
            )
        )
        
        self.w = ezui.EZSheet(
            content = content,
            descriptionData = descriptionData,
            size = ("auto", "auto"),
            parent = window,
            controller = self
        )
        
        self.operation = self.w.getItem("operationRadios")
        self.marginLeftField = self.w.getItem("marginLeftField")
        self.marginRightField = self.w.getItem("marginRightField")
        self.marginStack = self.w.getItem("marginStack")
        self.combMarginStack = self.w.getItem("combMarginStack")
        self.combMarginField = self.w.getItem("combMarginField")
        self.applyButton = self.w.getItem("applyButton")
        self.cancelButton = self.w.getItem("cancelButton")
        self.equalMargins = self.w.getItem("equalMarginsCheckbox")
        
        self.update_field_options()
        self.w.setDefaultButton(self.applyButton)

    def started(self):
        self.w.open()

    def destroy(self):
        pass

    def cancelButtonCallback(self, sender):
        self.w.close()

    def parse_margin_input(self, input_value, original_value):
        """
        Parses the input value and returns the new margin value based on the original value.
        Supports:
        - Absolute values (e.g., 50)
        - Percentages (e.g., 90%, -10%, +5%)
        """
        if isinstance(input_value, str) and "%" in input_value:
            match = re.match(r"^([+-]?)(\d+(\.\d+)?)%$", input_value.strip())
            if not match:
                raise ValueError("Invalid percentage format")
            sign, number, _ = match.groups()
            percent = float(number) / 100.0
            if sign == "":
                # e.g., 90%: set to 90% of original
                return int(round(original_value * percent))
            elif sign == "-":
                # e.g., -10%: subtract 10% of original
                return int(round(original_value * (1 - percent)))
            elif sign == "+":
                # e.g., +5%: add 5% of original
                return int(round(original_value * (1 + percent)))
        else:
            # Absolute value
            return int(input_value) if input_value else 0

    def applyButtonCallback(self, sender):
        operation = self.operation.get()
        equalMargins = self.equalMargins.get()

        # Check if Equal Margins is enabled
        if equalMargins == 1:
            combMarginValue = self.combMarginField.get()
            leftMarginValue = rightMarginValue = combMarginValue
        else:
            leftMarginValue = self.marginLeftField.get()
            rightMarginValue = self.marginRightField.get()

        selectedGlyphs = self.f.selectedGlyphNames
        if not selectedGlyphs:
            selectedGlyphs = self.f.keys()

        if operation == 0:  # Adjust Metrics by Value
            self.adjustMetrics(selectedGlyphs, leftMarginValue, rightMarginValue)
        elif operation == 1:  # Set Metrics to Value
            self.setMetrics(selectedGlyphs, leftMarginValue, rightMarginValue)

        self.f.changed()
        self.w.close()

    def adjustMetrics(self, glyphNames, leftAdjust, rightAdjust):
        for glyphName in glyphNames:
            glyph = self.f[glyphName]
            with glyph.undo("Adjust Margins"):
                if leftAdjust:
                    currentLeftMargin = glyph.leftMargin
                    try:
                        newLeft = self.parse_margin_input(leftAdjust, currentLeftMargin)
                    except Exception as e:
                        Message("Invalid Input", informativeText=str(e))
                        return
                    glyph.leftMargin = newLeft
                if rightAdjust:
                    currentRightMargin = glyph.rightMargin
                    try:
                        newRight = self.parse_margin_input(rightAdjust, currentRightMargin)
                    except Exception as e:
                        Message("Invalid Input", informativeText=str(e))
                        return
                    glyph.rightMargin = newRight

    def setMetrics(self, glyphNames, leftValue, rightValue):
        for glyphName in glyphNames:
            glyph = self.f[glyphName]
            with glyph.undo("Set Margins"):
                if leftValue:
                    try:
                        newLeft = self.parse_margin_input(leftValue, glyph.leftMargin)
                    except Exception as e:
                        Message("Invalid Input", informativeText=str(e))
                        return
                    glyph.leftMargin = newLeft
                if rightValue:
                    try:
                        newRight = self.parse_margin_input(rightValue, glyph.rightMargin)
                    except Exception as e:
                        Message("Invalid Input", informativeText=str(e))
                        return
                    glyph.rightMargin = newRight

    def equalMarginsCheckboxCallback(self, sender):
        self.update_field_options()

    def update_field_options(self):
        equalMargins = self.equalMargins.get()
        if equalMargins == 0:
            self.marginStack.show(True)
            self.combMarginStack.show(False)
        elif equalMargins == 1:
            self.marginStack.show(False)
            self.combMarginStack.show(True)

class MetricsAdjusterWindow(Subscriber):

    def fontOverviewWantsContextualMenuItems(self, info):
        self.f = CurrentFont()
        self.fo = info['fontOverview']
        
        if not CurrentFont().selectedGlyphNames:
            return

        message = "Adjust / Set Metrics"
        my_menu_items = [
            (message, self.openAdjustSetMetricsWindow)
        ]
        info['itemDescriptions'].extend(my_menu_items)

    def openAdjustSetMetricsWindow(self, sender):
        parent = CurrentFontWindow()
        MetricsAdjuster(parent)

if __name__ == '__main__':
    registerFontOverviewSubscriber(MetricsAdjusterWindow)
