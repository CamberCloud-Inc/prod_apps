#!/usr/bin/env python3
"""
Biomni Tool: Query Pride
Wraps: biomni.tool.database.query_pride
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni', 'biopython']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Query Pride'
    )
    parser.add_argument('--prompt', help='Query prompt/description')
    parser.add_argument('--endpoint', help='API endpoint path')
    parser.add_argument('--max_results', help='Maximum number of results')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import query_pride

    result = query_pride(
        prompt=args.prompt,
        endpoint=args.endpoint,
        max_results=int(args.max_results) if args.max_results else None
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'pride_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
