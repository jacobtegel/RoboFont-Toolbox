import ezui
from mojo.subscriber import Subscriber, registerRoboFontSubscriber
from mojo.UI import CurrentFontWindow, Message


class DuplicateGlyphsWindow(ezui.WindowController):

    def build(self, parent):
        window = parent.w
        self.f = CurrentFont()
        self.glyphs_to_copy = self.f.selectedGlyphNames

        content = """
        (X) Duplicate with Suffix          @operationRadios
        ( ) Duplicate with New Name
        
        ---
        
        . [_ _]                            @suffixTextField
        
        * HorizontalStack                  @newNameStack
        > [_ _]                            @newNameTextField

        ---
        
        [X] Overwrite Existing Glyphs      @overwriteCheckbox

        ======================
        
        (Cancel)                           @cancelButton
        (Apply)                            @applyButton
        """
        entry_width = 200
        button_width = (entry_width - 10) / 2
        descriptionData = dict(
            suffixTextField=dict(
                width=entry_width,
                placeholder="Enter suffix (e.g., 'alt')",
            ),
            newNameStack=dict(
                width=entry_width,
            ),
            newNameTextField=dict(
                width=(entry_width - 32),
                placeholder="Enter new name",
            ),
            overwriteCheckbox=dict(
                sizeStyle="small",
            ),
            cancelButton=dict(
                width=button_width,
            ),
            applyButton=dict(
                width=button_width,
            )
        )
        self.w = ezui.EZSheet(
            content=content,
            descriptionData=descriptionData,
            size="auto",
            parent=window,
            controller=self
        )
        self.operation = self.w.getItem("operationRadios")
        self.suffix_field = self.w.getItem("suffixTextField")
        self.new_name_field = self.w.getItem("newNameTextField")
        self.new_name_stack = self.w.getItem("newNameStack")
        self.overwrite = self.w.getItem("overwriteCheckbox")
        self.apply_button = self.w.getItem("applyButton")
        self.cancel_button = self.w.getItem("cancelButton")
        self.cancel_button.bind(chr(27), [])
        self.w.setDefaultButton(self.apply_button)
        
        self.update_field_options()

    def started(self):
        if not self.glyphs_to_copy:
            Message("No Glyphs Selected", informativeText="Please select at least one glyph.")
            return
        self.w.open()

    def destroy(self):
        pass

    def cancelButtonCallback(self, sender):
        self.w.close()

    def applyButtonCallback(self, sender):
        operation = self.operation.get()
        if operation == 0:  # Duplicate with Suffix
            suffix = self.suffix_field.get()
            if not suffix:
                Message("Missing Suffix", informativeText="Please provide a suffix for duplication.")
                return
            self.duplicate_with_suffix(suffix)
        elif operation == 1:  # Duplicate with New Name
            new_name = self.new_name_field.get()
            if not new_name:
                Message("Missing New Name", informativeText="Please provide a new name for duplication.")
                return
            self.duplicate_with_new_name(new_name)
        
        self.w.close()

    def duplicate_with_suffix(self, suffix):
        for glyph_name in self.glyphs_to_copy:
            base_name = glyph_name.split('.')[0]
            new_glyph_name = f"{base_name}.{suffix}"
            if new_glyph_name in self.f.glyphOrder and not self.overwrite.get():
                Message("Error", informativeText=f"Glyph '{new_glyph_name}' already exists. Enable overwrite to proceed.")
                continue
            self.f.insertGlyph(self.f[glyph_name], new_glyph_name)
            self.f[new_glyph_name].unicode = None
            print(f"Created {new_glyph_name}.")

        self.f.update()

    def duplicate_with_new_name(self, new_name):
        if len(self.glyphs_to_copy) > 1:
            Message("Error", informativeText="Please select only one glyph for this operation.")
            return
        
        glyph_name = self.glyphs_to_copy[0]
        if new_name in self.f.glyphOrder and not self.overwrite.get():
            Message("Error", informativeText=f"Glyph '{new_name}' already exists. Enable overwrite to proceed.")
            return
        self.f.insertGlyph(self.f[glyph_name], new_name)
        self.f[new_name].unicode = None
        print(f"Created {new_name}.")
        
        self.f.update()

    def operationRadiosCallback(self, sender):
        self.update_field_options()

    def update_field_options(self):
        operation = self.operation.get()
        if operation == 0:  # Duplicate with Suffix
            self.suffix_field.show(True)
            self.new_name_stack.show(False)
        elif operation == 1:  # Duplicate with New Name
            self.suffix_field.show(False)
            self.new_name_stack.show(True)


class CustomFontOverviewContextualMenu(Subscriber):

    debug = True

    def fontOverviewWantsContextualMenuItems(self, info):
        if not CurrentFont().selectedGlyphNames:
            return

        message = "Duplicate Glyphs..."
        my_menu_items = [
            (message, self.openDuplicateWindow)
        ]
        info['itemDescriptions'].extend(my_menu_items)

    def openDuplicateWindow(self, sender):
        parent = CurrentFontWindow()
        DuplicateGlyphsWindow(parent)


if __name__ == '__main__':
    registerRoboFontSubscriber(CustomFontOverviewContextualMenu)