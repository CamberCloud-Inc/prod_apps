import sys
import os
import argparse
import re


def merge_chunks(chunk_pattern, output_file):
    """Merge file chunks back together."""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Chunk pattern: {chunk_pattern}")
    print(f"Output file: {output_file}")

    # Find all chunk files matching the pattern
    directory = os.path.dirname(chunk_pattern) or './'
    base_pattern = os.path.basename(chunk_pattern)

    # Escape special regex characters except for *
    regex_pattern = re.escape(base_pattern).replace(r'\*', '.*')
    regex_pattern = f"^{regex_pattern}$"

    print(f"\nSearching for chunks in: {directory}")
    print(f"Pattern: {base_pattern}")

    try:
        # Find all matching chunk files
        all_files = os.listdir(directory)
        chunk_files = [f for f in all_files if re.match(regex_pattern, f)]

        if not chunk_files:
            print(f"Error: No chunk files found matching pattern: {base_pattern}")
            sys.exit(1)

        # Sort chunk files to ensure correct order
        chunk_files.sort()

        print(f"\nFound {len(chunk_files)} chunk(s):")
        for chunk in chunk_files:
            chunk_path = os.path.join(directory, chunk)
            chunk_size = os.path.getsize(chunk_path)
            print(f"  - {chunk} ({chunk_size:,} bytes)")

        # Merge chunks
        total_bytes = 0
        print(f"\nMerging chunks to: {output_file}")

        with open(output_file, 'wb') as outfile:
            for chunk_num, chunk_file in enumerate(chunk_files, 1):
                chunk_path = os.path.join(directory, chunk_file)

                print(f"Processing chunk {chunk_num}/{len(chunk_files)}: {chunk_file}")

                with open(chunk_path, 'rb') as infile:
                    chunk_data = infile.read()
                    outfile.write(chunk_data)
                    total_bytes += len(chunk_data)

        print(f"\nFile merging complete!")
        print(f"Merged {len(chunk_files)} chunk(s)")
        print(f"Output file: {output_file}")
        print(f"Total size: {total_bytes:,} bytes ({total_bytes / (1024**2):.2f} MB)")

    except Exception as e:
        print(f"Error: Failed to merge chunks: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='Merge file chunks back together',
        epilog='Example: file_merger.py "myfile.txt.part*" -o myfile.txt'
    )
    parser.add_argument('chunk_pattern', help='Pattern matching chunk files (e.g., "file.part*")')
    parser.add_argument('-o', '--output', required=True,
                        help='Output file name for merged file')

    args = parser.parse_args()

    # Expand user path if provided
    chunk_pattern = os.path.expanduser(args.chunk_pattern)

    # Create output directory if needed
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Merge chunks
    merge_chunks(chunk_pattern, args.output)

    print("\nFile merging completed!")


if __name__ == "__main__":
    main()