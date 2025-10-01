#!/usr/bin/env python3
"""
Create visualization of segmentation results.
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
    from biomni.tool.bioimaging import create_segmentation_visualization
    if len(sys.argv) != 2:
        print("Error: Expected config file as argument", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        config = json.load(f)

    original_mri = config['original_mri']
    segmentation = config['segmentation']
    output_dir = config.get('output_dir', './visualization_output')

    result = create_segmentation_visualization(
        original_mri=original_mri,
        segmentation=segmentation,
        output_dir=output_dir
    )

    print(json.dumps({
        "visualization_files": result,
        "status": "success"
    }))


if __name__ == '__main__':
    main()
