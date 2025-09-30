import subprocess
import sys
import os
import argparse

# Install weasyprint for HTML to PDF conversion
subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint"])

from weasyprint import HTML


def main():
    parser = argparse.ArgumentParser(description='Convert HTML files to PDF')
    parser.add_argument('input_file', help='Path to the HTML file')
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
        print(f"Error: HTML file not found at: {input_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate output filename (replace .html with .pdf)
    base_name = os.path.basename(input_path)
    if base_name.endswith('.html') or base_name.endswith('.htm'):
        output_name = os.path.splitext(base_name)[0] + '.pdf'
    else:
        output_name = base_name + '.pdf'

    output_path = os.path.join(args.output_dir, output_name)

    # Convert HTML to PDF
    print(f"Converting HTML to PDF...")
    try:
        HTML(filename=input_path).write_pdf(output_path)
        print(f"Successfully converted HTML to PDF: {output_path}")
        print("Conversion completed!")
    except Exception as e:
        print(f"Error during conversion: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()