import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Convert color images to grayscale')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for grayscale image (default: ./)')

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

    # Get the base filename and extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    extension = os.path.splitext(input_file)[1]

    output_filename = f"{base_name}_grayscale{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Convert to grayscale
    try:
        # Convert to grayscale (L mode)
        grayscale_img = img.convert('L')

        print(f"Converting from {img.mode} to grayscale (L mode)")
        print(f"Output size: {grayscale_img.size}")

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        grayscale_img.save(output_path, **save_kwargs)
        print(f"Successfully converted image to grayscale")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error converting to grayscale: {e}")
        sys.exit(1)

    print("\nGrayscale conversion completed!")


if __name__ == "__main__":
    main()