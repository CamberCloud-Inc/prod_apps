#!/usr/bin/env python3
"""
Camber wrapper for isolate_purify_immune_cells from biomni.tool.immunology
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
        description='Generate protocol for isolating and purifying immune cells'
    )
    parser.add_argument('input_file', help='JSON file with isolation parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    tissue_type = input_data['tissue_type']
    target_cell_type = input_data['target_cell_type']
    enzyme_type = input_data.get('enzyme_type', 'collagenase')
    macs_antibody = input_data.get('macs_antibody', None)
    digestion_time_min = input_data.get('digestion_time_min', 45)

    # Import after dependencies are installed
    from biomni.tool.immunology import isolate_purify_immune_cells

    result = isolate_purify_immune_cells(
        tissue_type=tissue_type,
        target_cell_type=target_cell_type,
        enzyme_type=enzyme_type,
        macs_antibody=macs_antibody,
        digestion_time_min=digestion_time_min
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'isolation_protocol.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
