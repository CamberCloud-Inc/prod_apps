#!/usr/bin/env python3
"""
Biomni Tool: Advanced Web Search Claude
Wraps: biomni.tool.literature.advanced_web_search_claude
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
        description='Advanced Web Search Claude'
    )
    parser.add_argument('--query', required=True, help='The search query or research question')
    parser.add_argument('--max_searches', default='5', help='Maximum number of search iterations to perform (default: 5)')
    parser.add_argument('--max_retries', default='3', help='Maximum number of retry attempts for failed searches (default: 3)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.literature import advanced_web_search_claude

    result = advanced_web_search_claude(
        query=args.query,
        max_searches=int(args.max_searches),
        max_retries=int(args.max_retries)
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'search_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
