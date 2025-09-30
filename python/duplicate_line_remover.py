import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='Remove duplicate lines from text files')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for cleaned text (default: ./)')
    parser.add_argument('-i', '--case-insensitive', action='store_true',
                        help='Ignore case when comparing lines')
    parser.add_argument('-k', '--keep-order', action='store_true',
                        help='Keep original order (default: keep first occurrence)')

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

    print(f"Read {len(lines)} lines from input file")

    # Remove duplicates
    print(f"Removing duplicates ({'case-insensitive' if args.case_insensitive else 'case-sensitive'})...")
    
    seen = set()
    unique_lines = []
    
    for line in lines:
        # Use lowercase version for comparison if case-insensitive
        compare_line = line.lower() if args.case_insensitive else line
        
        if compare_line not in seen:
            seen.add(compare_line)
            unique_lines.append(line)

    duplicates_removed = len(lines) - len(unique_lines)
    print(f"Removed {duplicates_removed} duplicate lines")

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{name_without_ext}_unique.txt"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(unique_lines)
        print(f"Successfully removed duplicates")
        print(f"Output saved to: {output_path}")
        print(f"Original lines: {len(lines)}")
        print(f"Unique lines: {len(unique_lines)}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("Duplicate removal completed!")


if __name__ == "__main__":
    main()
