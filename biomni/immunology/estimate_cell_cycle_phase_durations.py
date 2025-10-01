#!/usr/bin/env python3
"""
Camber wrapper for estimate_cell_cycle_phase_durations from biomni.tool.immunology
"""

import sys
import json
from biomni.tool.immunology import estimate_cell_cycle_phase_durations



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
        print("Usage: estimate_cell_cycle_phase_durations.py <flow_cytometry_data_json> <initial_estimates_json>")
        print("\nflow_cytometry_data format: {\"time_points\": [...], \"edu_positive\": [...], \"brdu_positive\": [...], \"double_positive\": [...]}")
        print("initial_estimates format: {\"g1_duration\": ..., \"s_duration\": ..., \"g2m_duration\": ..., \"death_rate\": ...}")
        sys.exit(1)

    flow_cytometry_data = json.loads(sys.argv[1])
    initial_estimates = json.loads(sys.argv[2])

    result = estimate_cell_cycle_phase_durations(
        flow_cytometry_data=flow_cytometry_data,
        initial_estimates=initial_estimates
    )

    print(result)


if __name__ == "__main__":
    main()
