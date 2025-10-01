#!/usr/bin/env python3
"""
Analyze RNA Secondary Structure Features

Calculate numeric values for various structural features of an RNA secondary structure.
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
    from biomni.tool.biochemistry import analyze_rna_secondary_structure_features
    if len(sys.argv) != 2:
        print("Usage: analyze_rna_secondary_structure_features.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    dot_bracket_structure = inputs['dot_bracket_structure']
    sequence = inputs.get('sequence')

    result = analyze_rna_secondary_structure_features(
        dot_bracket_structure=dot_bracket_structure,
        sequence=sequence
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
