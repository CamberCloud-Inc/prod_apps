#!/usr/bin/env python3
"""
Camber wrapper for advanced_web_search_claude from biomni.tool.literature
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
        description='Advanced web search using Claude'
    )
    parser.add_argument('input_file', help='JSON file with query parameters from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    query = input_data['query']
    max_searches = input_data.get('max_searches', 5)
    max_retries = input_data.get('max_retries', 3)

    # Import after dependencies are installed
    from biomni.tool.literature import advanced_web_search_claude

    result = advanced_web_search_claude(query=query, max_searches=max_searches, max_retries=max_retries)

    # Write output
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'search_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
