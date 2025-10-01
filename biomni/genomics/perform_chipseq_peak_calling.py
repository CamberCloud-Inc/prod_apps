#!/usr/bin/env python3
"""Biomni Tool: Perform ChIP-seq Peak Calling with MACS2
Wraps: biomni.tool.genomics.perform_chipseq_peak_calling_with_macs2
"""
import argparse
import sys
import subprocess
import os

def install_dependencies():
    deps = ['biomni', 'macs2']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Perform ChIP-seq peak calling using MACS2'
    )
    parser.add_argument('chipseq_file', help='ChIP-seq read data file (BAM/BED) from stash')
    parser.add_argument('control_file', help='Control/input data file (BAM/BED) from stash')
    parser.add_argument('--output-name', default='macs2_output',
                       help='Prefix for output files (default: macs2_output)')
    parser.add_argument('--genome-size', default='hs',
                       help='Effective genome size: hs (human), mm (mouse), etc. (default: hs)')
    parser.add_argument('--q-value', type=float, default=0.05,
                       help='q-value (minimum FDR) cutoff (default: 0.05)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.genomics import perform_chipseq_peak_calling_with_macs2

    output_prefix = os.path.join(args.output, args.output_name)
    result = perform_chipseq_peak_calling_with_macs2(
        chip_seq_file=args.chipseq_file,
        control_file=args.control_file,
        output_name=output_prefix,
        genome_size=args.genome_size,
        q_value=args.q_value
    )

    output_file = os.path.join(args.output, 'macs2_log.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
