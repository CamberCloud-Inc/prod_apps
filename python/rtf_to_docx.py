import subprocess
import sys
import os
import argparse

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "pypandoc"])

import pypandoc


def main():
    parser = argparse.ArgumentParser(description='Convert RTF to Word (DOCX) documents')
    parser.add_argument('rtf_path', help='Path to the RTF file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for DOCX file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received rtf_path argument: {args.rtf_path}")

    # Expand user path if provided
    rtf_path = os.path.expanduser(args.rtf_path)
    print(f"Expanded rtf_path: {rtf_path}")

    if not os.path.exists(rtf_path):
        print(f"Error: RTF file not found at: {rtf_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(rtf_path))[0]
    output_path = os.path.join(args.output_dir, f"{base_name}.docx")

    # Ensure pandoc is installed
    print("Ensuring pandoc is installed...")
    try:
        # Try to download pandoc if not available
        pypandoc.download_pandoc()
    except:
        # If already installed or download fails, continue
        pass

    # Convert RTF to DOCX
    print(f"Converting RTF to DOCX: {rtf_path} -> {output_path}")
    try:
        pypandoc.convert_file(
            rtf_path,
            'docx',
            outputfile=output_path,
            format='rtf'
        )
        print(f"RTF to DOCX conversion completed! Output: {output_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()