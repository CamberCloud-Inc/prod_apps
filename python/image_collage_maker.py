import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Combine images into a 2x2 grid collage')
    parser.add_argument('input_files', nargs='+', help='Paths to 2-4 input image files')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for collage (default: ./)')
    parser.add_argument('-s', '--size', type=int, default=800,
                        help='Size of each cell in pixels (default: 800)')

    args = parser.parse_args()

    # Validate number of images
    if len(args.input_files) < 2 or len(args.input_files) > 4:
        print(f"Error: Please provide 2-4 images. You provided {len(args.input_files)}.")
        sys.exit(1)

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received {len(args.input_files)} images for collage")
    print(f"Cell size: {args.size}x{args.size}")

    # Expand and validate all input files
    images = []
    for i, input_file in enumerate(args.input_files):
        expanded_path = os.path.expanduser(input_file)
        print(f"Image {i+1}: {input_file}")

        if not os.path.exists(expanded_path):
            print(f"Error: Image file not found at: {expanded_path}")
            sys.exit(1)

        try:
            img = Image.open(expanded_path)
            print(f"  Opened successfully: {img.size}, Mode: {img.mode}")
            images.append(img)
        except Exception as e:
            print(f"Error opening image {expanded_path}: {e}")
            sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Create 2x2 collage
    try:
        cell_size = args.size
        collage_width = cell_size * 2
        collage_height = cell_size * 2

        print(f"\nCreating 2x2 collage: {collage_width}x{collage_height}")

        # Create blank collage with white background
        collage = Image.new('RGB', (collage_width, collage_height), color='white')

        # Define positions for 2x2 grid
        positions = [
            (0, 0),              # Top-left
            (cell_size, 0),      # Top-right
            (0, cell_size),      # Bottom-left
            (cell_size, cell_size)  # Bottom-right
        ]

        # Process and paste each image
        for i, img in enumerate(images):
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Resize to fit cell while maintaining aspect ratio
            img.thumbnail((cell_size, cell_size), Image.Resampling.LANCZOS)

            # Calculate position to center image in cell
            x, y = positions[i]
            x_offset = x + (cell_size - img.width) // 2
            y_offset = y + (cell_size - img.height) // 2

            collage.paste(img, (x_offset, y_offset))
            print(f"  Placed image {i+1} at grid position ({i % 2}, {i // 2})")

        # Save the collage
        output_filename = f"collage_2x2_{len(images)}_images.jpg"
        output_path = os.path.join(args.output_dir, output_filename)

        collage.save(output_path, quality=95, optimize=True)
        print(f"\nSuccessfully created collage with {len(images)} images")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

    except Exception as e:
        print(f"Error creating collage: {e}")
        sys.exit(1)

    # Close all images
    for img in images:
        img.close()

    print("\nCollage creation completed!")


if __name__ == "__main__":
    main()