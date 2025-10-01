#!/usr/bin/env python3
"""
Biomni Tool: Query Scholar
Wraps: biomni.tool.literature.query_scholar
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    """Install required dependencies"""
    deps = ['PyPDF2', 'biomni', 'beautifulsoup4']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Query Scholar'
    )
    parser.add_argument('--query', required=True, help='Search query string for scholarly literature')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.literature import query_scholar

    result = query_scholar(query=args.query)

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'scholar_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
