import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Crop images to specified dimensions from center')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for cropped image (default: ./)')

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
        print(f"Original size: {img.size}, Mode: {img.mode}")
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Get the base filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    extension = os.path.splitext(input_file)[1]

    output_filename = f"{base_name}_cropped{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Crop the image from center - hardcoded to 800x600
    try:
        width, height = img.size
        target_width = 800
        target_height = 600

        # Calculate center crop coordinates
        left = (width - target_width) / 2
        top = (height - target_height) / 2
        right = (width + target_width) / 2
        bottom = (height + target_height) / 2

        # Ensure crop dimensions don't exceed image dimensions
        if target_width > width or target_height > height:
            print(f"Warning: Target dimensions ({target_width}x{target_height}) exceed image size ({width}x{height})")
            print(f"Adjusting crop to fit image dimensions")
            target_width = min(target_width, width)
            target_height = min(target_height, height)
            left = (width - target_width) / 2
            top = (height - target_height) / 2
            right = (width + target_width) / 2
            bottom = (height + target_height) / 2

        cropped_img = img.crop((left, top, right, bottom))

        print(f"Cropping from center: {img.size} -> {cropped_img.size}")

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        cropped_img.save(output_path, **save_kwargs)
        print(f"Successfully cropped image")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error cropping image: {e}")
        sys.exit(1)

    print("\nImage cropping completed!")


if __name__ == "__main__":
    main()