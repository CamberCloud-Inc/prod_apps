#!/usr/bin/env python3
"""
Biomni Tool: Search Google
Wraps: biomni.tool.literature.search_google
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
        description='Search Google'
    )
    parser.add_argument('--query', required=True, help='Search query string')
    parser.add_argument('--num_results', default='10', help='Number of search results to return (default: 10)')
    parser.add_argument('--language', default='en', help='Language code for search results (default: "en" for English)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.literature import search_google

    result = search_google(
        query=args.query,
        num_results=int(args.num_results),
        language=args.language
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'google_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
