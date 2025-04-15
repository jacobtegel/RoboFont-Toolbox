# Get source and target fonts by style name
sourceFont = AllFonts().getFontsByStyleName('Text')[0]
targetFont = AllFonts().getFontsByStyleName('Display')[0]

# Open source and target fonts from UFO files
# sourceFont = OpenFont("path/to/source.ufo", showInterface=False)
# targetFont = OpenFont("path/to/target.ufo", showInterface=False)

# List of glyph metrics to copy
metrics = ['leftMargin', 'rightMargin']

# Iterate over glyphs in the source font
for glyphName in sourceFont.keys():
    if glyphName in targetFont:
        sourceGlyph = sourceFont[glyphName]
        targetGlyph = targetFont[glyphName]
        
        # Copy metrics, ensuring no None values
        for metric in metrics:
            value = getattr(sourceGlyph, metric, 0)
            if value is None:
                value = 0  # Default to 0 if None
            setattr(targetGlyph, metric, value)

# Update target font
targetFont.changed()