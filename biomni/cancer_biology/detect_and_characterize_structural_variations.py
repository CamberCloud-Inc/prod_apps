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
    parser.add_argument('bam_file_path', help='Path to the BAM file containing aligned sequencing reads')
    parser.add_argument('reference_genome_path', help='Path to the reference genome FASTA file')
    parser.add_argument('output_dir_internal', help='Directory for output files')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--cosmic-db-path', help='Path to COSMIC database for annotation (optional)')
    parser.add_argument('--clinvar-db-path', help='Path to ClinVar database for annotation (optional)')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import detect_and_characterize_structural_variations

    result = detect_and_characterize_structural_variations(
        bam_file_path=args.bam_file_path,
        reference_genome_path=args.reference_genome_path,
        output_dir=args.output_dir_internal,
        cosmic_db_path=args.cosmic_db_path,
        clinvar_db_path=args.clinvar_db_path
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'structural_variations_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
