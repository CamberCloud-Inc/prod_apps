import subprocess
import sys
import os
import argparse

# Install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "PyMuPDF", "ebooklib"])

import fitz  # PyMuPDF
from ebooklib import epub


def main():
    parser = argparse.ArgumentParser(description='Convert PDF files to EPUB ebook format')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for EPUB file (default: ./)')
    parser.add_argument('-t', '--title', default=None,
                        help='Book title (default: PDF filename)')
    parser.add_argument('-a', '--author', default='Unknown',
                        help='Book author (default: Unknown)')
    parser.add_argument('-l', '--language', default='en',
                        help='Book language (default: en)')

    args = parser.parse_args()

    # Debug: print current working directory
    print(f"Current working directory: {os.getcwd()}")
    print(f"Received pdf_path argument: {args.pdf_path}")

    # Expand user path if provided
    pdf_path = os.path.expanduser(args.pdf_path)
    print(f"Expanded pdf_path: {pdf_path}")

    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at: {pdf_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Determine title
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    title = args.title if args.title else base_name

    print(f"\nConverting PDF to EPUB")
    print(f"Title: {title}")
    print(f"Author: {args.author}")
    print(f"Language: {args.language}")

    try:
        # Open PDF
        print(f"\nOpening PDF: {pdf_path}")
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        print(f"PDF has {total_pages} pages")

        # Create EPUB book
        book = epub.EpubBook()

        # Set metadata
        book.set_identifier(f'pdf2epub_{base_name}')
        book.set_title(title)
        book.set_language(args.language)
        book.add_author(args.author)

        # Extract text and create chapters
        chapters = []
        toc = []

        print("\nExtracting text from pages...")
        for page_num in range(total_pages):
            page = pdf_document[page_num]
            text = page.get_text()

            # Create a chapter for each page
            chapter = epub.EpubHtml(
                title=f'Page {page_num + 1}',
                file_name=f'page_{page_num + 1}.xhtml',
                lang=args.language
            )

            # Convert text to HTML paragraphs
            html_content = '<h2>Page {}</h2>\n'.format(page_num + 1)
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    html_content += '<p>{}</p>\n'.format(para.strip().replace('\n', '<br/>'))

            chapter.content = html_content
            book.add_item(chapter)
            chapters.append(chapter)
            toc.append(chapter)

            if (page_num + 1) % 10 == 0:
                print(f"  Processed {page_num + 1}/{total_pages} pages...")

        print(f"  Processed {total_pages}/{total_pages} pages")

        pdf_document.close()

        # Define Table of Contents
        book.toc = tuple(toc)

        # Add default NCX and Nav files
        book.add_item(epub.EpubNcx())
        book.add_item(epub.EpubNav())

        # Define CSS style
        style = '''
        body {
            font-family: Georgia, serif;
            line-height: 1.6;
            margin: 1em;
        }
        h2 {
            color: #333;
            border-bottom: 2px solid #666;
            padding-bottom: 0.3em;
        }
        p {
            text-align: justify;
            margin: 1em 0;
        }
        '''
        nav_css = epub.EpubItem(
            uid="style_nav",
            file_name="style/nav.css",
            media_type="text/css",
            content=style
        )
        book.add_item(nav_css)

        # Create spine
        book.spine = ['nav'] + chapters

        # Generate output filename
        output_filename = f"{base_name}.epub"
        output_path = os.path.join(args.output_dir, output_filename)

        print(f"\nWriting EPUB file: {output_path}")

        # Write EPUB file
        epub.write_epub(output_path, book, {})

        print(f"EPUB file saved to: {output_path}")
        print(f"Converted {total_pages} pages to EPUB format")

    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nPDF to EPUB conversion completed successfully!")


if __name__ == "__main__":
    main()