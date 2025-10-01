#!/usr/bin/env python3
"""
Camber wrapper for extract_pdf_content from biomni.tool.literature
"""

import argparse
import sys
import json
import subprocess
import os


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Extract content from PDF'
    )
    parser.add_argument('input_file', help='JSON file with URL from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    url = input_data['url']

    # Import after dependencies are installed
    from biomni.tool.literature import extract_pdf_content

    result = extract_pdf_content(url=url)

    # Write output
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'pdf_content.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
