#!/usr/bin/env python3
"""
Model bacterial population dynamics over time using ordinary differential equations.
"""

import sys
import json
from biomni.tool.microbiology import model_bacterial_growth_dynamics



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
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    initial_population = input_data.get('initial_population')
    growth_rate = input_data.get('growth_rate')
    clearance_rate = input_data.get('clearance_rate')
    niche_size = input_data.get('niche_size')
    simulation_time = input_data.get('simulation_time', 24)
    time_step = input_data.get('time_step', 0.1)

    # Call the function
    result = model_bacterial_growth_dynamics(
        initial_population=initial_population,
        growth_rate=growth_rate,
        clearance_rate=clearance_rate,
        niche_size=niche_size,
        simulation_time=simulation_time,
        time_step=time_step
    )

    # Output result as JSON
    output = {
        "research_log": result
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
