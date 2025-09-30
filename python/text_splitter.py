import sys
import os
import argparse
import math


def main():
    parser = argparse.ArgumentParser(description='Split large text files by line count or size')
    parser.add_argument('input_file', help='Path to the input text file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for split files (default: ./)')
    parser.add_argument('-l', '--lines', type=int, default=0,
                        help='Split by number of lines per file (default: 0, disabled)')
    parser.add_argument('-s', '--size', type=int, default=0,
                        help='Split by size in KB per file (default: 0, disabled)')
    parser.add_argument('-m', '--mode', default='lines',
                        choices=['lines', 'size'],
                        help='Split mode: by lines or by size (default: lines)')

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

    # Determine split mode and parameters
    if args.mode == 'lines':
        if args.lines <= 0:
            # Default to 1000 lines if not specified
            lines_per_file = 1000
        else:
            lines_per_file = args.lines
        split_by_size = False
        print(f"Split mode: by lines ({lines_per_file} lines per file)")
    else:
        if args.size <= 0:
            # Default to 100KB if not specified
            size_per_file = 100 * 1024  # 100KB in bytes
        else:
            size_per_file = args.size * 1024  # Convert KB to bytes
        split_by_size = True
        print(f"Split mode: by size ({size_per_file / 1024:.1f} KB per file)")

    # Read the input file
    print(f"Reading input file: {input_path}")
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            if split_by_size:
                content = f.read()
            else:
                lines = f.readlines()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    # Generate output filename base
    input_filename = os.path.basename(input_path)
    name_without_ext = os.path.splitext(input_filename)[0]
    ext = os.path.splitext(input_filename)[1]

    if split_by_size:
        # Split by size
        total_size = len(content)
        print(f"File size: {total_size} bytes ({total_size / 1024:.2f} KB)")
        num_files = math.ceil(total_size / size_per_file)
        print(f"Will create approximately {num_files} files")

        file_count = 0
        start_pos = 0

        while start_pos < total_size:
            file_count += 1
            end_pos = min(start_pos + size_per_file, total_size)

            # Extract chunk
            chunk = content[start_pos:end_pos]

            # Write chunk to file
            output_filename = f"{name_without_ext}_part{file_count:03d}{ext}"
            output_path = os.path.join(args.output_dir, output_filename)

            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(chunk)
                print(f"Created: {output_filename} ({len(chunk)} bytes)")
            except Exception as e:
                print(f"Error writing file {output_filename}: {e}")
                sys.exit(1)

            start_pos = end_pos

        print(f"\nSuccessfully split file into {file_count} parts by size")
    else:
        # Split by lines
        total_lines = len(lines)
        print(f"Found {total_lines} lines in input file")
        num_files = math.ceil(total_lines / lines_per_file)
        print(f"Will create {num_files} files")

        file_count = 0

        for i in range(0, total_lines, lines_per_file):
            file_count += 1
            chunk_lines = lines[i:i + lines_per_file]

            # Write chunk to file
            output_filename = f"{name_without_ext}_part{file_count:03d}{ext}"
            output_path = os.path.join(args.output_dir, output_filename)

            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.writelines(chunk_lines)
                print(f"Created: {output_filename} ({len(chunk_lines)} lines)")
            except Exception as e:
                print(f"Error writing file {output_filename}: {e}")
                sys.exit(1)

        print(f"\nSuccessfully split file into {file_count} parts by lines")

    print(f"All split files saved to: {args.output_dir}")
    print("Text splitting completed!")


if __name__ == "__main__":
    main()