import subprocess
import sys
import os
import argparse

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow-heif", "Pillow"])

from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()


def main():
    parser = argparse.ArgumentParser(description='Convert Apple HEIC format images to JPG')
    parser.add_argument('input_file', help='Path to the input HEIC file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for JPG file (default: ./)')
    parser.add_argument('-q', '--quality', type=int, default=95,
                        help='JPEG quality (1-100, default: 95)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: HEIC file not found at: {input_file}")
        sys.exit(1)

    # Validate file extension
    ext = os.path.splitext(input_file)[1].lower()
    if ext not in ['.heic', '.heif']:
        print(f"Warning: File extension is {ext}, expected .heic or .heif")
        print("Attempting conversion anyway...")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Open the HEIC image
    try:
        img = Image.open(input_file)
        print(f"Successfully opened HEIC image: {input_file}")
        print(f"Image size: {img.size}, Mode: {img.mode}")
    except Exception as e:
        print(f"Error opening HEIC image: {e}")
        print("\nTroubleshooting:")
        print("- Ensure the file is a valid HEIC/HEIF image")
        print("- The pillow-heif library may not be properly installed")
        sys.exit(1)

    # Get the base filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}.jpg"
    output_path = os.path.join(args.output_dir, output_filename)

    # Convert to RGB if necessary (HEIC images might be in different color modes)
    if img.mode not in ('RGB', 'L'):
        print(f"Converting from {img.mode} to RGB mode")
        img = img.convert('RGB')

    # Save as JPEG
    try:
        print(f"Converting HEIC to JPG with quality={args.quality}")
        img.save(output_path, 'JPEG', quality=args.quality, optimize=True)

        print(f"Successfully converted to JPG")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error saving JPG image: {e}")
        sys.exit(1)

    print("\nHEIC to JPG conversion completed!")


if __name__ == "__main__":
    main()