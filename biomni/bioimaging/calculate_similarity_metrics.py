#!/usr/bin/env python3
"""
Calculate similarity metrics between two medical images.
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
        description='Calculate similarity metrics between two medical images'
    )
    parser.add_argument('input_file', help='JSON config file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import calculate_similarity_metrics

    with open(args.input_file, 'r') as f:
        config = json.load(f)

    image1_path = config['image1_path']
    image2_path = config['image2_path']

    result = calculate_similarity_metrics(
        image1_path=image1_path,
        image2_path=image2_path
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'similarity_metrics.json')
    with open(output_file, 'w') as f:
        json.dump({
            "metrics": result,
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
