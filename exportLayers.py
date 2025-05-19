# menuTitle: Export Layers

import os
import ezui
from mojo.roboFont import CurrentFont, NewFont
from mojo.UI import Message

class ExportLayersController(ezui.WindowController):

    def build(self):
        content = """
        (select Folder) @selectFolderButton
        [Folder Path: None] @folderPathLabel

        ---

        [ ] Copy kerning and features @copyKerningCheckBox

        ---
        ===
        
        (Cancel) @cancelButton
        (Export) @exportButton
        """

        descriptionData = dict(
            selectFolderButton=dict(
                width=260,
            ),
            folderPathLabel=dict(
            ),
            copyKerningCheckBox=dict(
            ),
            cancelButton=dict(
                width=120,
            ),
            exportButton=dict(
                width=120,
            ),
        )

        self.w = ezui.EZWindow(
            title="Export Layers",
            content=content,
            descriptionData=descriptionData,
            size="auto",
            controller=self
        )
        
        self.w.setDefaultButton(self.w.getItem("exportButton"))
        self.exportFolder = None

    def started(self):
        self.w.open()

    def selectFolderButtonCallback(self, sender):
        self.showGetFolder(
            messageText="Choose export destination folder.",
            allowsMultipleSelection=False,
            directory=None,
            callback=self.selectFolderResultCallback
        )

    def selectFolderResultCallback(self, result):
        if result:
            self.exportFolder = result[0]
            
            max_length = 30
            if len(self.exportFolder) > max_length:
                truncated_path = f"...{self.exportFolder[-(max_length - 3):]}"
            else:
                truncated_path = self.exportFolder
            
            self.w.getItem("folderPathLabel").set(f"Folder Path: {truncated_path}")
        else:
            self.w.getItem("folderPathLabel").set("[No folder selected]")

    def exportButtonCallback(self, sender):
        font = CurrentFont()
        if not font:
            Message("No font open.", informativeText="Please open a font.")
            return
        exportPath = self.exportFolder or os.path.dirname(font.path)
        baseName = os.path.splitext(os.path.basename(font.path))[0]
        copyKerning = self.w.getItem("copyKerningCheckBox").get()
        exported = []
        for layerName in font.layerOrder:
            if layerName in ("foreground", "background"):
                continue
            idx = font.layerOrder.index(layerName)
            sourceLayer = font.layers[idx]
            newFont = NewFont(showInterface=False)
            for glyph in sourceLayer:
                newGlyph = newFont.newGlyph(glyph.name)
                newGlyph.appendGlyph(glyph)
                newGlyph.width = glyph.width
                newGlyph.unicodes = list(glyph.unicodes)
            for attr in [
                "familyName", "styleName", "ascender", "descender", "unitsPerEm",
                "xHeight", "capHeight", "italicAngle", "openTypeOS2WeightClass",
                "openTypeOS2WidthClass", "openTypeOS2VendorID"
            ]:
                if hasattr(font.info, attr):
                    setattr(newFont.info, attr, getattr(font.info, attr))
            newFont.info.styleName = f"{font.info.styleName} {layerName}"
            if copyKerning:
                newFont.kerning.update(font.kerning)
                newFont.features.text = font.features.text
            otfName = f"{baseName}-{font.info.familyName}-{font.info.styleName}-{layerName}.otf"
            otfPath = os.path.join(exportPath, otfName)
            newFont.generate(path=otfPath, format='otf', decompose=True, checkOutlines=True)
            newFont.close()
            if os.path.exists(otfPath):
                exported.append(f"File {otfName} successfully exported at {otfPath}")
            else:
                exported.append(f"Failed to export {otfName} at {otfPath}")
        Message("Export complete.", informativeText="\n\n".join(exported))

    def cancelButtonCallback(self, sender):
        self.w.close()

ExportLayersController()
