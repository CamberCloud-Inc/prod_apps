#!/usr/bin/env python3
"""
Camber wrapper for analyze_cfse_cell_proliferation from biomni.tool.immunology
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
    from biomni.tool.immunology import analyze_cfse_cell_proliferation
    if len(sys.argv) < 2:
        print("Usage: analyze_cfse_cell_proliferation.py <fcs_file_path> [cfse_channel] [lymphocyte_gate_json]")
        print("\nlymphocyte_gate format: JSON string of dict with 'fsc' and 'ssc' keys, e.g., '{\"fsc\": [50000, 250000], \"ssc\": [0, 200000]}'")
        sys.exit(1)

    fcs_file_path = sys.argv[1]
    cfse_channel = sys.argv[2] if len(sys.argv) > 2 else "FL1-A"
    lymphocyte_gate = None
    if len(sys.argv) > 3 and sys.argv[3] != "None":
        lymphocyte_gate = json.loads(sys.argv[3])

    result = analyze_cfse_cell_proliferation(
        fcs_file_path=fcs_file_path,
        cfse_channel=cfse_channel,
        lymphocyte_gate=lymphocyte_gate
    )

    print(result)


if __name__ == "__main__":
    main()
