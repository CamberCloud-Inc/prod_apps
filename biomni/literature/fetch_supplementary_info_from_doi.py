#!/usr/bin/env python3
"""
Biomni Tool: Fetch Supplementary Info From Doi
Wraps: biomni.tool.literature.fetch_supplementary_info_from_doi
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    """Install required dependencies"""
    deps = ['PyPDF2', 'biomni', 'beautifulsoup4', 'googlesearch-python']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Fetch Supplementary Info From Doi'
    )
    parser.add_argument('--doi', required=True, help='Digital Object Identifier of the research paper')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.literature import fetch_supplementary_info_from_doi

    os.makedirs(args.output, exist_ok=True)
    result = fetch_supplementary_info_from_doi(doi=args.doi, output_dir=args.output)

    output_file = os.path.join(args.output, 'supplementary_info.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
