#!/usr/bin/env python3
"""
Wrapper for Biomni detect_and_characterize_structural_variations tool
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
        description='Detect and characterize structural variations'
    )
    parser.add_argument('input_file', help='JSON file with parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import detect_and_characterize_structural_variations

    with open(args.input_file, 'r') as f:
        params = json.load(f)

    bam_file_path = params['bam_file_path']
    reference_genome_path = params['reference_genome_path']
    output_dir = params['output_dir']
    cosmic_db_path = params.get('cosmic_db_path')
    clinvar_db_path = params.get('clinvar_db_path')

    result = detect_and_characterize_structural_variations(
        bam_file_path=bam_file_path,
        reference_genome_path=reference_genome_path,
        output_dir=output_dir,
        cosmic_db_path=cosmic_db_path,
        clinvar_db_path=clinvar_db_path
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'structural_variations_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
