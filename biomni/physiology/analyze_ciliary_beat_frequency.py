#!/usr/bin/env python3
"""
Analyze Ciliary Beat Frequency

Analyze ciliary beat frequency from high-speed video microscopy data using FFT analysis.
"""

import sys
import json
from biomni.tool.physiology import analyze_ciliary_beat_frequency



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
    if len(sys.argv) != 2:
        print("Usage: analyze_ciliary_beat_frequency.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
