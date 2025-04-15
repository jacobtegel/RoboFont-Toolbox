# Get the current font
font = CurrentFont()
if font is None:
    print("No font open.")
else:
    # Define the metric value to set
    setMetrics = 25  # Change this to any desired value

    # List of metrics to modify (excluding width)
    metrics = ['leftMargin', 'rightMargin']

    # Flag to track changes
    changed = False

    # Iterate over all glyphs in the font
    for glyph in font:
        for metric in metrics:
            if hasattr(glyph, metric):  # Ensure the metric exists
                setattr(glyph, metric, setMetrics)
                changed = True

    # Update the font if any changes were made
    if changed:
        font.changed()