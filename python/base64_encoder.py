import base64
import sys
import os
import argparse


def encode_file_to_base64(file_path, output_dir):
    """Encode a file to Base64 string."""
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    print(f"Encoding file: {file_name}")
    print(f"File size: {file_size:,} bytes")

    # Read file and encode to base64
    with open(file_path, 'rb') as f:
        file_content = f.read()
        encoded_content = base64.b64encode(file_content)

    # Write encoded content to output file
    output_file = os.path.join(output_dir, f"{file_name}.b64")
    with open(output_file, 'wb') as f:
        f.write(encoded_content)

    encoded_size = len(encoded_content)
    print(f"\nEncoded size: {encoded_size:,} bytes")
    print(f"Size increase: {((encoded_size - file_size) / file_size * 100):.1f}%")
    print(f"\nEncoded file saved to: {output_file}")

    return output_file


def main():
    parser = argparse.ArgumentParser(description='Encode files to Base64 strings')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for encoded file (default: ./)')

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

    # Encode file
    encode_file_to_base64(input_path, args.output_dir)

    print("\nBase64 encoding completed!")


if __name__ == "__main__":
    main()