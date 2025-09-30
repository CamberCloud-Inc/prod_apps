import subprocess
import sys
import os
import argparse

# Install PyMuPDF
subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])

import fitz  # PyMuPDF


def main():
    parser = argparse.ArgumentParser(description='Split PDF into individual page files')
    parser.add_argument('input_file', help='Path to the PDF file to split')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for split PDF files (default: ./)')

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
    total_pages = len(pdf_document)
    print(f"PDF has {total_pages} page(s)")

    # Get base filename without extension
    base_name = os.path.basename(input_path)
    if base_name.endswith('.pdf'):
        base_name = base_name[:-4]

    # Split each page into a separate PDF
    for page_num in range(total_pages):
        # Create a new PDF with just this page
        single_page_pdf = fitz.open()
        single_page_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        # Generate output filename with zero-padded page numbers
        output_filename = f"{base_name}_page_{page_num + 1:03d}.pdf"
        output_path = os.path.join(args.output_dir, output_filename)

        # Save the single-page PDF
        single_page_pdf.save(output_path)
        single_page_pdf.close()

        print(f"Created page {page_num + 1}/{total_pages}: {output_filename}")

    # Close the original PDF
    pdf_document.close()

    print(f"\nSuccessfully split PDF into {total_pages} separate files")
    print("PDF split completed!")


if __name__ == "__main__":
    main()