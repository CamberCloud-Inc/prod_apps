import subprocess
import sys
import os
import argparse

# Install PyMuPDF for PDF page extraction
subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])

import fitz  # PyMuPDF


def main():
    parser = argparse.ArgumentParser(description='Extract specific page ranges from PDF files')
    parser.add_argument('input_file', help='Path to the PDF file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for extracted PDF (default: ./)')
    parser.add_argument('-s', '--start-page', type=int, default=1,
                        help='Start page number (1-based, default: 1)')
    parser.add_argument('-e', '--end-page', type=int, default=None,
                        help='End page number (1-based, default: last page)')

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

    # Extract pages
    print(f"Opening PDF...")
    try:
        pdf_document = fitz.open(input_path)
        total_pages = len(pdf_document)
        print(f"Total pages in PDF: {total_pages}")

        # Convert 1-based page numbers to 0-based indices
        start_idx = args.start_page - 1
        end_idx = (args.end_page - 1) if args.end_page else (total_pages - 1)

        # Validate page range
        if start_idx < 0:
            print(f"Error: Start page must be at least 1")
            sys.exit(1)

        if start_idx >= total_pages:
            print(f"Error: Start page {args.start_page} exceeds total pages ({total_pages})")
            sys.exit(1)

        if end_idx >= total_pages:
            print(f"Warning: End page {args.end_page} exceeds total pages ({total_pages}), using last page")
            end_idx = total_pages - 1

        if end_idx < start_idx:
            print(f"Error: End page must be greater than or equal to start page")
            sys.exit(1)

        print(f"Extracting pages {args.start_page} to {end_idx + 1}...")

        # Create new PDF with selected pages
        output_pdf = fitz.open()

        for page_num in range(start_idx, end_idx + 1):
            output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

        # Generate output filename
        base_name = os.path.basename(input_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_name = f"{name_without_ext}_pages_{args.start_page}-{end_idx + 1}.pdf"
        output_path = os.path.join(args.output_dir, output_name)

        # Save the extracted PDF
        output_pdf.save(output_path)
        output_pdf.close()
        pdf_document.close()

        extracted_pages = end_idx - start_idx + 1
        print(f"Successfully extracted {extracted_pages} pages")
        print(f"Output saved to: {output_path}")
        print("Page extraction completed!")

    except Exception as e:
        print(f"Error during extraction: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()