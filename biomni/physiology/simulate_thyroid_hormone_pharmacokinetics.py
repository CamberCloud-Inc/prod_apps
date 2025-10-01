#!/usr/bin/env python3
"""
Simulate Thyroid Hormone Pharmacokinetics

Simulates the transport and binding of thyroid hormones across different tissue compartments
using an ODE-based pharmacokinetic model.
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
    from biomni.tool.physiology import simulate_thyroid_hormone_pharmacokinetics
    if len(sys.argv) != 2:
        print("Usage: simulate_thyroid_hormone_pharmacokinetics.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    parameters = inputs['parameters']
    initial_conditions = inputs['initial_conditions']
    time_span = inputs.get('time_span', [0, 24])
    time_points = inputs.get('time_points', 100)

    result = simulate_thyroid_hormone_pharmacokinetics(
        parameters=parameters,
        initial_conditions=initial_conditions,
        time_span=tuple(time_span),
        time_points=time_points
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
