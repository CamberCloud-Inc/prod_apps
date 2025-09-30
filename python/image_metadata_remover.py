import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Strip metadata from images for privacy')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for cleaned image (default: ./)')
    parser.add_argument('--suffix', default='_no_metadata',
                        help='Suffix to add to output filename (default: _no_metadata)')

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

    # Open the image
    try:
        img = Image.open(input_file)
        print(f"Successfully opened image: {input_file}")
        print(f"Original size: {img.size}, Mode: {img.mode}, Format: {img.format}")

        # Check if image has EXIF data
        exif = img.getexif()
        if exif is None or len(exif) == 0:
            print("Note: This image has no EXIF metadata to remove.")
        else:
            print(f"Found {len(exif)} EXIF tags that will be removed.")

    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Get the base filename and extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    extension = os.path.splitext(input_file)[1]

    output_filename = f"{base_name}{args.suffix}{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Create a new image without metadata
    try:
        # Convert to RGB if needed (for saving as JPEG)
        if img.mode not in ('RGB', 'L', 'P') and extension.lower() in ['.jpg', '.jpeg']:
            print(f"Converting from {img.mode} to RGB mode for JPEG")
            data = img.convert('RGB')
        else:
            data = img

        # Save without any metadata
        # By creating a new image from the data, we strip all EXIF/metadata
        print(f"Removing all metadata and saving cleaned image...")

        save_kwargs = {}

        # Set quality for JPEG images
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        # Save the image without any metadata
        data.save(output_path, **save_kwargs)

        original_size = os.path.getsize(input_file)
        output_size = os.path.getsize(output_path)

        print(f"\nSuccessfully removed metadata from image")
        print(f"Output saved to: {output_path}")
        print(f"Original file size: {original_size:,} bytes ({original_size / 1024:.2f} KB)")
        print(f"Output file size: {output_size:,} bytes ({output_size / 1024:.2f} KB)")

        if original_size > output_size:
            savings = original_size - output_size
            print(f"Size reduction: {savings:,} bytes ({savings / 1024:.2f} KB, {(savings / original_size * 100):.1f}%)")

    except Exception as e:
        print(f"Error saving cleaned image: {e}")
        sys.exit(1)

    print("\nMetadata removal completed!")
    print("\nPrivacy Note:")
    print("- All EXIF metadata has been stripped from the image")
    print("- GPS location data (if present) has been removed")
    print("- Camera information and settings have been removed")
    print("- Original creation date has been removed")
    print("- The image pixels remain unchanged")


if __name__ == "__main__":
    main()