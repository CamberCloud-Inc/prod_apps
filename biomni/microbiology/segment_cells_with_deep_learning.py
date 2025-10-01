#!/usr/bin/env python3
"""
Segment cells in microscopy images using deep learning models.
"""

import sys
import json
from biomni.tool.microbiology import segment_cells_with_deep_learning



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
    image_path = input_data.get('image_path')
    model_type = input_data.get('model_type', 'cellpose')
    output_dir = input_data.get('output_dir', './output')

    # Call the function
    result = segment_cells_with_deep_learning(
        image_path=image_path,
        model_type=model_type,
        output_dir=output_dir
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
