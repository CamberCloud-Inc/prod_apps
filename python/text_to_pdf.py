import subprocess
import sys
import os
import argparse

# Install reportlab for text to PDF conversion
subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT


def main():
    parser = argparse.ArgumentParser(description='Convert plain text files to formatted PDF')
    parser.add_argument('input_file', help='Path to the text file (.txt)')
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
        print(f"Error: Text file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate output filename (replace .txt with .pdf)
    base_name = os.path.basename(input_path)
    if base_name.lower().endswith('.txt'):
        output_name = os.path.splitext(base_name)[0] + '.pdf'
    else:
        output_name = base_name + '.pdf'

    output_path = os.path.join(args.output_dir, output_name)

    # Convert text to PDF
    print(f"Converting text to PDF...")
    try:
        # Read the text file
        with open(input_path, 'r', encoding='utf-8') as f:
            text_content = f.read()

        # Create PDF
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=0.75*inch,
            rightMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Define styles
        styles = getSampleStyleSheet()

        # Create a custom style for body text
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )

        # Split text into paragraphs (by double newlines) and lines
        story = []
        paragraphs = text_content.split('\n\n')

        for para_text in paragraphs:
            if para_text.strip():
                # Replace single newlines with <br/> tags for line breaks within paragraphs
                formatted_text = para_text.strip().replace('\n', '<br/>')
                para = Paragraph(formatted_text, body_style)
                story.append(para)
                story.append(Spacer(1, 0.2*inch))

        # Build PDF
        doc.build(story)

        print(f"Successfully converted text to PDF: {output_path}")
        print("Conversion completed!")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()