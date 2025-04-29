# menuTitle: Steal Metrics

import ezui
import os
from mojo.roboFont import OpenFont
from mojo.UI import Message

class StealMetricsController(ezui.WindowController):
    
    def build(self):
            
        content = """
        * Box
        > Source Font: 
        > (Select Source) @selectSourceButton
        > [Path: None] @sourceFileLabel
        
        * Box
        > Target Font: 
        > (Select Target) @selectTargetButton
        > [Path: None] @targetFileLabel
        
        * HorizontalStack @buttonStack
        > (Cancel) @cancelButton
        > (Apply) @applyButton
        
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
        print("Select Source Button Callback Clicked")
#        self.showGetFile(
#            messageText="Select a source .ufo File",
#            allowsMultipleSelection=False,
#            directory=None,
#            callback=self.selectSourceResultCallback
#        )

    def selectSourceResultCallback(self, result):
        print("Source File Selected")
        if result:
            self.sourceFile = result[0]
            
            max_length = 40  # Adjust this value to fit your window size
            if len(self.sourceFile) > max_length:
                truncated_path = f"...{self.sourceFile[-(max_length - 3):]}"
            else:
                truncated_path = self.sourceFile
            
            self.w.getItem("sourceFileLabel").set(f"Folder Path: {truncated_path}")
        else:
            Message("No file selected", informativeText="Please select a file to proceed.")

    def selectTargetButtonCallback(self, sender):
        self.showGetFile(
            messageText="Select a target .ufo File",
            allowsMultipleSelection=False,
            directory=None,
            callback=self.selectTargetResultCallback
        )

    def selectTargetResultCallback(self, result):
        if result:
            self.targetFile = result[0]
            
            max_length = 40  # Adjust this value to fit your window size
            if len(self.targetFile) > max_length:
                truncated_path = f"...{self.targetFile[-(max_length - 3):]}"
            else:
                truncated_path = self.targetFile
            
            self.w.getItem("targetFileLabel").set(f"Folder Path: {truncated_path}")
        else:
            Message("No file selected", informativeText="Please select a file to proceed.")

    def cancelButtonCallback(self, sender):
        self.w.close()

    def applyButtonCallback(self, sender):
        if not self.sourceFile or not self.targetFile:
                Message("Error", informativeText="Please select both source and target fonts.")
                return
        self.stealMetrics()

    def stealMetrics(self):
        sourceFont = OpenFont(self.sourceFile, showInterface=False)
        targetFont = OpenFont(self.targetFile, showInterface=False)
        metrics = ['leftMargin', 'rightMargin']

        for glyphName in sourceFont.keys():
            if glyphName in targetFont:
                sourceGlyph = sourceFont[glyphName]
                targetGlyph = targetFont[glyphName]
                for metric in metrics:
                    value = getattr(sourceGlyph, metric, 0)
                    if value is None:
                        value = 0
                    setattr(targetGlyph, metric, value)

        targetFont.changed()
        Message("Success", informativeText="Metrics stolen successfully!")

StealMetricsController()
