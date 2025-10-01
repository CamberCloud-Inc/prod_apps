#!/usr/bin/env python3
"""
Analyze Protein Conservation

Perform multiple sequence alignment and phylogenetic analysis to identify conserved protein regions.
"""

import sys
import json
from biomni.tool.biochemistry import analyze_protein_conservation



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
        print("Usage: analyze_protein_conservation.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    protein_sequences = inputs['protein_sequences']
    output_dir = inputs.get('output_dir', './')

    result = analyze_protein_conservation(
        protein_sequences=protein_sequences,
        output_dir=output_dir
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
