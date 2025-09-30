import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Resize images to specific dimensions')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for resized image (default: ./)')
    parser.add_argument('-w', '--width', type=int, default=800,
                        help='Target width in pixels (default: 800)')
    parser.add_argument('-H', '--height', type=int, default=600,
                        help='Target height in pixels (default: 600)')

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

    output_filename = f"{base_name}_resized_{args.width}x{args.height}{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Resize the image
    try:
        target_size = (args.width, args.height)
        resized_img = img.resize(target_size, Image.Resampling.LANCZOS)

        print(f"Resizing from {img.size} to {target_size}")

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        resized_img.save(output_path, **save_kwargs)
        print(f"Successfully resized image")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error resizing image: {e}")
        sys.exit(1)

    print("\nImage resizing completed!")


if __name__ == "__main__":
    main()