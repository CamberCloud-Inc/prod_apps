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
    deps = ['biomni', 'nibabel']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Preprocess medical images with denoising and normalization'
    )
    parser.add_argument('--image_path', required=True, help='Path to the input medical image file')
    parser.add_argument('--output_path', required=True, help='Path where the preprocessed image will be saved')
    parser.add_argument('--denoise', type=lambda x: x.lower() == 'true', default=True, help='Enable denoising')
    parser.add_argument('--normalize', type=lambda x: x.lower() == 'true', default=True, help='Enable normalization')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import preprocess_image

    result = preprocess_image(
        image_path=args.image_path,
        output_path=args.output_path,
        denoise=args.denoise,
        normalize=args.normalize
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
