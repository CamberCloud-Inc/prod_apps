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
    parser.add_argument('input_file', help='JSON file with parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import detect_and_annotate_somatic_mutations

    with open(args.input_file, 'r') as f:
        params = json.load(f)

    tumor_bam = params['tumor_bam']
    normal_bam = params['normal_bam']
    reference_genome = params['reference_genome']
    output_prefix = params['output_prefix']
    snpeff_database = params.get('snpeff_database', 'GRCh38.105')

    result = detect_and_annotate_somatic_mutations(
        tumor_bam=tumor_bam,
        normal_bam=normal_bam,
        reference_genome=reference_genome,
        output_prefix=output_prefix,
        snpeff_database=snpeff_database
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'somatic_mutations_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
