#!/usr/bin/env python3
"""
Predict RNA secondary structure from sequence using thermodynamic models.
"""

import sys
import json
from biomni.tool.microbiology import predict_rna_secondary_structure



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
    rna_sequence = input_data.get('rna_sequence')
    output_format = input_data.get('output_format', 'dot_bracket')
    temperature = input_data.get('temperature', 37.0)

    # Call the function
    result = predict_rna_secondary_structure(
        rna_sequence=rna_sequence,
        output_format=output_format,
        temperature=temperature
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
