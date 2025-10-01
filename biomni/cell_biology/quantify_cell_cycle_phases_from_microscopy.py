#!/usr/bin/env python3
"""
Camber wrapper for quantify_cell_cycle_phases_from_microscopy from Biomni
"""

import json
import sys




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
    from biomni.tool.cell_biology import quantify_cell_cycle_phases_from_microscopy
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    image_paths = input_data.get("image_paths", [])
    output_dir = input_data.get("output_dir", "./results")

    # Call the function
    result = quantify_cell_cycle_phases_from_microscopy(
        image_paths=image_paths,
        output_dir=output_dir
    )

    # Output result as JSON
    output = {
        "research_log": result
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
