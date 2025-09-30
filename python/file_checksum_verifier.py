import hashlib
import sys
import os
import argparse


def calculate_hash(file_path, algorithm='sha256'):
    """Calculate hash for a file using specified algorithm."""
    if algorithm == 'md5':
        hash_obj = hashlib.md5()
    elif algorithm == 'sha1':
        hash_obj = hashlib.sha1()
    elif algorithm == 'sha256':
        hash_obj = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    chunk_size = 8192
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hash_obj.update(chunk)

    return hash_obj.hexdigest()


def verify_checksum(file_path, expected_checksum, output_dir):
    """Verify file integrity by comparing checksums."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    print(f"Verifying checksum for: {file_name}")
    print(f"File size: {file_size:,} bytes")
    print(f"Expected checksum: {expected_checksum}")

    # Detect hash algorithm based on checksum length
    checksum_len = len(expected_checksum)
    if checksum_len == 32:
        algorithm = 'md5'
        algo_name = 'MD5'
    elif checksum_len == 40:
        algorithm = 'sha1'
        algo_name = 'SHA1'
    elif checksum_len == 64:
        algorithm = 'sha256'
        algo_name = 'SHA256'
    else:
        print(f"Error: Unable to detect hash algorithm from checksum length ({checksum_len} characters)")
        print("Expected: 32 (MD5), 40 (SHA1), or 64 (SHA256)")
        sys.exit(1)

    print(f"Detected algorithm: {algo_name}")

    # Calculate actual checksum
    print(f"Calculating {algo_name} hash...")
    actual_checksum = calculate_hash(file_path, algorithm)
    print(f"Actual checksum:   {actual_checksum}")

    # Compare checksums
    match = actual_checksum.lower() == expected_checksum.lower()

    # Write results to output file
    output_file = os.path.join(output_dir, f"{file_name}_verification.txt")
    with open(output_file, 'w') as f:
        f.write(f"File: {file_name}\n")
        f.write(f"Size: {file_size:,} bytes\n")
        f.write(f"Algorithm: {algo_name}\n")
        f.write(f"\n")
        f.write(f"Expected checksum: {expected_checksum}\n")
        f.write(f"Actual checksum:   {actual_checksum}\n")
        f.write(f"\n")
        f.write(f"Verification: {'PASSED' if match else 'FAILED'}\n")
        if match:
            f.write(f"Status: File integrity verified successfully!\n")
        else:
            f.write(f"Status: WARNING - Checksums do not match! File may be corrupted or modified.\n")

    # Print results
    print(f"\n{'='*60}")
    if match:
        print("VERIFICATION PASSED")
        print("File integrity verified successfully!")
    else:
        print("VERIFICATION FAILED")
        print("WARNING: Checksums do not match!")
        print("The file may be corrupted or has been modified.")
    print(f"{'='*60}")

    print(f"\nResults saved to: {output_file}")

    return match


def main():
    parser = argparse.ArgumentParser(description='Verify file integrity using checksums')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('checksum', help='Expected checksum (MD5, SHA1, or SHA256)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for verification results (default: ./)')

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

    # Verify checksum
    match = verify_checksum(input_path, args.checksum, args.output_dir)

    print("\nChecksum verification completed!")

    # Exit with appropriate code
    sys.exit(0 if match else 1)


if __name__ == "__main__":
    main()