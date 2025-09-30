import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image, ImageOps


def main():
    parser = argparse.ArgumentParser(description='Add borders/frames to images')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for bordered image (default: ./)')

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

    output_filename = f"{base_name}_bordered{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Add border
    try:
        # Border width hardcoded to 50 pixels
        border_width = 50

        # Add black border using ImageOps.expand
        bordered_img = ImageOps.expand(img, border=border_width, fill='black')

        print(f"Successfully added border")
        print(f"Border width: {border_width} pixels")
        print(f"Border color: black")
        print(f"New size: {bordered_img.size} (from {img.size})")

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            # Convert RGBA to RGB if needed
            if bordered_img.mode == 'RGBA':
                rgb_img = Image.new('RGB', bordered_img.size, (0, 0, 0))
                rgb_img.paste(bordered_img, mask=bordered_img.split()[3] if len(bordered_img.split()) == 4 else None)
                bordered_img = rgb_img
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        bordered_img.save(output_path, **save_kwargs)
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error adding border: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nBorder addition completed!")


if __name__ == "__main__":
    main()