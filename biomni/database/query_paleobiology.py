#!/usr/bin/env python3
"""
Biomni Tool: Query Paleobiology
Wraps: biomni.tool.database.query_paleobiology
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
        description='Query Paleobiology'
    )
    parser.add_argument('--prompt', help='Query prompt/description')
    parser.add_argument('--endpoint', help='API endpoint path')
    parser.add_argument('--verbose', help='Enable verbose output (true/false)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import query_paleobiology

    result = query_paleobiology(
        prompt=args.prompt,
        endpoint=args.endpoint,
        verbose=args.verbose.lower() == 'true' if args.verbose else None
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'paleobiology_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
