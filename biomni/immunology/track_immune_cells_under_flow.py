#!/usr/bin/env python3
"""
Camber wrapper for track_immune_cells_under_flow from biomni.tool.immunology
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
        description='Track immune cells under flow conditions from microscopy images'
    )
    parser.add_argument('input_file', help='JSON file with tracking parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Load input data
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    image_sequence_path = input_data['image_sequence_path']
    pixel_size_um = input_data.get('pixel_size_um', 1.0)
    time_interval_sec = input_data.get('time_interval_sec', 1.0)
    flow_direction = input_data.get('flow_direction', 'right')

    # Import after dependencies are installed
    from biomni.tool.immunology import track_immune_cells_under_flow

    result = track_immune_cells_under_flow(
        image_sequence_path=image_sequence_path,
        output_dir=args.output,
        pixel_size_um=pixel_size_um,
        time_interval_sec=time_interval_sec,
        flow_direction=flow_direction
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'tracking_results.txt')
    with open(output_file, 'w') as f:
        f.write(result)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
