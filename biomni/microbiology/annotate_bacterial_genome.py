#!/usr/bin/env python3
"""
Annotate a bacterial genome using Prokka to identify genes, proteins, and functional features.
"""

import sys
import json
from biomni.tool.microbiology import annotate_bacterial_genome



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
    
    install_dependencies()
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

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

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
