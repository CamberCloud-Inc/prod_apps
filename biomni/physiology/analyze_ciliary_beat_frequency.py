#!/usr/bin/env python3
"""
Analyze Ciliary Beat Frequency

Analyze ciliary beat frequency from high-speed video microscopy data using FFT analysis.
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
        description='Analyze Ciliary Beat Frequency'
    )
    parser.add_argument('input_file', help='Input JSON file with video_path and optional parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_ciliary_beat_frequency

    with open(args.input_file, 'r') as f:
        inputs = json.load(f)

    video_path = inputs['video_path']
    roi_count = inputs.get('roi_count', 5)
    min_freq = inputs.get('min_freq', 0)
    max_freq = inputs.get('max_freq', 30)
    output_dir = inputs.get('output_dir', './')

    result = analyze_ciliary_beat_frequency(
        video_path=video_path,
        roi_count=roi_count,
        min_freq=min_freq,
        max_freq=max_freq,
        output_dir=output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'ciliary_beat_frequency_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
