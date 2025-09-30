import sys
import os
import argparse


def split_file(input_file, chunk_size_mb, output_dir):
    """Split a large file into smaller chunks."""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Input file: {input_file}")
    print(f"Chunk size: {chunk_size_mb} MB")
    print(f"Output directory: {output_dir}")

    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    if not os.path.isfile(input_file):
        print(f"Error: Path is not a file: {input_file}")
        sys.exit(1)

    # Get file info
    file_size = os.path.getsize(input_file)
    file_name = os.path.basename(input_file)

    print(f"\nFile to split: {file_name}")
    print(f"File size: {file_size:,} bytes ({file_size / (1024**2):.2f} MB)")

    # Convert chunk size to bytes
    chunk_size = chunk_size_mb * 1024 * 1024

    # Calculate number of chunks
    num_chunks = (file_size + chunk_size - 1) // chunk_size
    print(f"Will create {num_chunks} chunk(s)")

    try:
        with open(input_file, 'rb') as f:
            chunk_num = 0

            while True:
                chunk_data = f.read(chunk_size)
                if not chunk_data:
                    break

                chunk_num += 1
                chunk_filename = f"{file_name}.part{chunk_num:03d}"
                chunk_path = os.path.join(output_dir, chunk_filename)

                print(f"\nCreating chunk {chunk_num}/{num_chunks}: {chunk_filename}")
                print(f"  Chunk size: {len(chunk_data):,} bytes")

                with open(chunk_path, 'wb') as chunk_file:
                    chunk_file.write(chunk_data)

        print(f"\nFile splitting complete!")
        print(f"Created {chunk_num} chunk(s) in: {output_dir}")
        print(f"\nTo merge the chunks back, use the file-merger app with the base filename: {file_name}")

    except Exception as e:
        print(f"Error: Failed to split file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Split large files into smaller chunks')
    parser.add_argument('input_file', help='Path to the file to split')
    parser.add_argument('-s', '--chunk-size', type=int, default=10,
                        help='Chunk size in megabytes (default: 10 MB)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for chunks (default: ./)')

    args = parser.parse_args()

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Validate chunk size
    if args.chunk_size <= 0:
        print(f"Error: Chunk size must be positive")
        sys.exit(1)

    # Split file
    split_file(input_path, args.chunk_size, args.output_dir)

    print("\nFile splitting completed!")


if __name__ == "__main__":
    main()