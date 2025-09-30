import subprocess
import sys
import os
import argparse

# Install PyMuPDF
subprocess.check_call([sys.executable, "-m", "pip", "install", "PyMuPDF"])

import fitz  # PyMuPDF
from PIL import Image
import io


def main():
    parser = argparse.ArgumentParser(description='Convert PDF pages to PNG images')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output-dir', default='outputs',
                        help='Output directory for images (default: outputs)')
    parser.add_argument('-z', '--zoom', type=float, default=2.0,
                        help='Zoom factor for image quality (default: 2.0)')

    args = parser.parse_args()

    # Expand user path if provided
    pdf_path = os.path.expanduser(args.pdf_path)

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at: {pdf_path}")
        sys.exit(1)

    # Create outputs directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    print(f"PDF has {len(pdf_document)} page(s)")

    # Convert each page to image
    for page_num in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_num)

        # Convert page to image (matrix for higher resolution)
        mat = fitz.Matrix(args.zoom, args.zoom)
        pix = page.get_pixmap(matrix=mat)

        # Convert to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))

        # Save the image
        output_path = os.path.join(args.output_dir, f"pdf_page_{page_num + 1}.png")
        img.save(output_path)
        print(f"Saved page {page_num + 1} as {output_path}")

    # Close the PDF
    pdf_document.close()

    print("PDF conversion completed!")


if __name__ == "__main__":
    main()