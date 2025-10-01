#!/usr/bin/env python3
"""
Count bacterial colonies from an image of agar plate using computer vision techniques.
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
    from biomni.tool.microbiology import count_bacterial_colonies
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    image_path = input_data.get('image_path')
    dilution_factor = input_data.get('dilution_factor', 1)
    plate_area_cm2 = input_data.get('plate_area_cm2', 65.0)
    output_dir = input_data.get('output_dir', './output')

    # Call the function
    result = count_bacterial_colonies(
        image_path=image_path,
        dilution_factor=dilution_factor,
        plate_area_cm2=plate_area_cm2,
        output_dir=output_dir
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
