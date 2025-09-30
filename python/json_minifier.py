import json
import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Minify JSON files by removing whitespace')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for minified JSON (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nReading JSON file: {input_path}")

    # Read and parse JSON
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("JSON validation: PASSED")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Get original file size
    original_size = os.path.getsize(input_path)

    # Generate output filename
    input_filename = os.path.basename(input_path)
    base_name = os.path.splitext(input_filename)[0]
    output_filename = f"{base_name}_minified.json"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write minified JSON
    print(f"\nMinifying JSON (removing whitespace)...")
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, separators=(',', ':'), ensure_ascii=False)
        print(f"Minified JSON saved to: {output_path}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    # Get minified file size
    minified_size = os.path.getsize(output_path)
    reduction = ((original_size - minified_size) / original_size) * 100 if original_size > 0 else 0

    print(f"\nOriginal size: {original_size} bytes")
    print(f"Minified size: {minified_size} bytes")
    print(f"Size reduction: {reduction:.1f}%")
    print("\nJSON minification completed successfully!")


if __name__ == "__main__":
    main()