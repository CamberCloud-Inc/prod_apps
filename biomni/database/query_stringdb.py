#!/usr/bin/env python3
"""
Biomni Tool: Query Stringdb
Wraps: biomni.tool.database.query_stringdb
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Query Stringdb'
    )
    parser.add_argument('--prompt', help='Query prompt/description')
    parser.add_argument('--endpoint', help='API endpoint path')
    parser.add_argument('--download_image', help='Download network image (true/false)')
    parser.add_argument('--output_dir', help='Output directory for downloads')
    parser.add_argument('--verbose', help='Enable verbose output (true/false)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import query_stringdb

    result = query_stringdb(
        prompt=args.prompt,
        endpoint=args.endpoint,
        download_image=args.download_image.lower() == 'true' if args.download_image else None,
        output_dir=args.output_dir,
        verbose=args.verbose.lower() == 'true' if args.verbose else None
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'stringdb_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
