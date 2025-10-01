"""
Camber wrapper for biomni.tool.database.region_to_ccre_screen
"""

from biomni.tool.database import region_to_ccre_screen
import json



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main(coord_chrom, coord_start, coord_end, assembly="GRCh38") -> str:
    """Given starting and ending coordinates, this function retrieves information of intersecting cCREs.

    Args:
        assembly (str):
    """
    Wrapper for region_to_ccre_screen from biomni.tool.database
    
    No docstring available
    """
    result = region_to_ccre_screen(coord_chrom=coord_chrom, coord_start=coord_start, coord_end=coord_end, assembly=assembly)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description='region_to_ccre_screen')
    parser.add_argument('--coord_chrom', type=str, required=True, help='coord_chrom')
    parser.add_argument('--coord_start', type=int, required=True, help='coord_start')
    parser.add_argument('--coord_end', type=int, required=True, help='coord_end')
    parser.add_argument('--assembly', type=str, default="GRCh38") -> str:
    """Given starting and ending coordinates, this function retrieves information of intersecting cCREs.

    Args:
        assembly (str, help='assembly')
    
    args = parser.parse_args()
    main(**vars(args))
