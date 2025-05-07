import json
import os
import requests
import hashlib
import time
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Marvel API credentials
PUBLIC_KEY = os.getenv("MARVEL_PUBLIC_KEY")
PRIVATE_KEY = os.getenv("MARVEL_PRIVATE_KEY")

# Available Marvel API resources
MARVEL_RESOURCES = ["characters", "comics", "events"]

# List of attributes to remove (copied from clean_marvel_json.py)
attributes_to_remove = [
    "series",
    "variants",
    "creators",
    "characters",
    "comics",
    "stories",
    "events",
    "issueNumber",
    "variantDescription",
    "isbn",
    "ean",
    "issn",
    "pageCount",
    "textObjects",
    "collections",
    "collectedIssues",
    "dates",
    "prices",
    "digitalId",
    "upc",
    "urls",
    "next",
    "previous",
    "images",
]


def generate_hash():
    """Generate the required hash for Marvel API authentication"""
    ts = str(time.time())
    hash_input = ts + PRIVATE_KEY + PUBLIC_KEY
    return ts, hashlib.md5(hash_input.encode()).hexdigest()


def fetch_marvel_resource(resource_type, limit=100, offset=0):
    """Fetch data from Marvel API for the specified resource type"""
    if resource_type not in MARVEL_RESOURCES:
        raise ValueError(f"Invalid resource type. Must be one of: {', '.join(MARVEL_RESOURCES)}")

    ts, hash_value = generate_hash()
    url = f"https://gateway.marvel.com/v1/public/{resource_type}"
    params = {"ts": ts, "apikey": PUBLIC_KEY, "hash": hash_value, "limit": limit, "offset": offset}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e.response, "text"):
            print(f"Response text: {e.response.text}")
        return {"code": "RequestError", "message": str(e)}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return {"code": "JSONError", "message": str(e)}


def remove_resources_with_no_thumbnail(data):
    """Remove resources with no thumbnail"""
    data["data"]["results"] = [
        resource
        for resource in data["data"]["results"]
        if resource.get("thumbnail", {}).get("path")
        != "http://i.annihil.us/u/prod/marvel/i/mg/b/40/image_not_available"
    ]
    return data


def remove_attributes(data):
    """Remove specified attributes from the resource data"""
    for resource in data["data"]["results"]:
        for attr in attributes_to_remove:
            resource.pop(attr, None)
    return data


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fetch and process Marvel API data")
    parser.add_argument(
        "resource", choices=MARVEL_RESOURCES, help="Type of Marvel resource to fetch"
    )
    parser.add_argument(
        "--limit", type=int, default=100, help="Number of items to fetch (default: 100)"
    )
    parser.add_argument("--offset", type=int, default=0, help="Offset for pagination (default: 0)")
    args = parser.parse_args()

    # Create output directory if it doesn't exist
    output_dir = "00_Tests"
    os.makedirs(output_dir, exist_ok=True)

    # Fetch the specified resource
    print(f"Fetching {args.limit} {args.resource}...")
    response_data = fetch_marvel_resource(args.resource, limit=args.limit, offset=args.offset)

    # Check if the response is successful
    if not isinstance(response_data, dict):
        print("Error: Invalid response format")
        return

    if response_data.get("code") not in [200, "Ok"]:
        error_message = response_data.get("message", "Unknown error")
        print(f"Error: API returned code {response_data.get('code')}")
        print(f"Error message: {error_message}")
        return

    # Process the data
    processed_data = remove_resources_with_no_thumbnail(response_data)
    processed_data = remove_attributes(processed_data)

    # Save to file
    output_file = os.path.join(output_dir, f"marvel_{args.resource}_cleaned.json")
    with open(output_file, "w") as f:
        json.dump(processed_data, f, indent=2)

    print(
        f"Successfully saved {len(processed_data['data']['results'])} {args.resource} to {output_file}"
    )


if __name__ == "__main__":
    if not PUBLIC_KEY or not PRIVATE_KEY:
        print("Error: Please set MARVEL_PUBLIC_KEY and MARVEL_PRIVATE_KEY in your .env file")
    else:
        main()
