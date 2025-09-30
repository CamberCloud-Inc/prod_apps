import subprocess
import sys
import os
import argparse

# Install PyMuPDF
subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])

import fitz  # PyMuPDF


def main():
    parser = argparse.ArgumentParser(description='Extract all text from PDF to TXT file')
    parser.add_argument('input_file', help='Path to the PDF file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for text file (default: ./)')

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
        print(f"Error: PDF file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Open the PDF
    print(f"Opening PDF file: {input_path}")
    pdf_document = fitz.open(input_path)
    print(f"PDF has {len(pdf_document)} page(s)")

    # Extract text from all pages
    all_text = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        all_text.append(f"--- Page {page_num + 1} ---\n\n{text}\n")
        print(f"Extracted text from page {page_num + 1}")

    # Close the PDF
    pdf_document.close()

    # Generate output filename
    base_name = os.path.basename(input_path)
    if base_name.endswith('.pdf'):
        output_name = base_name[:-4] + '.txt'
    else:
        output_name = base_name + '.txt'

    output_path = os.path.join(args.output_dir, output_name)

    # Write all text to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))

    print(f"Successfully extracted text to: {output_path}")
    print("Text extraction completed!")


if __name__ == "__main__":
    main()