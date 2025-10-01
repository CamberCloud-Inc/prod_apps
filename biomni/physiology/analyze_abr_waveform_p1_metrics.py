#!/usr/bin/env python3
"""
Analyze ABR Waveform P1 Metrics

Extracts P1 amplitude and latency from Auditory Brainstem Response (ABR) waveform data.
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
    from biomni.tool.physiology import analyze_abr_waveform_p1_metrics
    if len(sys.argv) != 2:
        print("Usage: analyze_abr_waveform_p1_metrics.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    time_ms = inputs['time_ms']
    amplitude_uv = inputs['amplitude_uv']

    result = analyze_abr_waveform_p1_metrics(
        time_ms=time_ms,
        amplitude_uv=amplitude_uv
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
