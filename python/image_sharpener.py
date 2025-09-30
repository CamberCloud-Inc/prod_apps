import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image, ImageFilter


def main():
    parser = argparse.ArgumentParser(description='Enhance image sharpness')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for sharpened image (default: ./)')
    parser.add_argument('-i', '--intensity', type=int, default=1,
                        help='Number of times to apply sharpen filter (default: 1)')

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

    output_filename = f"{base_name}_sharpened{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Apply sharpen effect
    try:
        print(f"Applying sharpen filter (intensity: {args.intensity})")
        sharpened_img = img
        for i in range(args.intensity):
            sharpened_img = sharpened_img.filter(ImageFilter.SHARPEN)
            print(f"Applied sharpen filter pass {i+1}/{args.intensity}")

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        sharpened_img.save(output_path, **save_kwargs)
        print(f"Successfully applied sharpen effect")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error applying sharpen: {e}")
        sys.exit(1)

    print("\nImage sharpening completed!")


if __name__ == "__main__":
    main()