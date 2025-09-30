import tarfile
import sys
import os
import argparse


def extract_tar_gz(tar_path, output_dir):
    """Extract a tar.gz archive to the specified directory."""
    file_name = os.path.basename(tar_path)
    file_size = os.path.getsize(tar_path)

    print(f"Extracting tar.gz file: {file_name}")
    print(f"Archive size: {file_size:,} bytes")

    try:
        with tarfile.open(tar_path, 'r:gz') as tar:
            # Get list of files in the archive
            members = tar.getmembers()
            num_files = len([m for m in members if m.isfile()])

            print(f"\nArchive contains {num_files} file(s):")
            file_members = [m for m in members if m.isfile()][:10]
            for member in file_members:
                print(f"  - {member.name} ({member.size:,} bytes)")
            if num_files > 10:
                print(f"  ... and {num_files - 10} more files")

            # Extract all files
            print(f"\nExtracting to: {output_dir}")
            tar.extractall(output_dir)

            # Calculate total extracted size
            total_size = sum(m.size for m in members if m.isfile())

            print(f"\nExtraction complete!")
            print(f"Files extracted: {num_files}")
            print(f"Total extracted size: {total_size:,} bytes")

            if total_size > 0:
                compression_ratio = (1 - file_size / total_size) * 100
                print(f"Compression ratio: {compression_ratio:.1f}%")

    except tarfile.ReadError:
        print(f"Error: File is not a valid tar.gz archive")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to extract tar.gz file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Extract tar.gz archives')
    parser.add_argument('input_file', help='Path to the tar.gz file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for extracted files (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")

    if not os.path.exists(input_path):
        print(f"Error: File not found at: {input_path}")
        sys.exit(1)

    if not os.path.isfile(input_path):
        print(f"Error: Path is not a file: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Extract tar.gz file
    extract_tar_gz(input_path, args.output_dir)

    print("\ntar.gz extraction completed!")


if __name__ == "__main__":
    main()