#!/usr/bin/env python3
"""
Preprocess medical images with denoising and normalization.
"""

import argparse
import sys
import json
import os



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
    parser = argparse.ArgumentParser(
        description='Preprocess medical images with denoising and normalization'
    )
    parser.add_argument('input_file', help='JSON config file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import preprocess_image

    with open(args.input_file, 'r') as f:
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

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'preprocessing_results.json')
    with open(output_file, 'w') as f:
        json.dump({
            "output_path": result,
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
