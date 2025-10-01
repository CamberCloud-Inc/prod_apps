#!/usr/bin/env python3
"""
Camber wrapper for analyze_cytokine_production_in_cd4_tcells from biomni.tool.immunology
"""

import sys
import json
from biomni.tool.immunology import analyze_cytokine_production_in_cd4_tcells



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
        print("Usage: analyze_cytokine_production_in_cd4_tcells.py <fcs_files_dict_json> [output_dir]")
        print("\nfcs_files_dict format: JSON string mapping condition names to FCS file paths")
        print("Example: '{\"control\": \"/path/to/control.fcs\", \"stimulated\": \"/path/to/stimulated.fcs\"}'")
        sys.exit(1)

    fcs_files_dict = json.loads(sys.argv[1])
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "./results"

    result = analyze_cytokine_production_in_cd4_tcells(
        fcs_files_dict=fcs_files_dict,
        output_dir=output_dir
    )

    print(result)


if __name__ == "__main__":
    main()
