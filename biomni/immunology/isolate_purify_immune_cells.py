#!/usr/bin/env python3
"""
Camber wrapper for isolate_purify_immune_cells from biomni.tool.immunology
"""

import sys
from biomni.tool.immunology import isolate_purify_immune_cells



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
    if len(sys.argv) < 3:
        print("Usage: isolate_purify_immune_cells.py <tissue_type> <target_cell_type> [enzyme_type] [macs_antibody] [digestion_time_min]")
        sys.exit(1)

    tissue_type = sys.argv[1]
    target_cell_type = sys.argv[2]
    enzyme_type = sys.argv[3] if len(sys.argv) > 3 else "collagenase"
    macs_antibody = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != "None" else None
    digestion_time_min = int(sys.argv[5]) if len(sys.argv) > 5 else 45

    result = isolate_purify_immune_cells(
        tissue_type=tissue_type,
        target_cell_type=target_cell_type,
        enzyme_type=enzyme_type,
        macs_antibody=macs_antibody,
        digestion_time_min=digestion_time_min
    )

    print(result)


if __name__ == "__main__":
    main()
