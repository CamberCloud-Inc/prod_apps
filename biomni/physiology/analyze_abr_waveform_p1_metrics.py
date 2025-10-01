#!/usr/bin/env python3
"""
Analyze ABR Waveform P1 Metrics

Extracts P1 amplitude and latency from Auditory Brainstem Response (ABR) waveform data.
"""

import argparse
import sys
import json
import os
import subprocess


def install_dependencies():
    """Install required dependencies"""
    deps = ['biomni', 'opencv-python', 'scikit-image', 'scipy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze ABR Waveform P1 Metrics'
    )
    parser.add_argument('--time-ms-file', required=True, help='File containing time values in milliseconds (JSON array or CSV)')
    parser.add_argument('--amplitude-uv-file', required=True, help='File containing amplitude values in microvolts (JSON array or CSV)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_abr_waveform_p1_metrics

    # Load time_ms data from file
    with open(args.time_ms_file, 'r') as f:
        if args.time_ms_file.endswith('.json'):
            time_ms = json.load(f)
        else:  # Assume CSV
            time_ms = [float(line.strip()) for line in f if line.strip()]

    # Load amplitude_uv data from file
    with open(args.amplitude_uv_file, 'r') as f:
        if args.amplitude_uv_file.endswith('.json'):
            amplitude_uv = json.load(f)
        else:  # Assume CSV
            amplitude_uv = [float(line.strip()) for line in f if line.strip()]

    result = analyze_abr_waveform_p1_metrics(
        time_ms=time_ms,
        amplitude_uv=amplitude_uv
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'abr_waveform_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
