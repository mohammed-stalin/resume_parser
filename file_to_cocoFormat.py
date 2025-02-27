import json
from datetime import datetime

def convert_to_coco_format(input_data):
    # Initialize COCO format structure
    coco_format = {
        "info": {
            "year": datetime.now().year,
            "version": "1.0",
            "description": "Converted to COCO format",
            "date_created": datetime.now().strftime("%Y-%m-%d")
        },
        "images": [],
        "annotations": [],
        "categories": [
            {"id": 1, "name": "name"},
            {"id": 2, "name": "phone"},
            {"id": 3, "name": "email"},
            {"id": 4, "name": "experiences"},
            {"id": 5, "name": "skills"},
            {"id": 6, "name": "languages"},
            {"id": 7, "name": "study"}
        ]
    }
    
    # Keep track of annotation ID
    annotation_id = 1
    
    # Process each line of input data
    for image_idx, image_data in enumerate(input_data, 1):
        # Add image information
        image_info = {
            "id": image_idx,
            "file_name": image_data["file_name"],
            # You might want to add actual width and height if available
            "width": 1200,  # placeholder
            "height": 1800  # placeholder
        }
        coco_format["images"].append(image_info)
        
        # Process annotations for this image
        for ann in image_data["annotations"]:
            # Get category ID based on label
            category_id = next(
                (cat["id"] for cat in coco_format["categories"] if cat["name"] == ann["label"]),
                None
            )
            
            if category_id is None:
                continue
                
            # Convert to COCO annotation format
            coco_annotation = {
                "id": annotation_id,
                "image_id": image_idx,
                "category_id": category_id,
                "bbox": [
                    ann["x"],
                    ann["y"],
                    ann["width"],
                    ann["height"]
                ],
                "area": ann["width"] * ann["height"],
                "iscrowd": 0
            }
            
            coco_format["annotations"].append(coco_annotation)
            annotation_id += 1
    
    return coco_format

# Example usage
if __name__ == "__main__":
    # Read input data
    input_data = []
    with open("file", "r") as f:
        for line in f:
            if line.strip():  # Skip empty lines
                input_data.append(json.loads(line))
    
    # Convert to COCO format
    coco_format = convert_to_coco_format(input_data)
    
    # Save the converted format
    with open("coco_annotations_vF.json", "w") as f:
        json.dump(coco_format, f, indent=2)
    
    # Validate the format
    if "images" in coco_format and "annotations" in coco_format:
        print("Successfully converted to COCO format!")
        print(f"Total images: {len(coco_format['images'])}")
        print(f"Total annotations: {len(coco_format['annotations'])}")