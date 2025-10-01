#!/usr/bin/env python3
"""
Camber wrapper for analyze_atac_seq_differential_accessibility from biomni.tool.immunology
"""

import sys
from biomni.tool.immunology import analyze_atac_seq_differential_accessibility



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
    if len(sys.argv) < 3:
        print("Usage: analyze_atac_seq_differential_accessibility.py <treatment_bam> <control_bam> [output_dir] [genome_size] [q_value] [name_prefix]")
        sys.exit(1)

    treatment_bam = sys.argv[1]
    control_bam = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./atac_results"
    genome_size = sys.argv[4] if len(sys.argv) > 4 else "hs"
    q_value = float(sys.argv[5]) if len(sys.argv) > 5 else 0.05
    name_prefix = sys.argv[6] if len(sys.argv) > 6 else "atac"

    result = analyze_atac_seq_differential_accessibility(
        treatment_bam=treatment_bam,
        control_bam=control_bam,
        output_dir=output_dir,
        genome_size=genome_size,
        q_value=q_value,
        name_prefix=name_prefix
    )

    print(result)


if __name__ == "__main__":
    main()
