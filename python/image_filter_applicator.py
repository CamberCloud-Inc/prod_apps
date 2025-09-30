import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image, ImageEnhance, ImageFilter


def apply_sepia(img):
    """Apply sepia filter to the image"""
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Get pixel data
    pixels = img.load()
    width, height = img.size

    # Apply sepia transformation
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]

            # Sepia formula
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            # Clamp values to 0-255
            pixels[x, y] = (min(255, tr), min(255, tg), min(255, tb))

    return img


def apply_vintage(img):
    """Apply vintage filter to the image"""
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        img = img.convert('RGB')

    # Reduce contrast slightly
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.85)

    # Reduce saturation
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.7)

    # Increase brightness slightly
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)

    # Apply slight vignette effect by darkening edges
    pixels = img.load()
    width, height = img.size
    center_x, center_y = width / 2, height / 2
    max_distance = ((width / 2) ** 2 + (height / 2) ** 2) ** 0.5

    for y in range(height):
        for x in range(width):
            # Calculate distance from center
            distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
            # Normalize distance
            factor = 1 - (distance / max_distance) * 0.4

            r, g, b = pixels[x, y]
            pixels[x, y] = (
                int(r * factor),
                int(g * factor),
                int(b * factor)
            )

    return img


def apply_grayscale(img):
    """Apply grayscale filter"""
    return img.convert('L').convert('RGB')


def apply_blur(img):
    """Apply gaussian blur"""
    return img.filter(ImageFilter.GaussianBlur(radius=3))


def apply_sharpen(img):
    """Apply sharpen filter"""
    return img.filter(ImageFilter.SHARPEN)


def apply_edge_enhance(img):
    """Apply edge enhancement"""
    return img.filter(ImageFilter.EDGE_ENHANCE)


def main():
    parser = argparse.ArgumentParser(description='Apply preset filters to images')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for filtered image (default: ./)')
    parser.add_argument('-f', '--filter', required=True,
                        choices=['sepia', 'vintage', 'grayscale', 'blur', 'sharpen', 'edge-enhance'],
                        help='Filter to apply')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")
    print(f"Filter to apply: {args.filter}")

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

    # Apply the selected filter
    try:
        print(f"\nApplying {args.filter} filter...")

        if args.filter == 'sepia':
            filtered_img = apply_sepia(img.copy())
        elif args.filter == 'vintage':
            filtered_img = apply_vintage(img.copy())
        elif args.filter == 'grayscale':
            filtered_img = apply_grayscale(img.copy())
        elif args.filter == 'blur':
            filtered_img = apply_blur(img.copy())
        elif args.filter == 'sharpen':
            filtered_img = apply_sharpen(img.copy())
        elif args.filter == 'edge-enhance':
            filtered_img = apply_edge_enhance(img.copy())
        else:
            print(f"Error: Unknown filter: {args.filter}")
            sys.exit(1)

        # Get the base filename
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        extension = os.path.splitext(input_file)[1]

        output_filename = f"{base_name}_{args.filter}{extension}"
        output_path = os.path.join(args.output_dir, output_filename)

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        filtered_img.save(output_path, **save_kwargs)
        print(f"Successfully applied {args.filter} filter")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

    except Exception as e:
        print(f"Error applying filter: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nFilter application completed!")


if __name__ == "__main__":
    main()