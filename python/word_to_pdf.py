import subprocess
import sys
import os
import argparse

# Install docx2pdf for Word to PDF conversion
subprocess.check_call([sys.executable, "-m", "pip", "install", "docx2pdf"])

from docx2pdf import convert


def main():
    parser = argparse.ArgumentParser(description='Convert Word documents (DOCX/DOC) to PDF')
    parser.add_argument('input_file', help='Path to the Word document (.docx or .doc)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for PDF file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_file argument: {args.input_file}")

    # Expand user path if provided
    input_path = os.path.expanduser(args.input_file)
    print(f"Expanded input_path: {input_path}")
    print(f"Absolute input_path: {os.path.abspath(input_path)}")

    if not os.path.exists(input_path):
        print(f"Error: Word document not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate output filename (replace .docx/.doc with .pdf)
    base_name = os.path.basename(input_path)
    if base_name.lower().endswith('.docx') or base_name.lower().endswith('.doc'):
        output_name = os.path.splitext(base_name)[0] + '.pdf'
    else:
        output_name = base_name + '.pdf'

    output_path = os.path.join(args.output_dir, output_name)

    # Convert Word to PDF
    print(f"Converting Word document to PDF...")
    try:
        convert(input_path, output_path)
        print(f"Successfully converted Word to PDF: {output_path}")
        print("Conversion completed!")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()