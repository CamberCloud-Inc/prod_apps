#!/usr/bin/env python3
"""Biomni Tool: Find Enriched Motifs with HOMER
Wraps: biomni.tool.genomics.find_enriched_motifs_with_homer
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])
    # Note: HOMER must be installed separately on the system

def main():
    parser = argparse.ArgumentParser(
        description='Find DNA sequence motifs enriched in genomic regions using HOMER'
    )
    parser.add_argument('peak_file', help='Peak file in BED format from stash')
    parser.add_argument('--genome', default='hg38',
                       help='Reference genome (hg38, hg19, mm10, etc.) (default: hg38)')
    parser.add_argument('--background-file', default=None,
                       help='Optional BED file with background regions')
    parser.add_argument('--motif-length', default='8,10,12',
                       help='Comma-separated motif lengths (default: 8,10,12)')
    parser.add_argument('--num-motifs', type=int, default=10,
                       help='Number of motifs to find (default: 10)')
    parser.add_argument('--threads', type=int, default=4,
                       help='Number of CPU threads (default: 4)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.genomics import find_enriched_motifs_with_homer

    result = find_enriched_motifs_with_homer(
        peak_file=args.peak_file,
        genome=args.genome,
        background_file=args.background_file,
        motif_length=args.motif_length,
        output_dir=args.output,
        num_motifs=args.num_motifs,
        threads=args.threads
    )

    output_file = os.path.join(args.output, 'homer_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
