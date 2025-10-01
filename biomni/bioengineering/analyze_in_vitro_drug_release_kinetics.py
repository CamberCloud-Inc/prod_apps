import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "matplotlib", "scipy"])




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
    from biomni.tool.bioengineering import analyze_in_vitro_drug_release_kinetics
    parser = argparse.ArgumentParser(description='Analyze in vitro drug release kinetics from biomaterial formulations')
    parser.add_argument('input_file', help='JSON file containing input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    time_points = input_data['time_points']
    concentration_data = input_data['concentration_data']
    drug_name = input_data.get('drug_name', 'Drug')
    total_drug_loaded = input_data.get('total_drug_loaded', None)

    print(f"Drug: {drug_name}")
    print(f"Number of time points: {len(time_points)}")
    print(f"Time range: {min(time_points)} to {max(time_points)} hours")
    print(f"Concentration range: {min(concentration_data)} to {max(concentration_data)}")

    if len(time_points) != len(concentration_data):
        print(f"Error: Number of time points ({len(time_points)}) must match concentration data points ({len(concentration_data)})")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_in_vitro_drug_release_kinetics(
            time_points=time_points,
            concentration_data=concentration_data,
            drug_name=drug_name,
            total_drug_loaded=total_drug_loaded,
            output_dir=args.output
        )

        # Write result to file
        output_file = os.path.join(args.output, 'drug_release_kinetics_results.txt')
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
