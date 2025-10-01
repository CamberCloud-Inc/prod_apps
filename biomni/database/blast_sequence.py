#!/usr/bin/env python3
"""
Biomni Tool: Blast Sequence
Wraps: biomni.tool.database.blast_sequence
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
        description='Blast Sequence'
    )
    parser.add_argument('--sequence', required=True, help='The nucleotide or protein sequence to search')
    parser.add_argument('--database', required=True, help='Target NCBI database (e.g., 'nt', 'nr')')
    parser.add_argument('--program', required=True, help='BLAST program type (blastn, blastp, blastx, tblastn, tblastx)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.database import blast_sequence

    result = blast_sequence(
        sequence=args.sequence,
        database=args.database,
        program=args.program
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'blast_results.json')
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2, default=str)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
