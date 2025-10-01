#!/usr/bin/env python3
"""
Annotate a bacterial genome using Prokka to identify genes, proteins, and functional features.
"""

import sys
import json
import argparse
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'biopython']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Annotate a bacterial genome using Prokka to identify genes, proteins, and functional features.'
    )
    parser.add_argument('--genome-file-path', type=str, required=True, help='Path to the bacterial genome assembly file (FASTA format)')
    parser.add_argument('--output-dir', type=str, default='annotation_results', help='Directory where annotation results will be saved')
    parser.add_argument('--genus', type=str, default='', help='Genus name of the organism for improved annotation accuracy')
    parser.add_argument('--species', type=str, default='', help='Species name of the organism')
    parser.add_argument('--strain', type=str, default='', help='Strain identifier for the organism')
    parser.add_argument('--prefix', type=str, default='', help='Prefix for output file naming')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import annotate_bacterial_genome

    # Call the function
    result = annotate_bacterial_genome(
        genome_file_path=args.genome_file_path,
        output_dir=args.output_dir,
        genus=args.genus,
        species=args.species,
        strain=args.strain,
        prefix=args.prefix
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'genome_annotation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
