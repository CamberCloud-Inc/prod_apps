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
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze copy number, purity, ploidy and focal events'
    )
    parser.add_argument('input_file', help='JSON file with parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import analyze_copy_number_purity_ploidy_and_focal_events

    with open(args.input_file, 'r') as f:
        params = json.load(f)

    tumor_bam = params['tumor_bam']
    reference_genome = params['reference_genome']
    output_dir = params.get('output_dir', './results')
    normal_bam = params.get('normal_bam')

    result = analyze_copy_number_purity_ploidy_and_focal_events(
        tumor_bam=tumor_bam,
        reference_genome=reference_genome,
        output_dir=output_dir,
        normal_bam=normal_bam
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'copy_number_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
