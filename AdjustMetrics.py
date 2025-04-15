# Get the current font
font = CurrentFont()
if font is None:
    print("No font open.")
else:
    # Define the scaling factor
    adjustingFactor = 5  # Change this to any desired factor

    # List of metrics to modify (excluding width)
    metrics = ['leftMargin', 'rightMargin']

    # Iterate over all glyphs in the font
    for glyph in font:
        for metric in metrics:
            value = getattr(glyph, metric, 0)
            if value is not None:
                setattr(glyph, metric, value + adjustingFactor)

    # Update the font
    font.changed()