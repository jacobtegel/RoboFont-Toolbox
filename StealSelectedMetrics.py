# menuTitle: Steal Selected Metrics

import ezui
import os
from mojo.roboFont import OpenFont
from mojo.UI import Message

class StealMetricsController(ezui.WindowController):
    
    def build(self):
            
        content = """
        Steal From: 
        (Select Source) @selectSourceButton
        [Path: None] @sourceFileLabel
        
        ---
        
        (X) Complete Characterset @operationRadios
        ( ) Selected Characters
        
        ===
        (Cancel) @cancelButton
        (Apply) @applyButton
        
        """
        
        entry_width = 200
        button_width = (entry_width - 10) / 2
        descriptionData = dict(
            selectSourceButton =dict(
                text = "Select Source",
                width=button_width,
            ),
            sourceFileLabel = dict(
                sizeStyle="small",
            ),
            selectTargetButton = dict(
                text = "Select Target",
                width=button_width,
            ),
            targetFileLabel = dict(
                sizeStyle="small",
            ),
            buttonStack=dict(
                width=entry_width,
            ),
            cancelButton= dict(
                width=button_width,
            ),
            applyButton= dict(
                width=button_width,
            ),
        )
        self.w = ezui.EZWindow(
            content = content,
            descriptionData = descriptionData,
            size = "auto",
            controller = self
        )
        
        self.sourceFile = None
        self.targetFile = None

    def started(self):
        self.w.open()

    def selectSourceButtonCallback(self, sender):
        self.showGetFile(
            messageText="Select a source .ufo File",
            allowsMultipleSelection=False,
            directory=None,
            callback=self.selectSourceResultCallback
        )

    def selectSourceResultCallback(self, result):
        print("Source File Selected")
        if result:
            self.sourceFile = result[0]
            
            max_length = 27  # Adjust this value to fit your window size
            if len(self.sourceFile) > max_length:
                truncated_path = f"...{self.sourceFile[-(max_length - 3):]}"
            else:
                truncated_path = self.sourceFile
            
            self.w.getItem("sourceFileLabel").set(f"Folder Path: {truncated_path}")
        else:
            Message("No file selected", informativeText="Please select a file to proceed.")

    def cancelButtonCallback(self, sender):
        self.w.close()

    def applyButtonCallback(self, sender):
        if not self.sourceFile:
                Message("Error", informativeText="Please select a source font.")
                return
        self.stealMetrics()

    def stealMetrics(self):
        sourceFont = OpenFont(self.sourceFile, showInterface=False)
        targetFont = CurrentFont()
        if not targetFont:
            Message("No font open", informativeText="Please open a target font in RoboFont.")
            return
        
        operation = self.w.getItem("operationRadios").get()
        if operation == 0:  # Complete Characterset
            glyphNames = [gn for gn in sourceFont.keys() if gn in targetFont]
        else:  # Selected Characters
            glyphNames = [gn for gn in targetFont.selectedGlyphNames if gn in sourceFont]
        
        metrics = ['leftMargin', 'rightMargin']

        for glyphName in glyphNames:
            sourceGlyph = sourceFont[glyphName]
            targetGlyph = targetFont[glyphName]
            with targetGlyph.undo("Steal Metrics"):
                for metric in metrics:
                    value = getattr(sourceGlyph, metric, 0)
                    if value is None:
                        value = 0
                    setattr(targetGlyph, metric, value)

        targetFont.changed()
        Message("Success", informativeText="Metrics stolen successfully!")

StealMetricsController()
