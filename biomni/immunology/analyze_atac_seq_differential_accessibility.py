#!/usr/bin/env python3
"""
Biomni Tool: Analyze Atac Seq Differential Accessibility
Wraps: biomni.tool.immunology.analyze_atac_seq_differential_accessibility
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
        description='Analyze Atac Seq Differential Accessibility'
    )
    parser.add_argument('--treatment_bam', help='Path to treatment BAM file with aligned ATAC-seq reads')
    parser.add_argument('--control_bam', help='Path to control BAM file with aligned ATAC-seq reads')
    parser.add_argument('--genome_size', help='Effective genome size (hs, mm, ce, dm) (default: hs)')
    parser.add_argument('--q_value', help='Q-value cutoff for peak detection (default: 0.05)')
    parser.add_argument('--name_prefix', help='Prefix for output file names (default: atac)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import analyze_atac_seq_differential_accessibility

    # Parse optional parameters with defaults
    genome_size = args.genome_size if args.genome_size else 'hs'
    q_value = float(args.q_value) if args.q_value else 0.05
    name_prefix = args.name_prefix if args.name_prefix else 'atac'

    result = analyze_atac_seq_differential_accessibility(
        treatment_bam=args.treatment_bam,
        control_bam=args.control_bam,
        output_dir=args.output,
        genome_size=genome_size,
        q_value=q_value,
        name_prefix=name_prefix
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'atac_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
