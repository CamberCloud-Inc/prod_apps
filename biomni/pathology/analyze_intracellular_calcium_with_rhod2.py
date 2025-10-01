#!/usr/bin/env python3
"""
Analyze Intracellular Calcium with Rhod-2

Analyze intracellular calcium concentration using Rhod-2 fluorescent indicator.
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
    from biomni.tool.pathology import analyze_intracellular_calcium_with_rhod2
    if len(sys.argv) != 2:
        print("Usage: analyze_intracellular_calcium_with_rhod2.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    background_image_path = inputs['background_image_path']
    control_image_path = inputs['control_image_path']
    sample_image_path = inputs['sample_image_path']
    output_dir = inputs.get('output_dir', './output')

    result = analyze_intracellular_calcium_with_rhod2(
        background_image_path=background_image_path,
        control_image_path=control_image_path,
        sample_image_path=sample_image_path,
        output_dir=output_dir
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
