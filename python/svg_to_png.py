import subprocess
import sys
import os
import argparse

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "cairosvg"])

import cairosvg


def main():
    parser = argparse.ArgumentParser(description='Convert vector SVG files to raster PNG images')
    parser.add_argument('input_file', help='Path to the input SVG file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for PNG file (default: ./)')
    parser.add_argument('-w', '--width', type=int, default=None,
                        help='Output width in pixels (maintains aspect ratio if only width specified)')
    parser.add_argument('-H', '--height', type=int, default=None,
                        help='Output height in pixels (maintains aspect ratio if only height specified)')
    parser.add_argument('-s', '--scale', type=float, default=1.0,
                        help='Scale factor for output (default: 1.0)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: SVG file not found at: {input_file}")
        sys.exit(1)

    # Validate file extension
    ext = os.path.splitext(input_file)[1].lower()
    if ext != '.svg':
        print(f"Warning: File extension is {ext}, expected .svg")
        print("Attempting conversion anyway...")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Get the base filename
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_filename = f"{base_name}.png"
    output_path = os.path.join(args.output_dir, output_filename)

    # Prepare conversion parameters
    convert_kwargs = {}

    if args.width:
        convert_kwargs['output_width'] = args.width
        print(f"Output width set to: {args.width}px")

    if args.height:
        convert_kwargs['output_height'] = args.height
        print(f"Output height set to: {args.height}px")

    if args.scale != 1.0:
        convert_kwargs['scale'] = args.scale
        print(f"Scale factor set to: {args.scale}")

    # Convert SVG to PNG
    try:
        print(f"Converting SVG to PNG...")

        cairosvg.svg2png(
            url=input_file,
            write_to=output_path,
            **convert_kwargs
        )

        print(f"Successfully converted to PNG")
        print(f"Output saved to: {output_path}")
        print(f"Output file size: {os.path.getsize(output_path)} bytes")

    except Exception as e:
        print(f"Error converting SVG to PNG: {e}")
        print("\nTroubleshooting:")
        print("- Ensure the file is a valid SVG file")
        print("- Check that the SVG doesn't have syntax errors")
        print("- Some complex SVG features may not be fully supported")
        sys.exit(1)

    print("\nSVG to PNG conversion completed!")


if __name__ == "__main__":
    main()