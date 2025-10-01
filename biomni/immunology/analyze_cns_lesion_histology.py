#!/usr/bin/env python3
"""
Camber wrapper for analyze_cns_lesion_histology from biomni.tool.immunology
"""

import sys
import json
from biomni.tool.immunology import analyze_cns_lesion_histology



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
        print("Usage: analyze_cns_lesion_histology.py <image_path> [output_dir] [cell_markers_json] [pixel_size_um]")
        print("\ncell_markers format: JSON list of cell marker names, e.g., '[\"CD3\", \"CD8\", \"GFAP\"]'")
        sys.exit(1)

    image_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./histology_results"
    cell_markers = None
    if len(sys.argv) > 3 and sys.argv[3] != "None":
        cell_markers = json.loads(sys.argv[3])
    pixel_size_um = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5

    result = analyze_cns_lesion_histology(
        image_path=image_path,
        output_dir=output_dir,
        cell_markers=cell_markers,
        pixel_size_um=pixel_size_um
    )

    print(result)


if __name__ == "__main__":
    main()
