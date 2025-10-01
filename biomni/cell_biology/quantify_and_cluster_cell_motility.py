#!/usr/bin/env python3
"""
Camber wrapper for quantify_and_cluster_cell_motility from Biomni
"""

import argparse
import json
import os
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
    parser = argparse.ArgumentParser(
        description='Quantify and cluster cell motility'
    )
    parser.add_argument('input_file', help='JSON file with input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cell_biology import quantify_and_cluster_cell_motility

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    # Extract parameters
    image_sequence_path = input_data.get("image_sequence_path", "")
    output_dir = input_data.get("output_dir", "./results")
    num_clusters = input_data.get("num_clusters", 3)

    # Call the function
    result = quantify_and_cluster_cell_motility(
        image_sequence_path=image_sequence_path,
        output_dir=output_dir,
        num_clusters=num_clusters
    )

    # Create output directory and write result
    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'result.json')

    output = {
        "research_log": result
    }

    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
