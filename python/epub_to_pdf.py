import subprocess
import sys
import os
import argparse

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "ebooklib", "weasyprint"])

from ebooklib import epub
from weasyprint import HTML, CSS
from io import BytesIO


def main():
    parser = argparse.ArgumentParser(description='Convert EPUB ebooks to PDF')
    parser.add_argument('epub_path', help='Path to the EPUB file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for PDF file (default: ./)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received epub_path argument: {args.epub_path}")

    # Expand user path if provided
    epub_path = os.path.expanduser(args.epub_path)
    print(f"Expanded epub_path: {epub_path}")

    if not os.path.exists(epub_path):
        print(f"Error: EPUB file not found at: {epub_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Read EPUB file
    print(f"Reading EPUB file: {epub_path}")
    try:
        book = epub.read_epub(epub_path)
    except Exception as e:
        print(f"Error reading EPUB file: {e}")
        sys.exit(1)

    # Extract HTML content from EPUB
    print("Extracting content from EPUB...")
    html_content = []

    # Get all document items (chapters/sections)
    items = list(book.get_items_of_type(9))  # 9 is ITEM_DOCUMENT
    print(f"Found {len(items)} document items in EPUB")

    # Build complete HTML document
    html_parts = [
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="UTF-8">',
        '<style>',
        'body { font-family: serif; line-height: 1.6; margin: 2cm; }',
        'h1, h2, h3 { margin-top: 1em; margin-bottom: 0.5em; }',
        'p { margin-bottom: 0.5em; }',
        'img { max-width: 100%; height: auto; }',
        '</style>',
        '</head>',
        '<body>'
    ]

    for item in items:
        try:
            content = item.get_content().decode('utf-8')
            html_parts.append(content)
        except Exception as e:
            print(f"Warning: Could not extract content from item: {e}")

    html_parts.append('</body></html>')
    full_html = '\n'.join(html_parts)

    # Generate output filename
    base_name = os.path.splitext(os.path.basename(epub_path))[0]
    output_path = os.path.join(args.output_dir, f"{base_name}.pdf")

    # Convert HTML to PDF using WeasyPrint
    print(f"Converting to PDF: {output_path}")
    try:
        HTML(string=full_html).write_pdf(output_path)
        print(f"EPUB to PDF conversion completed! Output: {output_path}")
    except Exception as e:
        print(f"Error during PDF conversion: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()