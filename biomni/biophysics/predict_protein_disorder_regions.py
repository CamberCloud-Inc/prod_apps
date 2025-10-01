#!/usr/bin/env python3
"""
Predict Protein Disorder Regions

Predicts intrinsically disordered regions (IDRs) in a protein sequence using IUPred2A.
"""

import sys
import json
from biomni.tool.biophysics import predict_protein_disorder_regions



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
        print("Usage: predict_protein_disorder_regions.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    protein_sequence = inputs['protein_sequence']
    threshold = inputs.get('threshold', 0.5)
    output_file = inputs.get('output_file', 'disorder_prediction_results.csv')

    result = predict_protein_disorder_regions(
        protein_sequence=protein_sequence,
        threshold=threshold,
        output_file=output_file
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
