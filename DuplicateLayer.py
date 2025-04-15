font = CurrentFont()
g = CurrentGlyph()

if g:
    currentLayer = g.layer  # Get the layer of the current glyph
    layerName = currentLayer.name  # Extract the name of the layer
else:
    # If no glyph is selected, fallback to the default layer
    if "foreground" in font.layers:
        currentLayer = font.layers["foreground"]
    else:
        currentLayer = font.layers[0]  # Fallback to the first layer
    
    layerName = currentLayer.name  # Extract the name of the default layer

# Create a new layer name for duplication
newLayerName = f"{layerName} copy"

# Duplicate the current layer
font.duplicateLayer(layerName, newLayerName)

print(f"Duplicated layer '{layerName}' as '{newLayerName}'.")