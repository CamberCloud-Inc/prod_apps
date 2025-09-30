import sys
import os
import argparse
import glob


def main():
    parser = argparse.ArgumentParser(description='Combine multiple text files into one')
    parser.add_argument('input_pattern', help='Path pattern for input files (e.g., "files/*.txt" or directory path)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for merged file (default: ./)')
    parser.add_argument('-n', '--output-name', default='merged.txt',
                        help='Output filename (default: merged.txt)')
    parser.add_argument('-s', '--separator', default='',
                        help='Separator between files (default: none)')
    parser.add_argument('-H', '--headers', action='store_true',
                        help='Add filename headers before each file content')

    args = parser.parse_args()

    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_pattern argument: {args.input_pattern}")

    # Expand user path if provided
    input_pattern = os.path.expanduser(args.input_pattern)
    print(f"Expanded input_pattern: {input_pattern}")

    # Check if input is a directory
    if os.path.isdir(input_pattern):
        # If directory, use all .txt files in it
        search_pattern = os.path.join(input_pattern, "*.txt")
        print(f"Input is a directory, searching for: {search_pattern}")
        input_files = glob.glob(search_pattern)
    else:
        # Use the pattern directly
        input_files = glob.glob(input_pattern)

    # Sort files for consistent ordering
    input_files.sort()

    if not input_files:
        print(f"Error: No files found matching pattern: {input_pattern}")
        print("Please check:")
        print("  - The path/pattern is correct")
        print("  - Files exist at the specified location")
        print("  - For directories, ensure .txt files are present")
        sys.exit(1)

    print(f"\nFound {len(input_files)} files to merge:")
    for f in input_files:
        file_size = os.path.getsize(f)
        print(f"  - {os.path.basename(f)} ({file_size} bytes)")

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    output_path = os.path.join(args.output_dir, args.output_name)

    # Merge files
    print(f"\nMerging files into: {output_path}")
    total_lines = 0
    total_bytes = 0

    try:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for i, input_file in enumerate(input_files):
                print(f"Processing {i+1}/{len(input_files)}: {os.path.basename(input_file)}")

                # Add header if requested
                if args.headers:
                    header = f"\n{'='*60}\n"
                    header += f"File: {os.path.basename(input_file)}\n"
                    header += f"{'='*60}\n\n"
                    outfile.write(header)
                    total_bytes += len(header)

                # Read and write file content
                try:
                    with open(input_file, 'r', encoding='utf-8') as infile:
                        content = infile.read()
                        lines_in_file = content.count('\n')
                        outfile.write(content)
                        total_lines += lines_in_file
                        total_bytes += len(content)

                    # Add separator if not the last file and separator is specified
                    if i < len(input_files) - 1 and args.separator:
                        separator_text = args.separator.replace('\\n', '\n')
                        outfile.write(separator_text)
                        total_bytes += len(separator_text)

                except Exception as e:
                    print(f"Warning: Error reading file {input_file}: {e}")
                    continue

    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)

    print(f"\nMerge completed successfully!")
    print(f"Merged {len(input_files)} files")
    print(f"Total lines: {total_lines}")
    print(f"Total size: {total_bytes} bytes ({total_bytes / 1024:.2f} KB)")
    print(f"Output saved to: {output_path}")


if __name__ == "__main__":
    main()