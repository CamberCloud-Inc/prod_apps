#!/usr/bin/env python3
"""
Biomni Tool: Isolate Purify Immune Cells
Wraps: biomni.tool.immunology.isolate_purify_immune_cells
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
        description='Isolate Purify Immune Cells'
    )
    parser.add_argument('--tissue_type', help='Type of tissue source for cell isolation')
    parser.add_argument('--target_cell_type', help='Specific immune cell population to isolate')
    parser.add_argument('--enzyme_type', help='Enzyme for tissue digestion (default: collagenase)')
    parser.add_argument('--macs_antibody', help='Antibody for MACS selection (optional)')
    parser.add_argument('--digestion_time_min', help='Duration of enzymatic digestion in minutes (default: 45)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import isolate_purify_immune_cells

    # Parse optional parameters with defaults
    enzyme_type = args.enzyme_type if args.enzyme_type else 'collagenase'
    macs_antibody = args.macs_antibody if args.macs_antibody else None
    digestion_time_min = int(args.digestion_time_min) if args.digestion_time_min else 45

    result = isolate_purify_immune_cells(
        tissue_type=args.tissue_type,
        target_cell_type=args.target_cell_type,
        enzyme_type=enzyme_type,
        macs_antibody=macs_antibody,
        digestion_time_min=digestion_time_min
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'isolation_protocol.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")

if __name__ == '__main__':
    main()
