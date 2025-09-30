import hashlib
import sys
import os
import argparse


def calculate_hashes(file_path):
    """Calculate MD5, SHA1, and SHA256 hashes for a file."""
    md5_hash = hashlib.md5()
    sha1_hash = hashlib.sha1()
    sha256_hash = hashlib.sha256()

    # Read file in chunks to handle large files
    chunk_size = 8192
    file_size = os.path.getsize(file_path)
    bytes_read = 0

    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            md5_hash.update(chunk)
            sha1_hash.update(chunk)
            sha256_hash.update(chunk)
            bytes_read += len(chunk)

            # Print progress for large files
            if file_size > 1024 * 1024:  # > 1 MB
                progress = (bytes_read / file_size) * 100
                print(f"Progress: {progress:.1f}%", end='\r')

    if file_size > 1024 * 1024:
        print()  # New line after progress

    return {
        'md5': md5_hash.hexdigest(),
        'sha1': sha1_hash.hexdigest(),
        'sha256': sha256_hash.hexdigest()
    }


def main():
    parser = argparse.ArgumentParser(description='Generate MD5, SHA1, and SHA256 hashes for files')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for hash results (default: ./)')

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

    # Get file info
    file_name = os.path.basename(input_path)
    file_size = os.path.getsize(input_path)
    print(f"\nCalculating hashes for: {file_name}")
    print(f"File size: {file_size:,} bytes")

    # Calculate hashes
    print("Calculating hashes...")
    hashes = calculate_hashes(input_path)

    # Write results to output file
    output_file = os.path.join(args.output_dir, f"{file_name}_hashes.txt")
    with open(output_file, 'w') as f:
        f.write(f"File: {file_name}\n")
        f.write(f"Size: {file_size:,} bytes\n")
        f.write(f"\n")
        f.write(f"MD5:    {hashes['md5']}\n")
        f.write(f"SHA1:   {hashes['sha1']}\n")
        f.write(f"SHA256: {hashes['sha256']}\n")

    # Print results to console
    print(f"\nHash Results:")
    print(f"MD5:    {hashes['md5']}")
    print(f"SHA1:   {hashes['sha1']}")
    print(f"SHA256: {hashes['sha256']}")
    print(f"\nResults saved to: {output_file}")
    print("Hash generation completed!")


if __name__ == "__main__":
    main()