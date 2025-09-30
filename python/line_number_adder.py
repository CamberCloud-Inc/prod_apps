import sys
import os
import argparse


def main():
    parser = argparse.ArgumentParser(description='Add line numbers to text files')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for numbered text (default: ./)')
    parser.add_argument('-s', '--start', type=int, default=1,
                        help='Starting line number (default: 1)')
    parser.add_argument('-w', '--width', type=int, default=0,
                        help='Minimum width for line numbers, zero-padded (default: auto)')

    args = parser.parse_args()

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

    # Read the input file
    print(f"Reading input file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print(f"Found {len(lines)} lines in input file")

    # Determine width if not specified
    if args.width == 0:
        max_line_num = args.start + len(lines) - 1
        width = len(str(max_line_num))
    else:
        width = args.width

    # Add line numbers using enumerate
    print(f"Adding line numbers (starting from {args.start}, width: {width})...")
    numbered_lines = []
    for i, line in enumerate(lines, start=args.start):
        # Format line number with specified width
        line_num = str(i).zfill(width)
        # Remove trailing newline if present, we'll add it back
        line_content = line.rstrip('\n\r')
        numbered_line = f"{line_num}: {line_content}\n"
        numbered_lines.append(numbered_line)

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    ext = os.path.splitext(input_filename)[1]
    output_filename = f"{name_without_ext}_numbered{ext}"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(numbered_lines)
        print(f"Successfully added line numbers")
        print(f"Output saved to: {output_path}")
        print(f"Processed {len(numbered_lines)} lines")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("Line numbering completed!")


if __name__ == "__main__":
    main()