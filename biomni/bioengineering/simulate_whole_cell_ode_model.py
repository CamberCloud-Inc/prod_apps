import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "scipy"])




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
    from biomni.tool.bioengineering import simulate_whole_cell_ode_model
    parser = argparse.ArgumentParser(description='Simulate a whole-cell model using ordinary differential equations')
    parser.add_argument('initial_conditions', help='JSON string of initial conditions (e.g., {"mRNA":1.0,"protein":0.5,"metabolite":2.0,"atp":5.0})')
    parser.add_argument('parameters', help='JSON string of model parameters (e.g., {"k_transcription":0.5,"k_translation":0.1,...})')
    parser.add_argument('--time-start', type=float, default=0,
                        help='Start time for simulation (default: 0)')
    parser.add_argument('--time-end', type=float, default=100,
                        help='End time for simulation (default: 100)')
    parser.add_argument('--time-points', type=int, default=1000,
                        help='Number of time points to evaluate (default: 1000)')
    parser.add_argument('--method', default='LSODA',
                        choices=['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA'],
                        help='Numerical integration method (default: LSODA)')

    args = parser.parse_args()

    # Parse initial conditions JSON
    try:
        initial_conditions = json.loads(args.initial_conditions)
        print(f"Initial conditions: {initial_conditions}")
    except json.JSONDecodeError as e:
        print(f"Error parsing initial conditions JSON: {e}")
        sys.exit(1)

    # Parse parameters JSON
    try:
        parameters = json.loads(args.parameters)
        print(f"Parameters: {parameters}")
    except json.JSONDecodeError as e:
        print(f"Error parsing parameters JSON: {e}")
        sys.exit(1)

    time_span = (args.time_start, args.time_end)
    print(f"Time span: {time_span}")
    print(f"Time points: {args.time_points}")
    print(f"Method: {args.method}")
    print("\n" + "="*80)

    # Run the simulation
    try:
        result = simulate_whole_cell_ode_model(
            initial_conditions=initial_conditions,
            parameters=parameters,
            ode_function=None,  # Use default whole-cell model
            time_span=time_span,
            time_points=args.time_points,
            method=args.method
        )
        print(result)
    except Exception as e:
        print(f"Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "="*80)
    print("Whole-cell ODE model simulation completed successfully!")


if __name__ == "__main__":
    main()
