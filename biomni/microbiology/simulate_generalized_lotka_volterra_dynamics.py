#!/usr/bin/env python3
"""
Simulate microbial community dynamics using the generalized Lotka-Volterra model.
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
    from biomni.tool.microbiology import simulate_generalized_lotka_volterra_dynamics
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    initial_populations = input_data.get('initial_populations')
    growth_rates = input_data.get('growth_rates')
    interaction_matrix = input_data.get('interaction_matrix')
    simulation_time = input_data.get('simulation_time', 100)
    time_step = input_data.get('time_step', 0.1)

    # Call the function
    result = simulate_generalized_lotka_volterra_dynamics(
        initial_populations=initial_populations,
        growth_rates=growth_rates,
        interaction_matrix=interaction_matrix,
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
