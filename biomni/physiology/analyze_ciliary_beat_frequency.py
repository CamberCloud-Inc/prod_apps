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
    deps = ['biomni', 'cv2', 'opencv-python', 'scikit-image', 'scipy']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Analyze Ciliary Beat Frequency'
    )
    parser.add_argument('--video-path', required=True, help='Path to high-speed video microscopy file')
    parser.add_argument('--roi-count', type=int, default=5, help='Number of regions of interest to analyze (default: 5)')
    parser.add_argument('--min-freq', type=float, default=0, help='Minimum frequency in Hz (default: 0)')
    parser.add_argument('--max-freq', type=float, default=30, help='Maximum frequency in Hz (default: 30)')
    parser.add_argument('--output-dir', default='./', help='Directory for output files (default: ./)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.physiology import analyze_ciliary_beat_frequency

    result = analyze_ciliary_beat_frequency(
        video_path=args.video_path,
        roi_count=args.roi_count,
        min_freq=args.min_freq,
        max_freq=args.max_freq,
        output_dir=args.output_dir
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'ciliary_beat_frequency_results.json')
    with open(output_file, 'w') as f:
        json.dump({"result": result}, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == "__main__":
    main()
