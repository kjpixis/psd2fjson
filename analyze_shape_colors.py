"""
Script to analyze shape layer color properties in a PSD file
"""

import sys
import os
from psd_tools import PSDImage

def analyze_shape_layers(psd_path):
    """Analyze shape layers and their color properties"""
    print(f"Analyzing PSD file: {psd_path}")
    print("=" * 80)
    
    # Open PSD file
    psd = PSDImage.open(psd_path)
    print(f"PSD dimensions: {psd.width} x {psd.height}")
    
    # Find all shape layers
    shape_layers = []
    for layer in psd.descendants():
        if hasattr(layer, 'vector_mask') and layer.vector_mask:
            shape_layers.append(layer)
    
    print(f"\nFound {len(shape_layers)} shape layers")
    print("-" * 80)
    
    # Analyze each shape layer
    for i, layer in enumerate(shape_layers[:10], 1):  # Limit to first 10 for brevity
        print(f"\nShape Layer {i}: {layer.name}")
        
        # Check basic properties
        print(f"  Position: {layer.left}, {layer.top}")
        print(f"  Size: {layer.width} x {layer.height}")
        
        # Check for direct fill color
        try:
            # Try to access the layer data directly to find FillColor
            layer_data = getattr(layer, '_data', {})
            if isinstance(layer_data, dict) and 'FillColor' in layer_data:
                fill_color = layer_data['FillColor']
                print(f"  FillColor found in raw data: {fill_color}")
                
                if isinstance(fill_color, dict) and 'Values' in fill_color:
                    print(f"    Values: {fill_color['Values']}")
            else:
                print("  No FillColor in raw data")
                
            # List all color-related keys in raw data
            color_keys = [k for k in layer_data.keys() if 'color' in k.lower() or 'fill' in k.lower()]
            if color_keys:
                print(f"  Found color-related keys: {color_keys}")
                for key in color_keys:
                    print(f"    {key}: {layer_data[key]}")
        except Exception as e:
            print(f"  Error checking raw data: {e}")
        
        # Check for solid color
        if hasattr(layer, 'solid_color') and layer.solid_color:
            print(f"  Solid color: {layer.solid_color}")
        else:
            print("  No solid color")
            
        # Check for effects
        if hasattr(layer, 'effects') and layer.effects:
            print(f"  Has effects: Yes")
            
            # Check effect types
            effect_types = []
            if hasattr(layer.effects, '__dict__'):
                effect_attrs = vars(layer.effects)
                for attr_name, attr_value in effect_attrs.items():
                    if attr_value is not None:
                        effect_types.append(attr_name)
            
            if effect_types:
                print(f"  Effect types: {effect_types}")
                
                # Check for color overlay
                if hasattr(layer.effects, 'color_overlay') and layer.effects.color_overlay:
                    coloroverlay = layer.effects.color_overlay
                    print(f"  Color overlay: {coloroverlay}")
                    
                    if hasattr(coloroverlay, 'color') and coloroverlay.color:
                        print(f"    Color: {coloroverlay.color}")
                        
                        if hasattr(coloroverlay.color, 'values'):
                            print(f"    Color values: {coloroverlay.color.values}")
            else:
                print("  No effect types found")
        else:
            print("  Has effects: No")
    
    print("\nAnalysis complete!")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        psd_path = sys.argv[1]
    else:
        # Default to Template-01
        psd_path = "/Users/kshitij.jain/Downloads/clean-modern-resume-portfolio-cv-template/CV-Template-01.psd"
        
    if not os.path.exists(psd_path):
        print(f"Error: PSD file not found: {psd_path}")
        sys.exit(1)
        
    analyze_shape_layers(psd_path)
