"""
Test script to analyze PSD file colors and detect LAB colors
"""

import sys
import os
from psd_tools import PSDImage
from psd2fabric.parser.shape_parser import is_likely_lab_color, lab2rgb

def analyze_layer_colors(layer, prefix=""):
    """Analyze a layer for color information"""
    print(f"{prefix}Layer: {layer.name} (Type: {layer.kind})")
    
    # Check for colors in layer info
    has_color = False
    
    # Check for shape layers
    if hasattr(layer, 'vector_mask') and layer.vector_mask:
        print(f"{prefix}  - Has vector mask: Yes")
        has_color = True
        
        # Look for fill color
        try:
            layer_data = getattr(layer, '_data', {})
            if isinstance(layer_data, dict) and 'FillColor' in layer_data:
                fill_color = layer_data['FillColor']
                print(f"{prefix}  - Found direct FillColor: {fill_color}")
                
                if isinstance(fill_color, dict) and 'Values' in fill_color:
                    color_values = fill_color['Values']
                    if isinstance(color_values, list) and len(color_values) >= 3:
                        print(f"{prefix}  - Color values: {color_values}")
                        
                        # Check if LAB
                        if is_likely_lab_color(color_values):
                            print(f"{prefix}  - DETECTED LAB COLOR: {color_values}")
                            rgb_values = lab2rgb([color_values[1], color_values[2], color_values[0]])
                            r, g, b = [int(v) for v in rgb_values]
                            hex_color = f"#{r:02x}{g:02x}{b:02x}"
                            print(f"{prefix}  - Converted to RGB: {[int(v) for v in rgb_values]}")
                            print(f"{prefix}  - Hex color: {hex_color}")
                        else:
                            print(f"{prefix}  - Standard RGB color")
        except Exception as e:
            print(f"{prefix}  - Error checking fill color: {str(e)}")
    
    # Check for solid color fill
    if hasattr(layer, 'solid_color') and layer.solid_color:
        print(f"{prefix}  - Has solid color: {layer.solid_color}")
        has_color = True
        try:
            values = layer.solid_color.values
            print(f"{prefix}  - Solid color values: {values}")
            
            # Check if LAB
            if is_likely_lab_color(values):
                print(f"{prefix}  - DETECTED LAB COLOR in solid_color: {values}")
                rgb_values = lab2rgb([values[1], values[2], values[0]])
                r, g, b = [int(v) for v in rgb_values]
                hex_color = f"#{r:02x}{g:02x}{b:02x}"
                print(f"{prefix}  - Converted to RGB: {[int(v) for v in rgb_values]}")
                print(f"{prefix}  - Hex color: {hex_color}")
        except Exception as e:
            print(f"{prefix}  - Error checking solid color: {str(e)}")
    
    # Check for stroke color
    if hasattr(layer, 'stroke') and layer.stroke:
        print(f"{prefix}  - Has stroke: Yes")
        has_color = True
        try:
            if hasattr(layer.stroke, 'color') and layer.stroke.color:
                values = layer.stroke.color.values
                print(f"{prefix}  - Stroke color values: {values}")
                
                # Check if LAB
                if is_likely_lab_color(values):
                    print(f"{prefix}  - DETECTED LAB COLOR in stroke: {values}")
                    rgb_values = lab2rgb([values[1], values[2], values[0]])
                    r, g, b = [int(v) for v in rgb_values]
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    print(f"{prefix}  - Converted to RGB: {[int(v) for v in rgb_values]}")
                    print(f"{prefix}  - Hex color: {hex_color}")
        except Exception as e:
            print(f"{prefix}  - Error checking stroke color: {str(e)}")
    
    # Check for effects
    if hasattr(layer, 'effects') and layer.effects:
        print(f"{prefix}  - Has effects: Yes")
        
        # Check for color overlay
        if hasattr(layer.effects, 'color_overlay') and layer.effects.color_overlay:
            has_color = True
            try:
                coloroverlay = layer.effects.color_overlay
                color_values = coloroverlay.color.values
                print(f"{prefix}  - Color overlay values: {color_values}")
                
                # Check if LAB
                if is_likely_lab_color(color_values):
                    print(f"{prefix}  - DETECTED LAB COLOR in color_overlay: {color_values}")
                    rgb_values = lab2rgb([color_values[1], color_values[2], color_values[0]])
                    r, g, b = [int(v) for v in rgb_values]
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    print(f"{prefix}  - Converted to RGB: {[int(v) for v in rgb_values]}")
                    print(f"{prefix}  - Hex color: {hex_color}")
            except Exception as e:
                print(f"{prefix}  - Error checking color overlay: {str(e)}")
    
    # Check for other color attributes
    for attr_name in ['background_color', 'fill', 'color']:
        if hasattr(layer, attr_name):
            attr_value = getattr(layer, attr_name)
            if attr_value:
                has_color = True
                print(f"{prefix}  - Has {attr_name}: {attr_value}")
                try:
                    # Try to access color values
                    if hasattr(attr_value, 'values'):
                        values = attr_value.values
                        print(f"{prefix}  - {attr_name} values: {values}")
                        
                        # Check if LAB
                        if is_likely_lab_color(values):
                            print(f"{prefix}  - DETECTED LAB COLOR in {attr_name}: {values}")
                            rgb_values = lab2rgb([values[1], values[2], values[0]])
                            r, g, b = [int(v) for v in rgb_values]
                            hex_color = f"#{r:02x}{g:02x}{b:02x}"
                            print(f"{prefix}  - Converted to RGB: {[int(v) for v in rgb_values]}")
                            print(f"{prefix}  - Hex color: {hex_color}")
                except Exception as e:
                    print(f"{prefix}  - Error checking {attr_name}: {str(e)}")
    
    # If this is a shape layer with no reported color, check raw data
    if layer.kind == 'shape' and not has_color:
        try:
            # Look for any color-related attributes in raw data
            layer_data = getattr(layer, '_data', {})
            if isinstance(layer_data, dict):
                print(f"{prefix}  - Examining raw layer data for colors")
                for key in layer_data:
                    if 'color' in key.lower() or 'fill' in key.lower():
                        print(f"{prefix}  - Found color-related key: {key} = {layer_data[key]}")
        except Exception as e:
            print(f"{prefix}  - Error examining raw data: {str(e)}")
    
    # Process child layers for group layers and artboards
    if layer.kind in ['group', 'artboard']:
        for child in layer:
            analyze_layer_colors(child, prefix + "  ")
    
    # Also process any descendants that might not be direct children
    if hasattr(layer, 'descendants') and callable(getattr(layer, 'descendants')):
        descendants = list(layer.descendants())
        if len(descendants) > 0 and descendants[0] != layer:
            for descendant in descendants:
                # Skip if we already processed direct children
                if descendant.parent == layer:
                    continue
                analyze_layer_colors(descendant, prefix + "  ")

def analyze_psd_colors(psd_path):
    """Analyze all colors in a PSD file"""
    print(f"Analyzing PSD file: {psd_path}")
    print("=" * 80)
    
    try:
        # Open PSD file
        psd = PSDImage.open(psd_path)
        print(f"PSD dimensions: {psd.width} x {psd.height}")
        print(f"Number of layers: {len(list(psd.descendants()))}")
        
        # Analyze each layer
        print("\nAnalyzing layers:")
        print("-" * 80)
        
        # Process each top-level layer
        for layer in psd:
            analyze_layer_colors(layer)
        
        # Look for any standalone shape layers that might not be in the hierarchy
        all_layers = list(psd.descendants())
        shape_layers = [layer for layer in all_layers if layer.kind == 'shape']
        if shape_layers:
            print("\nFound standalone shape layers:")
            for shape in shape_layers:
                print(f"Shape layer: {shape.name}")
        
        print("\nAnalysis complete!")
        print(f"Total layers analyzed: {len(list(psd.descendants()))}")
        
    except Exception as e:
        print(f"Error analyzing PSD file: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        psd_path = sys.argv[1]
    else:
        # Default to CV Template 05
        psd_path = "/Users/kshitij.jain/Downloads/clean-modern-resume-portfolio-cv-template (1)/CV-Template-05.psd"
        
    if not os.path.exists(psd_path):
        print(f"Error: PSD file not found: {psd_path}")
        print("Please provide a valid PSD file path")
        sys.exit(1)
        
    analyze_psd_colors(psd_path)
