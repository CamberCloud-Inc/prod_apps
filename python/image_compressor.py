import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Compress image file size while maintaining quality')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for compressed image (default: ./)')

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
        original_file_size = os.path.getsize(input_file)
        print(f"Original file size: {original_file_size} bytes ({original_file_size / 1024:.2f} KB)")
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Get the base filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    extension = os.path.splitext(input_file)[1]

    output_filename = f"{base_name}_compressed{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Compress the image
    try:
        # Convert RGBA to RGB if saving as JPEG
        if extension.lower() in ['.jpg', '.jpeg'] and img.mode == 'RGBA':
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[3])
            img = rgb_img

        # Save with quality=85 for compression
        save_kwargs = {'quality': 85, 'optimize': True}

        if extension.lower() in ['.jpg', '.jpeg']:
            img.save(output_path, 'JPEG', **save_kwargs)
        elif extension.lower() == '.png':
            img.save(output_path, 'PNG', optimize=True)
        else:
            img.save(output_path, **save_kwargs)

        compressed_file_size = os.path.getsize(output_path)
        compression_ratio = (1 - compressed_file_size / original_file_size) * 100

        print(f"Successfully compressed image")
        print(f"Output saved to: {output_path}")
        print(f"Compressed file size: {compressed_file_size} bytes ({compressed_file_size / 1024:.2f} KB)")
        print(f"Compression ratio: {compression_ratio:.2f}% reduction")
    except Exception as e:
        print(f"Error compressing image: {e}")
        sys.exit(1)

    print("\nImage compression completed!")


if __name__ == "__main__":
    main()