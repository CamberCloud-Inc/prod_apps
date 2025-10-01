#!/usr/bin/env python3
"""
Biomni Tool: Query Pubmed
Wraps: biomni.tool.literature.query_pubmed
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
        description='Query Pubmed'
    )
    parser.add_argument('--query', required=True, help='Search query string using PubMed syntax or natural language')
    parser.add_argument('--max_papers', default='10', help='Maximum number of papers to return (default: 10)')
    parser.add_argument('--max_retries', default='3', help='Maximum number of retry attempts with simplified queries (default: 3)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.literature import query_pubmed

    result = query_pubmed(
        query=args.query,
        max_papers=int(args.max_papers),
        max_retries=int(args.max_retries)
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'pubmed_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
