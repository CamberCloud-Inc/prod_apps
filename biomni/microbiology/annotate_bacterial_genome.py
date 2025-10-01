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
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Annotate a bacterial genome using Prokka to identify genes, proteins, and functional features.'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.microbiology import annotate_bacterial_genome

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    genome_file_path = input_data.get('genome_file_path')
    output_dir = input_data.get('output_dir', 'annotation_results')
    genus = input_data.get('genus', '')
    species = input_data.get('species', '')
    strain = input_data.get('strain', '')
    prefix = input_data.get('prefix', '')

    # Call the function
    result = annotate_bacterial_genome(
        genome_file_path=genome_file_path,
        output_dir=output_dir,
        genus=genus,
        species=species,
        strain=strain,
        prefix=prefix
    )

    # Write result to output file
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'genome_annotation_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
