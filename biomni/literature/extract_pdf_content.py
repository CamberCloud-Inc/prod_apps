#!/usr/bin/env python3
"""
Biomni Tool: Extract Pdf Content
Wraps: biomni.tool.literature.extract_pdf_content
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    """Install required dependencies"""
    deps = ['PyPDF2', 'biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Extract Pdf Content'
    )
    parser.add_argument('--url', required=True, help='URL pointing to a PDF file or webpage containing a PDF link')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.literature import extract_pdf_content

    result = extract_pdf_content(url=args.url)

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'pdf_content.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
