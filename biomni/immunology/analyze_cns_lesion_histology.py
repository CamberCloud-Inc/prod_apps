#!/usr/bin/env python3
"""
Camber wrapper for analyze_cns_lesion_histology from biomni.tool.immunology
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
        description='Analyze CNS lesion histology from microscopy images'
    )
    parser.add_argument('input_file', help='JSON file with analysis parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    image_path = input_data['image_path']
    cell_markers = input_data.get('cell_markers', None)
    pixel_size_um = input_data.get('pixel_size_um', 0.5)

    # Import after dependencies are installed
    from biomni.tool.immunology import analyze_cns_lesion_histology

    result = analyze_cns_lesion_histology(
        image_path=image_path,
        output_dir=args.output,
        cell_markers=cell_markers,
        pixel_size_um=pixel_size_um
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'histology_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
