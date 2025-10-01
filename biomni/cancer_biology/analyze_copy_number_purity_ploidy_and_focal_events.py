#!/usr/bin/env python3
"""
Wrapper for Biomni analyze_copy_number_purity_ploidy_and_focal_events tool
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
    from biomni.tool.cancer_biology import analyze_copy_number_purity_ploidy_and_focal_events
    if len(sys.argv) != 2:
        print("Usage: analyze_copy_number_purity_ploidy_and_focal_events.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(result)


if __name__ == '__main__':
    main()
