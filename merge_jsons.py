import os
import json

# Define input and output directories
input_dir = "Resume_jsons2"  # Folder containing your JSON files
output_file = "formatted_annotations2.json"  # Output JSONL file for Donut

# Initialize a list to store the formatted annotations
donut_annotations = []

# Iterate through JSON files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(".json"):
        json_path = os.path.join(input_dir, filename)
        with open(json_path, "r") as f:
            data = json.load(f)

            # Extract the first key (filename) and regions
            for image_key, image_data in data.items():
                if "regions" in image_data:
                    # Initialize the Donut annotation structure
                    donut_annotation = {
                        "file_name": image_key,  # Keep the image file name with extension
                        "annotations": []
                    }

                    # Map regions to Donut's key-value structure
                    for region_id, region_data in image_data["regions"].items():
                        region_name = region_data["region_attributes"].get("name", "")
                        if region_name:
                            donut_annotation["annotations"].append({
                                "label": region_name,
                                "x": region_data["shape_attributes"]["x"],
                                "y": region_data["shape_attributes"]["y"],
                                "width": region_data["shape_attributes"]["width"],
                                "height": region_data["shape_attributes"]["height"]
                            })

                    # Add the formatted annotation to the list (only once per image)
                    donut_annotations.append(donut_annotation)

# Write the annotations to a JSONL file
with open(output_file, "w") as f:
    for annotation in donut_annotations:
        f.write(json.dumps(annotation) + "\n")

print(f"Converted {len(donut_annotations)} annotations to Donut format!")
