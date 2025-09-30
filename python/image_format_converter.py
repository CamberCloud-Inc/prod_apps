import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Convert images between different formats (PNG/JPG/WebP)')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for converted image (default: ./)')
    parser.add_argument('-f', '--format', choices=['PNG', 'JPEG', 'WEBP'], default='PNG',
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
        img = Image.open(input_file)
        print(f"Successfully opened image: {input_file}")
        print(f"Image format: {img.format}, Size: {img.size}, Mode: {img.mode}")
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Determine output file extension
    extension_map = {
        'PNG': '.png',
        'JPEG': '.jpg',
        'WEBP': '.webp'
    }
    output_extension = extension_map[args.format]
    output_filename = f"{base_name}{output_extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Convert and save
    try:
        # Convert RGBA to RGB if saving as JPEG (JPEG doesn't support transparency)
        if args.format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
            print(f"Converting {img.mode} to RGB for JPEG format...")
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = rgb_img

        # Save the image in the specified format
        save_kwargs = {}
        if args.format == 'JPEG':
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True
        elif args.format == 'WEBP':
            save_kwargs['quality'] = 90

        img.save(output_path, format=args.format, **save_kwargs)
        print(f"Successfully converted image to {args.format}")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error saving image: {e}")
        sys.exit(1)

    print("\nImage format conversion completed!")


if __name__ == "__main__":
    main()