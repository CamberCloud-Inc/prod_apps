import tarfile
import sys
import os
import argparse


def create_tar_gz(input_path, output_file):
    """Create a compressed tar.gz archive from files or folders."""
    print(f"Current working directory: {os.getcwd()}")
    print(f"Input path: {input_path}")
    print(f"Output file: {output_file}")

    # Check if input exists
    if not os.path.exists(input_path):
        print(f"Error: Input path not found: {input_path}")
        sys.exit(1)

    try:
        # Create tar.gz file
        with tarfile.open(output_file, 'w:gz') as tar:
            if os.path.isfile(input_path):
                # Single file compression
                print(f"\nCompressing file: {os.path.basename(input_path)}")
                file_size = os.path.getsize(input_path)
                print(f"Original size: {file_size:,} bytes")

                arcname = os.path.basename(input_path)
                tar.add(input_path, arcname=arcname)

                num_files = 1
                total_size = file_size
            else:
                # Directory compression
                print(f"\nCompressing directory: {input_path}")
                num_files = 0
                total_size = 0

                for root, dirs, files in os.walk(input_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(input_path))

                        print(f"  Adding: {arcname}")
                        tar.add(file_path, arcname=arcname)

                        total_size += os.path.getsize(file_path)
                        num_files += 1

                print(f"\nTotal original size: {total_size:,} bytes")

        # Get compressed size
        compressed_size = os.path.getsize(output_file)

        print(f"\nCompression complete!")
        print(f"Files compressed: {num_files}")
        print(f"Compressed size: {compressed_size:,} bytes")

        if total_size > 0:
            compression_ratio = (1 - compressed_size / total_size) * 100
            print(f"Compression ratio: {compression_ratio:.1f}%")
            print(f"Space saved: {total_size - compressed_size:,} bytes")

    except Exception as e:
        print(f"Error: Failed to create tar.gz archive: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Create compressed tar.gz archives')
    parser.add_argument('input_path', help='Path to file or folder to compress')
    parser.add_argument('-o', '--output', default='archive.tar.gz',
                        help='Output tar.gz file name (default: archive.tar.gz)')

    args = parser.parse_args()

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_path)

    # Create output directory if needed
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # Create tar.gz archive
    create_tar_gz(input_path, args.output)

    print("\ntar.gz creation completed!")


if __name__ == "__main__":
    main()