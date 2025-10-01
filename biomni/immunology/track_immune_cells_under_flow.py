#!/usr/bin/env python3
"""
Biomni Tool: Track Immune Cells Under Flow
Wraps: biomni.tool.immunology.track_immune_cells_under_flow
"""
import argparse
import sys
import subprocess
import os
import json

def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni']
    for dep in deps:
        print(f"Installing {dep}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep])

def main():
    parser = argparse.ArgumentParser(
        description='Track Immune Cells Under Flow'
    )
    parser.add_argument('--image_sequence_path', help='Path to time-lapse microscopy images')
    parser.add_argument('--pixel_size_um', help='Physical size of each pixel in micrometers (default: 1.0)')
    parser.add_argument('--time_interval_sec', help='Time interval between frames in seconds (default: 1.0)')
    parser.add_argument('--flow_direction', help='Direction of flow in imaging field (default: right)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    from biomni.tool.immunology import track_immune_cells_under_flow

    # Parse optional parameters with defaults
    pixel_size_um = float(args.pixel_size_um) if args.pixel_size_um else 1.0
    time_interval_sec = float(args.time_interval_sec) if args.time_interval_sec else 1.0
    flow_direction = args.flow_direction if args.flow_direction else 'right'

    result = track_immune_cells_under_flow(
        image_sequence_path=args.image_sequence_path,
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

if __name__ == '__main__':
    main()
