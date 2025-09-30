import subprocess
import sys
import os
import argparse

# Install Pillow and colorthief
subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "colorthief"])

from PIL import Image, ImageDraw, ImageFont
from colorthief import ColorThief


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code"""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])


def create_palette_image(colors, palette_width=800, palette_height=400):
    """Create a visual representation of the color palette"""
    num_colors = len(colors)
    color_width = palette_width // num_colors

    # Create image
    palette_img = Image.new('RGB', (palette_width, palette_height), color='white')
    draw = ImageDraw.Draw(palette_img)

    # Draw color swatches
    for i, color in enumerate(colors):
        x1 = i * color_width
        x2 = (i + 1) * color_width
        y1 = 0
        y2 = palette_height - 80  # Leave space for text

        # Draw color rectangle
        draw.rectangle([x1, y1, x2, y2], fill=color)

        # Draw hex code text
        hex_code = rgb_to_hex(color)
        rgb_text = f"RGB{color}"

        # Calculate text position (center of swatch)
        text_x = x1 + color_width // 2
        text_y = palette_height - 60

        # Draw text background for readability
        draw.rectangle([x1, y2, x2, palette_height], fill='white')

        # Draw hex code
        try:
            # Try to use a font
            font = ImageFont.load_default()
        except:
            font = None

        # Calculate text bbox for centering
        if font:
            bbox = draw.textbbox((0, 0), hex_code, font=font)
            text_width = bbox[2] - bbox[0]
        else:
            text_width = len(hex_code) * 6  # Approximate

        text_x = x1 + (color_width - text_width) // 2

        draw.text((text_x, text_y), hex_code, fill='black', font=font)
        draw.text((text_x, text_y + 20), rgb_text, fill='black', font=font)

    return palette_img


def main():
    parser = argparse.ArgumentParser(description='Extract dominant colors from an image')
    parser.add_argument('input_file', help='Path to the input image file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for palette (default: ./)')
    parser.add_argument('-n', '--num-colors', type=int, default=6,
                        help='Number of colors to extract (default: 6)')

    args = parser.parse_args()

    # Validate num_colors
    if args.num_colors < 2 or args.num_colors > 10:
        print(f"Error: Number of colors must be between 2 and 10. You provided {args.num_colors}.")
        sys.exit(1)

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")
    print(f"Extracting {args.num_colors} colors")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: Image file not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Open the image for display info
    try:
        img = Image.open(input_file)
        print(f"Successfully opened image: {input_file}")
        print(f"Image size: {img.size}, Mode: {img.mode}")
    except Exception as e:
        print(f"Error opening image: {e}")
        sys.exit(1)

    # Extract color palette using ColorThief
    try:
        print(f"\nExtracting {args.num_colors} dominant colors...")

        color_thief = ColorThief(input_file)

        # Get the palette
        palette = color_thief.get_palette(color_count=args.num_colors, quality=1)

        print(f"Successfully extracted {len(palette)} colors:")
        for i, color in enumerate(palette, 1):
            hex_code = rgb_to_hex(color)
            print(f"  {i}. RGB{color} - {hex_code}")

        # Create visual palette
        print("\nCreating palette visualization...")
        palette_img = create_palette_image(palette)

        # Save palette image
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_filename = f"{base_name}_palette_{args.num_colors}_colors.png"
        output_path = os.path.join(args.output_dir, output_filename)

        palette_img.save(output_path, format='PNG', optimize=True)
        print(f"Palette image saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

        # Also save color data to text file
        text_filename = f"{base_name}_palette_{args.num_colors}_colors.txt"
        text_path = os.path.join(args.output_dir, text_filename)

        with open(text_path, 'w') as f:
            f.write(f"Color Palette extracted from: {os.path.basename(input_file)}\n")
            f.write(f"Number of colors: {args.num_colors}\n\n")
            for i, color in enumerate(palette, 1):
                hex_code = rgb_to_hex(color)
                f.write(f"Color {i}:\n")
                f.write(f"  RGB: {color}\n")
                f.write(f"  Hex: {hex_code}\n\n")

        print(f"Color data saved to: {text_path}")

    except Exception as e:
        print(f"Error extracting colors: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nColor palette extraction completed!")


if __name__ == "__main__":
    main()