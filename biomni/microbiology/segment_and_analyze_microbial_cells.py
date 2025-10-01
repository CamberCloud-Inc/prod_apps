#!/usr/bin/env python3
"""
Segment and analyze microbial cells in microscopy images using image processing techniques.
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
    from biomni.tool.microbiology import segment_and_analyze_microbial_cells
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    image_path = input_data.get('image_path')
    output_dir = input_data.get('output_dir', './output')
    min_cell_size = input_data.get('min_cell_size', 50)
    max_cell_size = input_data.get('max_cell_size', 5000)

    # Call the function
    result = segment_and_analyze_microbial_cells(
        image_path=image_path,
        output_dir=output_dir,
        min_cell_size=min_cell_size,
        max_cell_size=max_cell_size
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
