import subprocess
import sys
import os
import argparse

# Install fonttools
subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "fonttools", "brotli"])

from fontTools.ttLib import TTFont


def main():
    parser = argparse.ArgumentParser(description='Convert between TTF/OTF/WOFF/WOFF2 font formats')
    parser.add_argument('input_file', help='Path to the input font file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for converted font (default: ./)')
    parser.add_argument('-f', '--format', choices=['TTF', 'OTF', 'WOFF', 'WOFF2'], default='WOFF',
                        help='Output format (default: WOFF)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Expanded input_file: {input_file}")
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: Font file not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Open the font
    try:
        font = TTFont(input_file)
        print(f"Successfully opened font: {input_file}")
        print(f"Font contains {len(font.getGlyphOrder())} glyphs")
    except Exception as e:
        print(f"Error opening font: {e}")
        sys.exit(1)

    # Get the base filename without extension
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    # Determine output file extension
    extension_map = {
        'TTF': '.ttf',
        'OTF': '.otf',
        'WOFF': '.woff',
        'WOFF2': '.woff2'
    }
    output_extension = extension_map[args.format]
    output_filename = f"{base_name}{output_extension}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Convert and save
    try:
        # Determine flavor for WOFF/WOFF2
        flavor = None
        if args.format == 'WOFF':
            flavor = 'woff'
        elif args.format == 'WOFF2':
            flavor = 'woff2'

        # Save the font in the specified format
        font.flavor = flavor
        font.save(output_path)
        print(f"Successfully converted font to {args.format}")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")
    except Exception as e:
        print(f"Error saving font: {e}")
        sys.exit(1)
    finally:
        font.close()

    print("\nFont conversion completed!")


if __name__ == "__main__":
    main()