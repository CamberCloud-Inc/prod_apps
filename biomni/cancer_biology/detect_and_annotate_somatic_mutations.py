#!/usr/bin/env python3
"""
Wrapper for Biomni detect_and_annotate_somatic_mutations tool
"""

import sys
import json



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

    # Import after dependencies are installed
    from biomni.tool.cancer_biology import detect_and_annotate_somatic_mutations
    if len(sys.argv) != 2:
        print("Usage: detect_and_annotate_somatic_mutations.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(result)


if __name__ == '__main__':
    main()
