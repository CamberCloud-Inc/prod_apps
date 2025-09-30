import subprocess
import sys
import os
import argparse

# Install rembg and pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "rembg[gpu]", "pillow"])

from rembg import remove
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Remove backgrounds from images')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for processed image (default: ./)')
    parser.add_argument('-a', '--alpha-matting', action='store_true',
                        help='Enable alpha matting for better edge quality')
    parser.add_argument('-f', '--format', choices=['PNG', 'WEBP'], default='PNG',
                        help='Output format (default: PNG)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Expanded input_file: {input_file}")
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: Image file not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Open the image
    try:
        print(f"\nOpening image: {input_file}")
        input_image = Image.open(input_file)
        print(f"Image format: {input_image.format}, Size: {input_image.size}, Mode: {input_image.mode}")
        print(f"Original file size: {os.path.getsize(input_file)} bytes")
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Remove background
    try:
        print("\nRemoving background...")
        print("This may take a moment depending on image size...")

        # Configure options
        kwargs = {}
        if args.alpha_matting:
            print("Alpha matting enabled for better edge quality")
            kwargs['alpha_matting'] = True
            kwargs['alpha_matting_foreground_threshold'] = 240
            kwargs['alpha_matting_background_threshold'] = 10
            kwargs['alpha_matting_erode_size'] = 10

        # Remove background
        output_image = remove(input_image, **kwargs)
        print("Background removed successfully!")

        # Get the base filename without extension
        base_name = os.path.splitext(os.path.basename(input_file))[0]

        # Determine output file extension
        extension_map = {
            'PNG': '.png',
            'WEBP': '.webp'
        }
        output_extension = extension_map[args.format]
        output_filename = f"{base_name}_no_bg{output_extension}"
        output_path = os.path.join(args.output_dir, output_filename)

        # Save the image
        save_kwargs = {}
        if args.format == 'WEBP':
            save_kwargs['quality'] = 95
            save_kwargs['method'] = 6  # Best quality

        output_image.save(output_path, format=args.format, **save_kwargs)
        print(f"\nOutput saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
        print(f"Output format: {args.format}")

        # Print statistics
        size_diff = os.path.getsize(input_file) - os.path.getsize(output_path)
        if size_diff > 0:
            print(f"Size reduction: {size_diff} bytes ({size_diff / os.path.getsize(input_file) * 100:.1f}%)")
        else:
            print(f"Size increase: {abs(size_diff)} bytes ({abs(size_diff) / os.path.getsize(input_file) * 100:.1f}%)")

    except Exception as e:
        print(f"Error removing background: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nBackground removal completed!")


if __name__ == "__main__":
    main()