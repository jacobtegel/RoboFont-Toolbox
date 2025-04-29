# menuTitle: Set Metrics in Layer

font = CurrentFont()
if font is None:
    print("No font open.")
else:
    # Define the metric value to set
    setMetrics = 50  # Change this to any desired value

    # Define the target layer
    layerName = "background"  # Change this to the desired layer name

    # List of metrics to modify (excluding width)
    metrics = ['leftMargin', 'rightMargin']

    # Find the target layer
    layer = None
    for l in font.layers:
        if l.name == layerName:
            layer = l
            break

    if layer is None:
        print(f"Layer '{layerName}' not found.")
    else:
        # Get selected glyphs, default to all if none are selected
        selectedGlyphs = font.selectedGlyphNames if font.selectedGlyphNames else layer.keys()

        # Flag to track changes
        changed = False

        # Iterate over selected glyphs in the layer
        for glyphName in selectedGlyphs:
            if glyphName in layer:
                glyph = layer[glyphName]  # Get glyph from the specific layer
                for metric in metrics:
                    if hasattr(glyph, metric):  # Ensure the metric exists
                        setattr(glyph, metric, setMetrics)
                        changed = True

        # Update the font if any changes were made
        if changed:
            font.changed()