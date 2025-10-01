#!/usr/bin/env python3
"""
Camber wrapper for track_immune_cells_under_flow from biomni.tool.immunology
"""

import sys
from biomni.tool.immunology import track_immune_cells_under_flow



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
    if len(sys.argv) < 2:
        print("Usage: track_immune_cells_under_flow.py <image_sequence_path> [output_dir] [pixel_size_um] [time_interval_sec] [flow_direction]")
        sys.exit(1)

    image_sequence_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./output"
    pixel_size_um = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    time_interval_sec = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
    flow_direction = sys.argv[5] if len(sys.argv) > 5 else "right"

    result = track_immune_cells_under_flow(
        image_sequence_path=image_sequence_path,
        output_dir=output_dir,
        pixel_size_um=pixel_size_um,
        time_interval_sec=time_interval_sec,
        flow_direction=flow_direction
    )

    print(result)


if __name__ == "__main__":
    main()
