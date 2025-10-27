# menuTitle: Adjust/Set Metrics

import ezui
import re
from mojo.UI import CurrentFontWindow, Message

class MetricsAdjusterWindow(ezui.WindowController):

    def build(self):
        self.f = CurrentFont()
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
                
        * HorizontalStack     @buttonStack
        > (Cancel)            @cancelButton
        > (Apply)             @applyButton
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
            buttonStack = dict(
                width = "fill",
                ),
            cancelButton = dict(
                width = button_width,
                ),
            applyButton = dict(
                width = button_width,

            )
        )
        
        self.w = ezui.EZWindow(
            content = content,
            descriptionData = descriptionData,
            size = ("auto", "auto"),
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
        # self.cancelButton.bind(chr(27), [])
        self.w.setDefaultButton(self.applyButton)

    def started(self):
        self.w.open()

    def destroy(self):
        pass

    def cancelButtonCallback(self, sender):
        self.w.close()

    def applyButtonCallback(self, sender):
        operation = self.operation.get()
        equalMargins = self.equalMargins.get()
    
        if equalMargins == 1:
            combMarginValue = self.combMarginField.get()
            leftMarginValue = rightMarginValue = combMarginValue
        else:
            leftMarginValue = self.marginLeftField.get()
            rightMarginValue = self.marginRightField.get()
    
        selectedGlyphs = self.f.selectedGlyphNames
        if not selectedGlyphs:
            selectedGlyphs = self.f.keys()
    
        if operation == 0:
            self.adjustMetrics(selectedGlyphs, leftMarginValue, rightMarginValue)
        elif operation == 1:
            self.setMetrics(selectedGlyphs, leftMarginValue, rightMarginValue)
    
        self.f.changed()
        
    def parse_margin_input(self, input_value, original_value):
        """
        Parses the input value and returns the new margin value based on the original value.
        Supports:
        - Absolute values (e.g., 50)
        - Relative values (e.g., +5, -10)
        - Percentages (e.g., 90%, -10%, +5%)
        """
        if isinstance(input_value, str):
            input_value = input_value.strip()
            if "%" in input_value:
                match = re.match(r"^([+-]?)(\d+(\.\d+)?)%$", input_value)
                if not match:
                    raise ValueError("Invalid percentage format")
                sign, number, _ = match.groups()
                percent = float(number) / 100.0
                if sign == "":
                    return int(round(original_value * percent))
                elif sign == "-":
                    return int(round(original_value * (1 - percent)))
                elif sign == "+":
                    return int(round(original_value * (1 + percent)))
            else:
                match = re.match(r"^([+-])(\d+)$", input_value)
                if match:
                    sign, number = match.groups()
                    delta = int(number)
                    if sign == "+":
                        return original_value + delta
                    else:
                        return original_value - delta
                # Absolute value
                return int(input_value) if input_value else 0
        else:
            return int(input_value) if input_value else 0

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
        if equalMargins == 0:  # Show seperate Margins Field
            self.marginStack.show(True)
            self.combMarginStack.show(False)
        elif equalMargins == 1:  # Show combined Margins Field
            self.marginStack.show(False)
            self.combMarginStack.show(True)

MetricsAdjusterWindow()
