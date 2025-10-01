#!/usr/bin/env python3
"""
Camber wrapper for analyze_ebv_antibody_titers from biomni.tool.immunology
"""

import sys
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

def main():
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.immunology import analyze_ebv_antibody_titers
    if len(sys.argv) < 2:
        print("Usage: analyze_ebv_antibody_titers.py <sample_data_json> [output_dir]")
        print("\nsample_data format: JSON string of list containing dicts with keys: sample_id, vca_igg_od, ea_igg_od, ebna_igg_od")
        print("Example: '[{\"sample_id\": \"S001\", \"vca_igg_od\": 0.8, \"ea_igg_od\": 0.3, \"ebna_igg_od\": 1.2}]'")
        sys.exit(1)

    sample_data = json.loads(sys.argv[1])
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    result = analyze_ebv_antibody_titers(
        sample_data=sample_data,
        output_dir=output_dir
    )

    print(result)


if __name__ == "__main__":
    main()
