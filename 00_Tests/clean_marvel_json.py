import json
import os

# Hardcoded list of file paths
file_paths = [
    "00_Tests/characters_response.json",
    "00_Tests/comics_response.json",
    "00_Tests/characters_response.json"
]

# List of attributes to remove
attributes_to_remove = [
    "series", "variants", "creators", "characters", "comics",
    "stories", "events", "issueNumber", "variantDescription",
    "isbn", "ean", "issn", "pageCount", "textObjects", "collections", "collectedIssues",
    "dates", "prices", "digitalId", "upc", "urls", "next", "previous", "images"
]


# Function to remove resource with the specified thumbnail
def remove_comics_with_no_thumbnail(data):
    data["data"]["results"] = [
        resource for resource in data["data"]["results"]
        if resource.get("thumbnail", {}).get("path") != "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available"
    ]
    return data


# Function to remove specified attributes from the resource data
def remove_attributes(data):
    for resource in data["data"]["results"]:
        for attr in attributes_to_remove:
            resource.pop(attr, None)  # Remove the attribute if it exists
    return data


# Process each file path
for file_path in file_paths:
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"Error: The file {file_path} was not found.")
        continue  # Skip to the next file path

    # Read the JSON file
    with open(file_path, "r") as file:
        json_data = json.load(file)

    # Remove comics with no thumbnail
    json_data = remove_comics_with_no_thumbnail(json_data)

    # Remove the specified attributes
    updated_data = remove_attributes(json_data)

    # Write the updated data to a new JSON file
    original_file_name = os.path.basename(file_path)  # Get the original file name
    new_file_path = f"00_Tests/updated_{original_file_name}"  # Specify the new file path
    with open(new_file_path, "w") as file:
        json.dump(updated_data, file, indent=2)

    print(f"File updated into {new_file_path}")
