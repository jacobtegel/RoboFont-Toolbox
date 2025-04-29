# menuTitle: Duplicate Layer

font = CurrentFont()
g = CurrentGlyph()

if g:
    currentLayer = g.layer  # Get the layer of the current glyph
    layerName = currentLayer.name  # Extract the name of the layer

elif font and font.selectedLayerNames:  # Check if layers are selected in the font
    # Use the first selected layer name
    layerName = font.selectedLayerNames[0]
    currentLayer = font.layers[layerName]

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