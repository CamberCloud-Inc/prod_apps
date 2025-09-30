import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Rotate images by 90/180/270 degrees')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for rotated image (default: ./)')
    parser.add_argument('-r', '--rotation', type=int, choices=[90, 180, 270], default=90,
                        help='Rotation angle in degrees (default: 90)')

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

    output_filename = f"{base_name}_rotated_{args.rotation}{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Rotate the image
    try:
        # Pillow's rotate is counterclockwise, so we negate the angle for clockwise rotation
        # But we want clockwise rotation (standard user expectation)
        # So we use 360 - angle to get clockwise rotation
        # Or better yet, use transpose methods which are faster and lossless

        rotation_methods = {
            90: Image.Transpose.ROTATE_270,   # 90 degrees clockwise = 270 CCW
            180: Image.Transpose.ROTATE_180,
            270: Image.Transpose.ROTATE_90    # 270 degrees clockwise = 90 CCW
        }

        rotated_img = img.transpose(rotation_methods[args.rotation])

        print(f"Rotating image {args.rotation} degrees clockwise")
        print(f"New size: {rotated_img.size}")

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        rotated_img.save(output_path, **save_kwargs)
        print(f"Successfully rotated image")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error rotating image: {e}")
        sys.exit(1)

    print("\nImage rotation completed!")


if __name__ == "__main__":
    main()