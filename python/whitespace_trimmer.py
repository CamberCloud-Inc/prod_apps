import argparse
import os
import sys


def main():
    parser = argparse.ArgumentParser(description='Remove trailing/leading whitespace from text files')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for trimmed text (default: ./)')
    parser.add_argument('-l', '--leading', action='store_true',
                        help='Remove only leading whitespace')
    parser.add_argument('-t', '--trailing', action='store_true',
                        help='Remove only trailing whitespace')
    parser.add_argument('-e', '--empty-lines', action='store_true',
                        help='Also remove empty lines')

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

    # Process lines based on options
    if args.leading and not args.trailing:
        print("Removing leading whitespace only...")
        processed_lines = [line.lstrip() for line in lines]
    elif args.trailing and not args.leading:
        print("Removing trailing whitespace only...")
        processed_lines = [line.rstrip() + '\n' if line.endswith('\n') else line.rstrip() for line in lines]
    else:
        print("Removing both leading and trailing whitespace...")
        processed_lines = [line.strip() + '\n' if line.endswith('\n') else line.strip() for line in lines]

    # Remove empty lines if requested
    if args.empty_lines:
        print("Removing empty lines...")
        original_count = len(processed_lines)
        processed_lines = [line for line in processed_lines if line.strip()]
        removed_count = original_count - len(processed_lines)
        print(f"Removed {removed_count} empty lines")

    # Calculate statistics
    original_size = sum(len(line) for line in lines)
    processed_size = sum(len(line) for line in processed_lines)
    whitespace_removed = original_size - processed_size

    print(f"Original size: {original_size} characters")
    print(f"Processed size: {processed_size} characters")
    print(f"Whitespace removed: {whitespace_removed} characters")

    # Generate output filename
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    output_filename = f"{name_without_ext}_trimmed.txt"
    output_path = os.path.join(args.output_dir, output_filename)

    # Write the output file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(processed_lines)
        print(f"Successfully trimmed whitespace")
        print(f"Output saved to: {output_path}")
        print(f"Original lines: {len(lines)}")
        print(f"Output lines: {len(processed_lines)}")
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print("Whitespace trimming completed!")


if __name__ == "__main__":
    main()
