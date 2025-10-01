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
    deps = ['biomni']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze ABR Waveform P1 Metrics'
    )
    parser.add_argument('input_file', help='Input JSON file with time_ms and amplitude_uv')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_abr_waveform_p1_metrics

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    time_ms = inputs['time_ms']
    amplitude_uv = inputs['amplitude_uv']

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
