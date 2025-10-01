#!/usr/bin/env python3
"""
Wrapper for Biomni analyze_copy_number_purity_ploidy_and_focal_events tool
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['FlowCytometryTools', 'biomni', 'gseapy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze copy number, purity, ploidy and focal events'
    )
    parser.add_argument('tumor_bam', help='Path to the tumor sample BAM file')
    parser.add_argument('reference_genome', help='Path to the reference genome FASTA file')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--output-dir', default='./results', help='Directory for output files (default: ./results)')
    parser.add_argument('--normal-bam', help='Path to the matched normal sample BAM file (optional)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import analyze_copy_number_purity_ploidy_and_focal_events

    result = analyze_copy_number_purity_ploidy_and_focal_events(
        tumor_bam=args.tumor_bam,
        reference_genome=args.reference_genome,
        output_dir=args.output_dir,
        normal_bam=args.normal_bam
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'copy_number_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
