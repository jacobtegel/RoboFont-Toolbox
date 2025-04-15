# Get the current font
font = CurrentFont()
if font is None:
    print("No font open.")
else:
    # Define the scaling factor
    adjustingFactor = 10  # Change this to any desired factor

    # List of metrics to modify (excluding width)
    metrics = ['leftMargin', 'rightMargin']

    # Get selected glyphs, default to all if none are selected
    selectedGlyphs = font.selectedGlyphNames if font.selectedGlyphNames else layer.keys()

    # Iterate over all glyphs in the font
    for glyphName in selectedGlyphs:
        glyph = font[glyphName]
        for metric in metrics:
            value = getattr(glyph, metric, 0)
            if value is not None:
                setattr(glyph, metric, value + adjustingFactor)

    # Update the font
    font.changed()