import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='Sort text lines alphabetically or numerically')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for sorted text (default: ./)')
    parser.add_argument('-r', '--reverse', action='store_true',
                        help='Sort in reverse order')
    parser.add_argument('-n', '--numeric', action='store_true',
                        help='Sort numerically instead of alphabetically')
    parser.add_argument('-u', '--unique', action='store_true',
                        help='Remove duplicate lines after sorting')

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

    # Sort the lines
    print(f"Sorting lines ({'numeric' if args.numeric else 'alphabetic'}, {'reverse' if args.reverse else 'forward'})...")
    
    if args.numeric:
        # Try to sort numerically - extract first number from each line
        def get_number(line):
            import re
            match = re.search(r'-?\d+\.?\d*', line)
            if match:
                try:
                    return float(match.group())
                except:
                    return float('inf')
            return float('inf')
        
        sorted_lines = sorted(lines, key=get_number, reverse=args.reverse)
    else:
        # Alphabetic sort (case-insensitive)
        sorted_lines = sorted(lines, key=str.lower, reverse=args.reverse)

    # Remove duplicates if requested
    if args.unique:
        print("Removing duplicate lines...")
        seen = set()
        unique_lines = []
        for line in sorted_lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        sorted_lines = unique_lines
        print(f"Removed {len(lines) - len(sorted_lines)} duplicate lines")

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{name_without_ext}_sorted.txt"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(sorted_lines)
        print(f"Successfully sorted lines")
        print(f"Output saved to: {output_path}")
        print(f"Original lines: {len(lines)}")
        print(f"Output lines: {len(sorted_lines)}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("Line sorting completed!")


if __name__ == "__main__":
    main()
