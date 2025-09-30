import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Generate favicons in multiple sizes from an image')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for favicons (default: ./)')

    args = parser.parse_args()

    # Define favicon sizes
    sizes = [16, 32, 64]

    # Debug: print current working directory
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

    # Generate favicons in multiple sizes
    print(f"\nGenerating favicons in sizes: {sizes}")

    generated_files = []
    try:
        for size in sizes:
            target_size = (size, size)

            # Convert to RGBA if necessary (for transparency support)
            if img.mode != 'RGBA':
                favicon_img = img.convert('RGBA')
            else:
                favicon_img = img.copy()

            # Resize using high-quality resampling
            favicon_img = favicon_img.resize(target_size, Image.Resampling.LANCZOS)

            # Save as PNG
            output_filename = f"favicon_{size}x{size}.png"
            output_path = os.path.join(args.output_dir, output_filename)

            favicon_img.save(output_path, format='PNG', optimize=True)
            file_size = os.path.getsize(output_path)

            print(f"  Generated {size}x{size}: {output_path} ({file_size} bytes)")
            generated_files.append(output_path)

        # Also generate a standard favicon.ico with multiple sizes
        ico_path = os.path.join(args.output_dir, "favicon.ico")

        # Create images for ICO format (16, 32, 64)
        ico_images = []
        for size in sizes:
            target_size = (size, size)
            if img.mode != 'RGBA':
                ico_img = img.convert('RGBA')
            else:
                ico_img = img.copy()
            ico_img = ico_img.resize(target_size, Image.Resampling.LANCZOS)
            ico_images.append(ico_img)

        # Save as ICO with multiple sizes
        ico_images[0].save(
            ico_path,
            format='ICO',
            sizes=[(s, s) for s in sizes],
            append_images=ico_images[1:]
        )
        ico_size = os.path.getsize(ico_path)
        print(f"  Generated favicon.ico with all sizes: {ico_path} ({ico_size} bytes)")
        generated_files.append(ico_path)

    except Exception as e:
        print(f"Error generating favicons: {e}")
        sys.exit(1)

    print(f"\nSuccessfully generated {len(generated_files)} favicon files")
    print("\nFavicon generation completed!")


if __name__ == "__main__":
    main()