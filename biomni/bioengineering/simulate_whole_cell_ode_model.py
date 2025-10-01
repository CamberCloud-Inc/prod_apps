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
    parser.add_argument('input_file', help='JSON file containing input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    initial_conditions = input_data['initial_conditions']
    parameters = input_data['parameters']
    time_start = input_data.get('time_start', 0)
    time_end = input_data.get('time_end', 100)
    time_points = input_data.get('time_points', 1000)
    method = input_data.get('method', 'LSODA')

    print(f"Initial conditions: {initial_conditions}")
    print(f"Parameters: {parameters}")

    time_span = (time_start, time_end)
    print(f"Time span: {time_span}")
    print(f"Time points: {time_points}")
    print(f"Method: {method}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Run the simulation
    try:
        result = simulate_whole_cell_ode_model(
            initial_conditions=initial_conditions,
            parameters=parameters,
            ode_function=None,  # Use default whole-cell model
            time_span=time_span,
            time_points=time_points,
            method=method
        )

        # Write result to file
        output_file = os.path.join(args.output, 'whole_cell_ode_simulation_results.txt')
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")
    except Exception as e:
        print(f"Error during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
