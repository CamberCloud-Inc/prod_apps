import subprocess
import sys
import os
import argparse
import json

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "piexif"])

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import piexif


def get_exif_data(image_path):
    """Extract EXIF data from image file."""
    exif_data = {}

    try:
        img = Image.open(image_path)

        # Get EXIF data using Pillow
        exif = img.getexif()

        if exif is None or len(exif) == 0:
            return None

        # Parse standard EXIF tags
        for tag_id, value in exif.items():
            tag_name = TAGS.get(tag_id, tag_id)

            # Handle GPS data separately
            if tag_name == "GPSInfo":
                gps_data = {}
                for gps_tag_id, gps_value in value.items():
                    gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_data[gps_tag_name] = str(gps_value)
                exif_data[tag_name] = gps_data
            else:
                # Convert value to string for JSON serialization
                try:
                    exif_data[tag_name] = str(value)
                except:
                    exif_data[tag_name] = "Unable to decode"

        return exif_data

    except Exception as e:
        print(f"Error reading EXIF data with Pillow: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Extract EXIF metadata from photos')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for metadata JSON file (default: ./)')
    parser.add_argument('--format', choices=['json', 'text'], default='json',
                        help='Output format (default: json)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: Image file not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Get basic file info
    file_size = os.path.getsize(input_file)
    print(f"\nFile: {os.path.basename(input_file)}")
    print(f"Size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

    # Get image dimensions
    try:
        img = Image.open(input_file)
        print(f"Dimensions: {img.size[0]} x {img.size[1]} pixels")
        print(f"Format: {img.format}")
        print(f"Mode: {img.mode}")
    except Exception as e:
        print(f"Could not open image: {e}")
        sys.exit(1)

    # Extract EXIF data
    print("\nExtracting EXIF metadata...")
    exif_data = get_exif_data(input_file)

    if exif_data is None or len(exif_data) == 0:
        print("No EXIF metadata found in this image.")
        print("\nNote: Not all images contain EXIF data. It's commonly found in:")
        print("- Photos taken with digital cameras")
        print("- Photos taken with smartphones")
        print("- Images that haven't been stripped of metadata")

        # Still create an output file with basic info
        exif_data = {
            "note": "No EXIF metadata found",
            "filename": os.path.basename(input_file),
            "file_size_bytes": file_size,
            "dimensions": f"{img.size[0]}x{img.size[1]}",
            "format": img.format,
            "mode": img.mode
        }
    else:
        print(f"Found {len(exif_data)} EXIF tags")

        # Add basic file info to output
        exif_data["_file_info"] = {
            "filename": os.path.basename(input_file),
            "file_size_bytes": file_size,
            "dimensions": f"{img.size[0]}x{img.size[1]}",
            "format": img.format,
            "mode": img.mode
        }

        # Print some key metadata
        print("\nKey Metadata:")
        key_fields = ['Make', 'Model', 'DateTime', 'DateTimeOriginal',
                      'ExposureTime', 'FNumber', 'ISOSpeedRatings', 'FocalLength']

        for field in key_fields:
            if field in exif_data:
                print(f"  {field}: {exif_data[field]}")

    # Save to output file
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    if args.format == 'json':
        output_filename = f"{base_name}_metadata.json"
        output_path = os.path.join(args.output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(exif_data, f, indent=2, ensure_ascii=False)

        print(f"\nMetadata saved to: {output_path}")

    else:  # text format
        output_filename = f"{base_name}_metadata.txt"
        output_path = os.path.join(args.output_dir, output_filename)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"EXIF Metadata for: {os.path.basename(input_file)}\n")
            f.write("=" * 60 + "\n\n")

            for key, value in exif_data.items():
                if isinstance(value, dict):
                    f.write(f"{key}:\n")
                    for sub_key, sub_value in value.items():
                        f.write(f"  {sub_key}: {sub_value}\n")
                else:
                    f.write(f"{key}: {value}\n")

        print(f"\nMetadata saved to: {output_path}")

    print("\nMetadata extraction completed!")


if __name__ == "__main__":
    main()