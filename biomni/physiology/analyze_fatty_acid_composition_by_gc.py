#!/usr/bin/env python3
"""
Analyze Fatty Acid Composition by GC

Analyzes fatty acid composition in tissue samples using gas chromatography data.
"""

import sys
import json
from biomni.tool.physiology import analyze_fatty_acid_composition_by_gc



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
        print("Usage: analyze_fatty_acid_composition_by_gc.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    gc_data_file = inputs['gc_data_file']
    tissue_type = inputs['tissue_type']
    sample_id = inputs['sample_id']
    output_directory = inputs.get('output_directory', './results')

    result = analyze_fatty_acid_composition_by_gc(
        gc_data_file=gc_data_file,
        tissue_type=tissue_type,
        sample_id=sample_id,
        output_directory=output_directory
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
