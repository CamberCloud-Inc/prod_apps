import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image, ImageOps


def main():
    parser = argparse.ArgumentParser(description='Invert image colors to create negative effect')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for inverted image (default: ./)')

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

    output_filename = f"{base_name}_inverted{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Invert colors
    try:
        # Convert to RGB if needed (ImageOps.invert requires RGB or L mode)
        if img.mode == 'RGBA':
            # For RGBA images, preserve alpha channel
            r, g, b, a = img.split()
            rgb_img = Image.merge('RGB', (r, g, b))
            inverted_rgb = ImageOps.invert(rgb_img)
            inverted_img = Image.merge('RGBA', (*inverted_rgb.split(), a))
        elif img.mode in ['RGB', 'L']:
            inverted_img = ImageOps.invert(img)
        else:
            # Convert other modes to RGB first
            rgb_img = img.convert('RGB')
            inverted_img = ImageOps.invert(rgb_img)

        print(f"Successfully inverted image colors")
        print(f"Created negative effect")

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            # Convert to RGB if RGBA (JPEG doesn't support transparency)
            if inverted_img.mode == 'RGBA':
                rgb_img = Image.new('RGB', inverted_img.size, (255, 255, 255))
                rgb_img.paste(inverted_img, mask=inverted_img.split()[3])
                inverted_img = rgb_img
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        inverted_img.save(output_path, **save_kwargs)
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error inverting colors: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nColor inversion completed!")


if __name__ == "__main__":
    main()