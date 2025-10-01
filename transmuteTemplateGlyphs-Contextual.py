from mojo.subscriber import Subscriber, registerFontOverviewSubscriber

class TransmuteTemplateGlyphs(Subscriber):

    def fontOverviewWantsContextualMenuItems (self, info):
        self.f = CurrentFont()
		
        if self.f is None:
            return
        if not self.f.templateSelectedGlyphNames:
            return

        if len(self.f.templateSelectedGlyphNames) > 1:
            message = "Transmute TemplateGlyphs"
        else:
            message = "Transmute TemplateGlyph"
        
        myMenuItems = [
            (message, self.turnTemplateGlyphsToGlyphs)
        ]

        info['itemDescriptions'].extend(myMenuItems)

    def turnTemplateGlyphsToGlyphs(self, sender):

        for g in self.f.templateSelectedGlyphNames:
            g = self.f[g]
            g.changed()
			
if __name__ == "__main__":    
    registerFontOverviewSubscriber(TransmuteTemplateGlyphs)