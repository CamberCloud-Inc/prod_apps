import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Generate 200x200 thumbnail from images')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for thumbnail (default: ./)')

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

    output_filename = f"{base_name}_thumb.jpg"
    output_path = os.path.join(args.output_dir, output_filename)

    # Create thumbnail (200x200)
    try:
        thumbnail_size = (200, 200)

        # Create a copy of the image to work with
        img_copy = img.copy()

        # Use thumbnail method which maintains aspect ratio
        img_copy.thumbnail(thumbnail_size, Image.Resampling.LANCZOS)

        # Create a 200x200 canvas with white background
        thumb = Image.new('RGB', thumbnail_size, (255, 255, 255))

        # Calculate position to center the image
        offset_x = (thumbnail_size[0] - img_copy.size[0]) // 2
        offset_y = (thumbnail_size[1] - img_copy.size[1]) // 2

        # Convert RGBA to RGB if needed
        if img_copy.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img_copy.size, (255, 255, 255))
            if img_copy.mode == 'P':
                img_copy = img_copy.convert('RGBA')
            if img_copy.mode in ('RGBA', 'LA'):
                background.paste(img_copy, mask=img_copy.split()[-1])
                img_copy = background

        # Paste the resized image onto the canvas
        thumb.paste(img_copy, (offset_x, offset_y))

        print(f"Creating thumbnail from {img.size} to {thumbnail_size}")
        print(f"Resized to: {img_copy.size}")

        # Save as JPEG with good quality
        thumb.save(output_path, 'JPEG', quality=90, optimize=True)
        print(f"Successfully created thumbnail")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error creating thumbnail: {e}")
        sys.exit(1)

    print("\nThumbnail generation completed!")


if __name__ == "__main__":
    main()