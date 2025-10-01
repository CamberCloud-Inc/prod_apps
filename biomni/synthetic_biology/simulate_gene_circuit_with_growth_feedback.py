#!/usr/bin/env python3
"""
Camber app wrapper for simulate_gene_circuit_with_growth_feedback from biomni.tool.synthetic_biology
"""

import sys
import json
import numpy as np
from biomni.tool.synthetic_biology import simulate_gene_circuit_with_growth_feedback



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
    """Main function for Camber app wrapper"""
    # Read input from stdin
    input_data = json.loads(sys.stdin.read())

    # Extract parameters
    circuit_topology = np.array(input_data.get("circuit_topology"))
    kinetic_params = input_data.get("kinetic_params")
    growth_params = input_data.get("growth_params")
    simulation_time = input_data.get("simulation_time", 100)
    time_points = input_data.get("time_points", 1000)

    # Call the function
    result = simulate_gene_circuit_with_growth_feedback(
        circuit_topology=circuit_topology,
        kinetic_params=kinetic_params,
        growth_params=growth_params,
        simulation_time=simulation_time,
        time_points=time_points
    )

    # Output result
    print(result)


if __name__ == "__main__":
    main()
