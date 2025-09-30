import subprocess
import sys
import os
import argparse

# Install Pillow
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser(description='Add text watermarks to images')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for watermarked image (default: ./)')

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

        # Convert to RGBA if not already (for transparency support)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Get the base filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    extension = os.path.splitext(input_file)[1]

    output_filename = f"{base_name}_watermarked{extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Add watermark
    try:
        # Create a transparent overlay
        watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark)

        # Watermark text
        text = "© WATERMARK"

        # Calculate font size based on image dimensions (roughly 1/20 of width)
        font_size = max(20, img.size[0] // 20)

        # Try to use a default font, fallback to PIL default if not available
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                # Use default PIL font
                font = ImageFont.load_default()
                print("Using default font (system fonts not found)")

        # Get text bounding box for positioning
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position text at bottom-right with some padding
        padding = 20
        x = img.size[0] - text_width - padding
        y = img.size[1] - text_height - padding

        # Draw text with semi-transparent white color
        draw.text((x, y), text, fill=(255, 255, 255, 180), font=font)

        # Composite the watermark onto the original image
        watermarked = Image.alpha_composite(img, watermark)

        print(f"Successfully added watermark: '{text}'")
        print(f"Watermark position: bottom-right corner")

        # Convert back to original mode if needed for saving
        if extension.lower() in ['.jpg', '.jpeg']:
            # Convert RGBA to RGB for JPEG
            rgb_img = Image.new('RGB', watermarked.size, (255, 255, 255))
            rgb_img.paste(watermarked, mask=watermarked.split()[3])
            watermarked = rgb_img

        # Save with appropriate quality settings
        save_kwargs = {}
        if extension.lower() in ['.jpg', '.jpeg']:
            save_kwargs['quality'] = 95
            save_kwargs['optimize'] = True

        watermarked.save(output_path, **save_kwargs)
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error adding watermark: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nImage watermarking completed!")


if __name__ == "__main__":
    main()