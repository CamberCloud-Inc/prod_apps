#!/usr/bin/env python3
"""
Biomni Tool: Extract Url Content
Wraps: biomni.tool.literature.extract_url_content
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Extract Url Content'
    )
    parser.add_argument('--url', required=True, help='URL of the webpage to extract content from')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.literature import extract_url_content

    result = extract_url_content(url=args.url)

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'url_content.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
