#!/usr/bin/env python3
"""
Camber wrapper for analyze_mitochondrial_morphology_and_potential from Biomni
"""

import json
import sys

from biomni.tool.cell_biology import analyze_mitochondrial_morphology_and_potential



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
    morphology_image_path = input_data.get("morphology_image_path", "")
    potential_image_path = input_data.get("potential_image_path", "")
    output_dir = input_data.get("output_dir", "./output")

    # Call the function
    result = analyze_mitochondrial_morphology_and_potential(
        morphology_image_path=morphology_image_path,
        potential_image_path=potential_image_path,
        output_dir=output_dir
    )

    # Output result as JSON
    output = {
        "research_log": result
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
