#!/usr/bin/env python3
"""
Wrapper for Biomni detect_and_characterize_structural_variations tool
"""

import sys
import json
from biomni.tool.cancer_biology import detect_and_characterize_structural_variations



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
    if len(sys.argv) != 2:
        print("Usage: detect_and_characterize_structural_variations.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(result)


if __name__ == '__main__':
    main()
