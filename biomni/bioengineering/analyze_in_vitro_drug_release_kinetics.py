import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "matplotlib", "scipy"])

from biomni.tool.bioengineering import analyze_in_vitro_drug_release_kinetics



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
    parser = argparse.ArgumentParser(description='Analyze in vitro drug release kinetics from biomaterial formulations')
    parser.add_argument('time_points', help='JSON string or comma-separated list of time points (hours)')
    parser.add_argument('concentration_data', help='JSON string or comma-separated list of drug concentrations')
    parser.add_argument('--drug-name', default='Drug',
                        help='Name of the drug being analyzed (default: Drug)')
    parser.add_argument('--total-drug-loaded', type=float, default=None,
                        help='Total amount of drug initially loaded. If not provided, max concentration is used as 100%%')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Parse time points (either JSON or comma-separated)
    try:
        time_points = json.loads(args.time_points)
    except json.JSONDecodeError:
        time_points = [float(t.strip()) for t in args.time_points.split(',')]

    # Parse concentration data (either JSON or comma-separated)
    try:
        concentration_data = json.loads(args.concentration_data)
    except json.JSONDecodeError:
        concentration_data = [float(c.strip()) for c in args.concentration_data.split(',')]

    print(f"Drug: {args.drug_name}")
    print(f"Number of time points: {len(time_points)}")
    print(f"Time range: {min(time_points)} to {max(time_points)} hours")
    print(f"Concentration range: {min(concentration_data)} to {max(concentration_data)}")

    if len(time_points) != len(concentration_data):
        print(f"Error: Number of time points ({len(time_points)}) must match concentration data points ({len(concentration_data)})")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_in_vitro_drug_release_kinetics(
            time_points=time_points,
            concentration_data=concentration_data,
            drug_name=args.drug_name,
            total_drug_loaded=args.total_drug_loaded,
            output_dir=args.output_dir
        )
        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        print(result)
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nDrug release kinetics analysis completed successfully!")


if __name__ == "__main__":
    main()
