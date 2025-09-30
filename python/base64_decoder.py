import base64
import sys
import os
import argparse


def decode_base64_to_file(encoded_file_path, output_dir):
    """Decode a Base64 file to its original binary form."""
    file_name = os.path.basename(encoded_file_path)

    # Remove .b64 extension if present, otherwise use original name
    if file_name.endswith('.b64'):
        output_name = file_name[:-4]  # Remove .b64
    else:
        output_name = f"{file_name}_decoded"

    print(f"Decoding file: {file_name}")

    # Read base64 encoded content
    with open(encoded_file_path, 'rb') as f:
        encoded_content = f.read()

    encoded_size = len(encoded_content)
    print(f"Encoded size: {encoded_size:,} bytes")

    try:
        # Decode from base64
        decoded_content = base64.b64decode(encoded_content)
    except Exception as e:
        print(f"Error: Failed to decode Base64 content: {e}")
        sys.exit(1)

    # Write decoded content to output file
    output_file = os.path.join(output_dir, output_name)
    with open(output_file, 'wb') as f:
        f.write(decoded_content)

    decoded_size = len(decoded_content)
    print(f"Decoded size: {decoded_size:,} bytes")
    print(f"Size reduction: {((encoded_size - decoded_size) / encoded_size * 100):.1f}%")
    print(f"\nDecoded file saved to: {output_file}")

    return output_file


def main():
    parser = argparse.ArgumentParser(description='Decode Base64 files to original binary format')
    parser.add_argument('input_file', help='Path to the Base64 encoded file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for decoded file (default: ./)')

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

    # Decode file
    decode_base64_to_file(input_path, args.output_dir)

    print("\nBase64 decoding completed!")


if __name__ == "__main__":
    main()