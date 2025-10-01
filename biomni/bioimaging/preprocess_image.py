#!/usr/bin/env python3
"""
Preprocess medical images with denoising and normalization.
"""

import sys
import json
from biomni.tool.bioimaging import preprocess_image



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
        print("Error: Expected config file as argument", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        config = json.load(f)

    image_path = config['image_path']
    output_path = config['output_path']
    denoise = config.get('denoise', True)
    normalize = config.get('normalize', True)

    result = preprocess_image(
        image_path=image_path,
        output_path=output_path,
        denoise=denoise,
        normalize=normalize
    )

    print(json.dumps({
        "output_path": result,
        "status": "success"
    }))


if __name__ == '__main__':
    main()
