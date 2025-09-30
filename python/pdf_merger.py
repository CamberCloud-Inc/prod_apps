import subprocess
import sys
import os
import argparse

# Install PyMuPDF
subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])

import fitz  # PyMuPDF


def main():
    parser = argparse.ArgumentParser(description='Merge multiple PDF files into one')
    parser.add_argument('input_files', nargs='+', help='Paths to PDF files to merge (space-separated)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for merged PDF (default: ./)')
    parser.add_argument('-n', '--output-name', default='merged.pdf',
                        help='Name of output file (default: merged.pdf)')

    args = parser.parse_args()

    # Debug: print current working directory and its contents
    print(f"Current working directory: {os.getcwd()}")
    print(f"Contents of current directory:")
    for item in os.listdir("."):
        print(f"  {item}")

    print(f"\nReceived input_files arguments: {args.input_files}")

    # Filter out empty strings from input files
    input_files = [f for f in args.input_files if f.strip()]

    # Validate that we have at least 2 PDFs
    if len(input_files) < 2:
        print("Error: At least 2 PDF files are required for merging")
        sys.exit(1)

    # Expand and validate input paths
    input_paths = []
    for input_file in input_files:
        input_path = os.path.expanduser(input_file)
        print(f"Checking PDF: {input_path}")

        if not os.path.exists(input_path):
            print(f"Error: PDF file not found at: {input_path}")
            sys.exit(1)

        input_paths.append(input_path)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Create a new PDF for the merged output
    merged_pdf = fitz.open()

    # Merge all PDFs
    total_pages = 0
    for i, pdf_path in enumerate(input_paths, 1):
        print(f"\nMerging PDF {i}/{len(input_paths)}: {pdf_path}")
        pdf_document = fitz.open(pdf_path)
        pages_in_doc = len(pdf_document)
        print(f"  Pages in this PDF: {pages_in_doc}")

        # Insert all pages from this PDF
        merged_pdf.insert_pdf(pdf_document)
        total_pages += pages_in_doc
        pdf_document.close()

    # Save the merged PDF
    output_path = os.path.join(args.output_dir, args.output_name)
    merged_pdf.save(output_path)
    merged_pdf.close()

    print(f"\nSuccessfully merged {len(input_paths)} PDF files")
    print(f"Total pages in merged PDF: {total_pages}")
    print(f"Output saved to: {output_path}")
    print("PDF merge completed!")


if __name__ == "__main__":
    main()