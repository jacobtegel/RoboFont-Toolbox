# menuTitle: Adjust/Set Metrics

import ezui
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
                valueType="integer",
                valueFallback = "0"
                ),
            marginRightField = dict(
                placeholder = "Right",
                valueWidth = 75,
                valueType = "integer",
                valueFallback = "0"
                ),
            combMarginStack = dict(
                width = entry_width,
                height = "fill"
                ),
            combMarginField = dict(
                placeholder = "Left & Right",
                valueType = "integer",
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

        # Check if Equal Margins is enabled
        if equalMargins == 1:
            # Use combined margin value for both left and right
            combMarginValue = self.combMarginField.get()  # Correctly access combMarginField
            try:
                combMarginValue = int(combMarginValue) if combMarginValue else 0
            except ValueError:
                Message("Invalid Input", informativeText="Please enter a valid number for the combined margins.")
                return
            leftMarginValue = rightMarginValue = combMarginValue
        else:
            # Use separate margin values
            leftMarginValue = self.marginLeftField.get()
            rightMarginValue = self.marginRightField.get()

            try:
                leftMarginValue = int(leftMarginValue) if leftMarginValue else 0
                rightMarginValue = int(rightMarginValue) if rightMarginValue else 0
            except ValueError:
                Message("Invalid Input", informativeText="Please enter valid numbers for the margins.")
                return

        # Get selected glyphs or use all glyphs if none selected
        selectedGlyphs = self.f.selectedGlyphNames
        if not selectedGlyphs:
            selectedGlyphs = self.f.keys()

        if operation == 0:  # Adjust Metrics by Value
            self.adjustMetrics(selectedGlyphs, leftMarginValue, rightMarginValue)
        elif operation == 1:  # Set Metrics to Value
            self.setMetrics(selectedGlyphs, leftMarginValue, rightMarginValue)

        # Update the font
        self.f.changed()
        # self.w.close()

    def adjustMetrics(self, glyphNames, leftAdjust, rightAdjust):
        for glyphName in glyphNames:
            glyph = self.f[glyphName]
            
            if leftAdjust != 0:
                currentLeftMargin = glyph.leftMargin
                glyph.leftMargin = currentLeftMargin + leftAdjust
            
            if rightAdjust != 0:
                currentRightMargin = glyph.rightMargin
                glyph.rightMargin = currentRightMargin + rightAdjust
        
        print(f"Adjusted margins for {len(glyphNames)} glyphs.")

    def setMetrics(self, glyphNames, leftValue, rightValue):
        changed = False
        
        for glyphName in glyphNames:
            glyph = self.f[glyphName]
            
            if leftValue != 0:
                glyph.leftMargin = leftValue
                changed = True
            
            if rightValue != 0:
                glyph.rightMargin = rightValue
                changed = True
        
        if changed:
            print(f"Set margins for {len(glyphNames)} glyphs.")
    
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