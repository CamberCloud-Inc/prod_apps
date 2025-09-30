import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image, ImageEnhance


def main():
    parser = argparse.ArgumentParser(description='Adjust image brightness and contrast')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for adjusted image (default: ./)')
    parser.add_argument('-b', '--brightness', type=float, default=1.2,
                        help='Brightness factor (1.0=original, <1.0=darker, >1.0=brighter) (default: 1.2)')
    parser.add_argument('-c', '--contrast', type=float, default=1.1,
                        help='Contrast factor (1.0=original, <1.0=less contrast, >1.0=more contrast) (default: 1.1)')

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
        print(f"Size: {img.size}, Mode: {img.mode}")
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Get the base filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    extension = os.path.splitext(input_file)[1]

    output_filename = f"{base_name}_adjusted{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Apply brightness and contrast adjustments
    try:
        print(f"Adjusting brightness (factor: {args.brightness})")
        enhancer = ImageEnhance.Brightness(img)
        adjusted_img = enhancer.enhance(args.brightness)

        print(f"Adjusting contrast (factor: {args.contrast})")
        enhancer = ImageEnhance.Contrast(adjusted_img)
        adjusted_img = enhancer.enhance(args.contrast)

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        adjusted_img.save(output_path, **save_kwargs)
        print(f"Successfully adjusted brightness and contrast")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error adjusting image: {e}")
        sys.exit(1)

    print("\nImage adjustment completed!")


if __name__ == "__main__":
    main()