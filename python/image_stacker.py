import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Stack multiple images vertically or horizontally')
    parser.add_argument('input_files', nargs='+', help='Paths to 2-4 input image files')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for stacked image (default: ./)')
    parser.add_argument('-d', '--direction', choices=['vertical', 'horizontal'], default='vertical',
                        help='Stack direction (default: vertical)')

    args = parser.parse_args()

    # Validate number of images
    if len(args.input_files) < 2 or len(args.input_files) > 4:
        print(f"Error: Please provide 2-4 images to stack. You provided {len(args.input_files)}.")
        sys.exit(1)

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received {len(args.input_files)} images to stack")
    print(f"Stack direction: {args.direction}")

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

    # Calculate output dimensions
    try:
        if args.direction == 'vertical':
            # Stack vertically: max width, sum of heights
            output_width = max(img.width for img in images)
            output_height = sum(img.height for img in images)
            print(f"Output dimensions: {output_width}x{output_height}")

            # Create new image
            stacked_image = Image.new('RGB', (output_width, output_height))

            # Paste images
            current_y = 0
            for i, img in enumerate(images):
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Center horizontally if image is narrower
                x_offset = (output_width - img.width) // 2
                stacked_image.paste(img, (x_offset, current_y))
                print(f"  Pasted image {i+1} at position ({x_offset}, {current_y})")
                current_y += img.height

        else:  # horizontal
            # Stack horizontally: sum of widths, max height
            output_width = sum(img.width for img in images)
            output_height = max(img.height for img in images)
            print(f"Output dimensions: {output_width}x{output_height}")

            # Create new image
            stacked_image = Image.new('RGB', (output_width, output_height))

            # Paste images
            current_x = 0
            for i, img in enumerate(images):
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Center vertically if image is shorter
                y_offset = (output_height - img.height) // 2
                stacked_image.paste(img, (current_x, y_offset))
                print(f"  Pasted image {i+1} at position ({current_x}, {y_offset})")
                current_x += img.width

        # Save the stacked image
        output_filename = f"stacked_{args.direction}_{len(images)}_images.jpg"
        output_path = os.path.join(args.output_dir, output_filename)

        stacked_image.save(output_path, quality=95, optimize=True)
        print(f"Successfully stacked {len(images)} images")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

    except Exception as e:
        print(f"Error stacking images: {e}")
        sys.exit(1)

    # Close all images
    for img in images:
        img.close()

    print("\nImage stacking completed!")


if __name__ == "__main__":
    main()