# menuTitle: Duplicate Layer

font = CurrentFont()
g = CurrentGlyph()

if g:
    # if glyph is selected 
    layer = g.layer
    layerName = layer.name

else:
    # if no glyph is selected, fallback to the default layer
    if "foreground" in font.layers:
        layer = font.layers["foreground"]
    
    else:
        # fallback to default layer
        layer = font.defaultLayer
    
    layerName = layer.name

newLayerName = f"{layerName} copy"

while newLayerName in font.layerOrder:
    newLayerName = f"{newLayerName} copy"

font.duplicateLayer(layerName, newLayerName)

print(f"Duplicated layer '{layerName}' as '{newLayerName}'.")