#!/usr/bin/env python3
"""
Wrapper for Biomni detect_and_annotate_somatic_mutations tool
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Detect and annotate somatic mutations'
    )
    parser.add_argument('tumor_bam', help='Path to the tumor sample BAM file')
    parser.add_argument('normal_bam', help='Path to the matched normal sample BAM file')
    parser.add_argument('reference_genome', help='Path to the reference genome FASTA file')
    parser.add_argument('output_prefix', help='Prefix for output files')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--snpeff-database', default='GRCh38.105', help='SnpEff annotation database version (default: GRCh38.105)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import detect_and_annotate_somatic_mutations

    result = detect_and_annotate_somatic_mutations(
        tumor_bam=args.tumor_bam,
        normal_bam=args.normal_bam,
        reference_genome=args.reference_genome,
        output_prefix=args.output_prefix,
        snpeff_database=args.snpeff_database
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'somatic_mutations_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
