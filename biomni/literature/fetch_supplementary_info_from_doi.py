#!/usr/bin/env python3
"""
Camber wrapper for fetch_supplementary_info_from_doi from biomni.tool.literature
"""

import sys
import json
from biomni.tool.literature import fetch_supplementary_info_from_doi



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
    """Main function for Camber app execution"""
    if len(sys.argv) != 3:
        print(json.dumps({
            "error": "Usage: fetch_supplementary_info_from_doi.py <doi> <output_dir>"
        }))
        sys.exit(1)

    doi = sys.argv[1]
    output_dir = sys.argv[2]

    try:
        result = fetch_supplementary_info_from_doi(doi=doi, output_dir=output_dir)
        print(json.dumps({
            "success": True,
            "result": result
        }, indent=2))
    except Exception as e:
        print(json.dumps({
            "error": str(e)
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
