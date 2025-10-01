#!/usr/bin/env python3
"""
Simulate microbial population dynamics with multiple interacting species.
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
    from biomni.tool.microbiology import simulate_microbial_population_dynamics
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    species_params = input_data.get('species_params')
    interactions = input_data.get('interactions')
    simulation_time = input_data.get('simulation_time', 100)
    time_step = input_data.get('time_step', 0.1)

    # Call the function
    result = simulate_microbial_population_dynamics(
        species_params=species_params,
        interactions=interactions,
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
