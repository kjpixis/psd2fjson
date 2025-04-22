#!/usr/bin/env python3
"""
Script to convert Template-01 PSD file to JSON format
"""

import os
import sys
import json
import logging
from psd_tools import PSDImage

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import parser
from psd2fabric.parser.psd_parser import psd_to_fabric

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('psd2json')



def convert_psd_to_json(psd_path, output_path):
    """Convert PSD file to JSON format"""
    logger.info(f"Processing PSD file: {psd_path}")
    
    # Open PSD file
    psd = PSDImage.open(psd_path)
    logger.info(f"PSD dimensions: {psd.width} x {psd.height}")
    
    # Convert PSD to Fabric.js format
    logger.info("Converting PSD to Fabric.js format...")
    fabric_obj = psd_to_fabric(psd)
    
    # Convert Fabric object to dictionary
    canvas_data = fabric_obj.to_dict() if hasattr(fabric_obj, 'to_dict') else fabric_obj
    
    # Transform the output to match the desired format
    new_format = {
        "dpi": 96,
        "children": canvas_data.get("objects", []),
        "backgroundColor": canvas_data.get("background", "#ffffff"),
        "backgroundImage": None,
        "sizes": [
            {
                "height": psd.height,
                "width": psd.width,
                "type": "custom",
                "name": f"{psd.width}:{psd.height}",
                "aspectRatio": f"{psd.width}:{psd.height}"
            }
        ],
        "key": "original"
    }
    
    # Add additional properties to each object in the children array
    for child in new_format["children"]:
        # Change i-text type to text
        if child.get("type") == "i-text":
            child["type"] = "text"
            
        # Set defaults for required properties if they don't exist
        if "layerType" not in child:
            if child.get("type") == "image":
                child["layerType"] = "Image"
            elif child.get("type") == "path":
                child["layerType"] = "Shape" 
            elif child.get("type") == "text":
                child["layerType"] = "Text"
            elif child.get("type") == "group":
                child["layerType"] = "Group"
            else:
                child["layerType"] = "Object"
                
        # Add asset properties for images
        if child.get("type") == "image" and "assetType" not in child:
            child["assetType"] = "asset"
            # Generate a placeholder assetId (would be replaced with real IDs in production)
            import uuid
            child["assetId"] = str(uuid.uuid4())
            child["repositionOption"] = "top-left"
            child["cropDetails"] = {
                "leftPercent": 0,
                "topPercent": 0,
                "rightPercent": 0,
                "bottomPercent": 0
            }
            
    # Save JSON to file
    with open(output_path, 'w') as f:
        # Add default handler for any object types that aren't natively JSON serializable
        def json_serializer(obj):
            # Handle string-like objects
            if isinstance(obj, (str, bytes)):
                return str(obj)
            # Handle String type from psd_tools
            if hasattr(obj, '__class__') and obj.__class__.__name__ == 'String':
                return str(obj)
            # Handle any object with a value attribute (which String has)
            if hasattr(obj, 'value'):
                return obj.value
            
            # If we can't serialize it, raise an error with details
            raise TypeError(f"Type {type(obj)} not serializable")
            
        json.dump(new_format, f, indent=2, default=json_serializer)
    logger.info(f"Successfully saved JSON to: {output_path}")
    
    # Log some statistics
    logger.info(f"Total objects in JSON: {len(new_format['children'])}")
    
    # Count object types
    object_types = {}
    for obj in new_format["children"]:
        obj_type = obj.get('type')
        if obj_type in object_types:
            object_types[obj_type] += 1
        else:
            object_types[obj_type] = 1
    
    logger.info("Object types:")
    for obj_type, count in object_types.items():
        logger.info(f"  - {obj_type}: {count}")
    
    return new_format

if __name__ == "__main__":
   
    psd_path = "/Users/kshitij.jain/Desktop/Letterhead-16.psd"
    output_path = "/Users/kshitij.jain/psd2fjson/Letterhead-16_output.json"
    
    # Convert PSD to JSON
    print(f"Converting {psd_path} to JSON...")

    canvas_data = convert_psd_to_json(psd_path, output_path)
    print(f"Conversion complete! Output saved to: {output_path}")
