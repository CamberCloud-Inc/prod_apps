import sys
import os
import argparse
import mimetypes
import struct


def detect_file_type_by_magic(header):
    """Detect file type by magic bytes."""
    if not header:
        return "Empty file"

    # Common magic bytes
    magic_bytes = {
        b'\x89PNG\r\n\x1a\n': 'PNG image',
        b'\xff\xd8\xff': 'JPEG image',
        b'GIF87a': 'GIF image (87a)',
        b'GIF89a': 'GIF image (89a)',
        b'RIFF': 'RIFF container (WebP/WAV/AVI)',
        b'%PDF': 'PDF document',
        b'PK\x03\x04': 'ZIP archive (or Office document)',
        b'PK\x05\x06': 'ZIP archive (empty)',
        b'\x1f\x8b': 'GZIP compressed file',
        b'BM': 'BMP image',
        b'\x00\x00\x01\x00': 'ICO image',
        b'<?xml': 'XML document',
        b'{': 'JSON or JavaScript file',
        b'[': 'JSON array',
        b'#!/': 'Script with shebang',
    }

    for magic, description in magic_bytes.items():
        if header.startswith(magic):
            return description

    # Check if it's text
    try:
        header.decode('utf-8')
        return "Text file (UTF-8)"
    except:
        pass

    try:
        header.decode('ascii')
        return "Text file (ASCII)"
    except:
        pass

    return None


def main():
    parser = argparse.ArgumentParser(description='Identify file types by magic bytes')
    parser.add_argument('input_file', help='Path to the input file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for report (default: ./)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Show detailed information')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_file argument: {args.input_file}")

    # Expand user path if provided
    input_file = os.path.expanduser(args.input_file)
    print(f"Expanded input_file: {input_file}")
    print(f"Absolute input_file: {os.path.abspath(input_file)}")

    if not os.path.exists(input_file):
        print(f"Error: File not found at: {input_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Get file information
    try:
        # Get MIME type from extension
        mime_type, encoding = mimetypes.guess_type(input_file)
        if mime_type is None:
            mime_type = "application/octet-stream"

        # Read first few bytes to detect file type by magic bytes
        with open(input_file, 'rb') as f:
            header = f.read(16)

        # Detect file type by magic bytes
        file_type = detect_file_type_by_magic(header)
        if not file_type:
            file_type = f"Unknown binary file (starts with: {header[:8].hex()})"

        # Try to detect encoding for text files
        if mime_type.startswith('text/') or 'json' in mime_type or 'xml' in mime_type:
            try:
                with open(input_file, 'rb') as f:
                    sample = f.read(4096)
                    # Try UTF-8
                    sample.decode('utf-8')
                    encoding = 'utf-8'
            except:
                encoding = 'binary or unknown'
        else:
            encoding = 'binary'

        print(f"\n{'='*60}")
        print(f"FILE TYPE DETECTION REPORT")
        print(f"{'='*60}")
        print(f"File: {os.path.basename(input_file)}")
        print(f"Path: {input_file}")
        print(f"Size: {os.path.getsize(input_file)} bytes")
        print(f"\n{'='*60}")
        print(f"MIME Type: {mime_type}")
        print(f"Description: {file_type}")
        print(f"Encoding: {encoding}")
        print(f"{'='*60}")

        if args.verbose:
            print(f"\nAdditional Information:")
            print(f"  - File extension: {os.path.splitext(input_file)[1]}")
            print(f"  - Is readable: {os.access(input_file, os.R_OK)}")
            print(f"  - Is writable: {os.access(input_file, os.W_OK)}")
            print(f"  - Is executable: {os.access(input_file, os.X_OK)}")

        # Write report to file
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_filename = f"{base_name}_file_type_report.txt"
        output_path = os.path.join(args.output_dir, output_filename)

        with open(output_path, 'w') as f:
            f.write(f"{'='*60}\n")
            f.write(f"FILE TYPE DETECTION REPORT\n")
            f.write(f"{'='*60}\n")
            f.write(f"File: {os.path.basename(input_file)}\n")
            f.write(f"Path: {input_file}\n")
            f.write(f"Size: {os.path.getsize(input_file)} bytes\n")
            f.write(f"\n{'='*60}\n")
            f.write(f"MIME Type: {mime_type}\n")
            f.write(f"Description: {file_type}\n")
            f.write(f"Encoding: {encoding}\n")
            f.write(f"{'='*60}\n")

            if args.verbose:
                f.write(f"\nAdditional Information:\n")
                f.write(f"  - File extension: {os.path.splitext(input_file)[1]}\n")
                f.write(f"  - Is readable: {os.access(input_file, os.R_OK)}\n")
                f.write(f"  - Is writable: {os.access(input_file, os.W_OK)}\n")
                f.write(f"  - Is executable: {os.access(input_file, os.X_OK)}\n")

        print(f"\nReport saved to: {output_path}")
        print(f"Report file size: {os.path.getsize(output_path)} bytes")

    except Exception as e:
        print(f"Error detecting file type: {e}")
        sys.exit(1)

    print("\nFile type detection completed!")


if __name__ == "__main__":
    main()