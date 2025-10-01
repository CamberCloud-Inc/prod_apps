#!/usr/bin/env python3
"""
Wrapper for Biomni simulate_renin_angiotensin_system_dynamics tool
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
    from biomni.tool.systems_biology import simulate_renin_angiotensin_system_dynamics
    if len(sys.argv) < 4:
        print("Usage: simulate_renin_angiotensin_system_dynamics.py <initial_concentrations_json> <rate_constants_json> <feedback_params_json> [simulation_time] [time_points]")
        sys.exit(1)

    initial_concentrations = json.loads(sys.argv[1])
    rate_constants = json.loads(sys.argv[2])
    feedback_params = json.loads(sys.argv[3])
    simulation_time = float(sys.argv[4]) if len(sys.argv) > 4 else 48
    time_points = int(sys.argv[5]) if len(sys.argv) > 5 else 100

    result = simulate_renin_angiotensin_system_dynamics(
        initial_concentrations, rate_constants, feedback_params, simulation_time, time_points
    )
    print(result)

if __name__ == "__main__":
    main()
