#!/usr/bin/env python3
"""
Biomni Tool: Query Alphafold
Wraps: biomni.tool.database.query_alphafold
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
        description='Query Alphafold'
    )
    parser.add_argument('--uniprot_id', required=True, help='UniProt protein identifier')
    parser.add_argument('--endpoint', default='prediction', help='API endpoint (default: prediction)')
    parser.add_argument('--residue_range', help='Residue range (optional)')
    parser.add_argument('--download', default='false', help='Download files (true/false, default: false)')
    parser.add_argument('--output_dir', help='Output directory for downloads (optional)')
    parser.add_argument('--file_format', default='pdb', help='File format (pdb/cif, default: pdb)')
    parser.add_argument('--model_version', default='v4', help='Model version (default: v4)')
    parser.add_argument('--model_number', default='1', help='Model number (default: 1)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import query_alphafold

    result = query_alphafold(
        uniprot_id=args.uniprot_id,
        endpoint=args.endpoint,
        residue_range=args.residue_range,
        download=args.download.lower() == 'true' if args.download else None,
        output_dir=args.output_dir,
        file_format=args.file_format,
        model_version=args.model_version,
        model_number=int(args.model_number) if args.model_number else None
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'alphafold_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
