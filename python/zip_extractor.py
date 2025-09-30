import zipfile
import sys
import os
import argparse


def extract_zip(zip_path, output_dir):
    """Extract a ZIP archive to the specified directory."""
    file_name = os.path.basename(zip_path)
    file_size = os.path.getsize(zip_path)

    print(f"Extracting ZIP file: {file_name}")
    print(f"ZIP file size: {file_size:,} bytes")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get list of files in the archive
            file_list = zip_ref.namelist()
            num_files = len(file_list)

            print(f"\nArchive contains {num_files} file(s):")
            for file in file_list[:10]:  # Show first 10 files
                print(f"  - {file}")
            if num_files > 10:
                print(f"  ... and {num_files - 10} more files")

            # Extract all files
            print(f"\nExtracting to: {output_dir}")
            zip_ref.extractall(output_dir)

            # Calculate total extracted size
            total_size = 0
            for file in file_list:
                file_path = os.path.join(output_dir, file)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)

            print(f"\nExtraction complete!")
            print(f"Files extracted: {num_files}")
            print(f"Total extracted size: {total_size:,} bytes")
            print(f"Compression ratio: {(1 - file_size / total_size) * 100:.1f}%")

    except zipfile.BadZipFile:
        print(f"Error: File is not a valid ZIP archive")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Failed to extract ZIP file: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description='Extract ZIP archives')
    parser.add_argument('input_file', help='Path to the ZIP file')
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

    # Extract ZIP file
    extract_zip(input_path, args.output_dir)

    print("\nZIP extraction completed!")


if __name__ == "__main__":
    main()