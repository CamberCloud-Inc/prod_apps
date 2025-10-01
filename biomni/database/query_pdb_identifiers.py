#!/usr/bin/env python3
"""
Biomni Tool: Query Pdb Identifiers
Wraps: biomni.tool.database.query_pdb_identifiers
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
        description='Query Pdb Identifiers'
    )
    parser.add_argument('--identifiers', help='Comma-separated PDB identifiers')
    parser.add_argument('--return_type', help='Return data type')
    parser.add_argument('--download', help='Download files (true/false)')
    parser.add_argument('--attributes', help='Attributes to retrieve')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import query_pdb_identifiers

    result = query_pdb_identifiers(
        identifiers=args.identifiers,
        return_type=args.return_type,
        download=args.download.lower() == 'true' if args.download else None,
        attributes=args.attributes
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'pdb_identifiers_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
