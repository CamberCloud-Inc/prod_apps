#!/usr/bin/env python3
"""
Camber wrapper for analyze_atac_seq_differential_accessibility from biomni.tool.immunology
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
        description='Analyze ATAC-seq differential accessibility between treatment and control'
    )
    parser.add_argument('input_file', help='JSON file with analysis parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    treatment_bam = input_data['treatment_bam']
    control_bam = input_data['control_bam']
    genome_size = input_data.get('genome_size', 'hs')
    q_value = input_data.get('q_value', 0.05)
    name_prefix = input_data.get('name_prefix', 'atac')

    # Import after dependencies are installed
    from biomni.tool.immunology import analyze_atac_seq_differential_accessibility

    result = analyze_atac_seq_differential_accessibility(
        treatment_bam=treatment_bam,
        control_bam=control_bam,
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


if __name__ == "__main__":
    main()
