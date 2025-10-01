import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "matplotlib", "scikit-learn", "pykalman"])

import numpy as np



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
    from biomni.tool.bioengineering import decode_behavior_from_neural_trajectories
    parser = argparse.ArgumentParser(description='Model neural activity trajectories and decode behavioral variables')
    parser.add_argument('neural_data_file', help='Path to CSV file containing neural data (rows=timepoints, cols=neurons)')
    parser.add_argument('behavioral_data_file', help='Path to CSV file containing behavioral data (rows=timepoints, cols=variables)')
    parser.add_argument('--n-components', type=int, default=10,
                        help='Number of principal components for dimensionality reduction (default: 10)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Expand user paths if provided
    neural_data_file = os.path.expanduser(args.neural_data_file)
    behavioral_data_file = os.path.expanduser(args.behavioral_data_file)

    print(f"Loading neural data from: {neural_data_file}")
    print(f"Loading behavioral data from: {behavioral_data_file}")

    if not os.path.exists(neural_data_file):
        print(f"Error: Neural data file not found at: {neural_data_file}")
        sys.exit(1)

    if not os.path.exists(behavioral_data_file):
        print(f"Error: Behavioral data file not found at: {behavioral_data_file}")
        sys.exit(1)

    # Load data from CSV files
    try:
        import pandas as pd
        neural_df = pd.read_csv(neural_data_file)
        behavioral_df = pd.read_csv(behavioral_data_file)

        neural_data = neural_df.values
        behavioral_data = behavioral_df.values

        print(f"Neural data shape: {neural_data.shape}")
        print(f"Behavioral data shape: {behavioral_data.shape}")

        if neural_data.shape[0] != behavioral_data.shape[0]:
            print(f"Error: Neural and behavioral data must have the same number of timepoints")
            print(f"Neural: {neural_data.shape[0]}, Behavioral: {behavioral_data.shape[0]}")
            sys.exit(1)

    except Exception as e:
        print(f"Error loading data files: {e}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Run the analysis
    try:
        result = decode_behavior_from_neural_trajectories(
            neural_data=neural_data,
            behavioral_data=behavioral_data,
            n_components=args.n_components,
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

    print("\nNeural trajectory decoding analysis completed successfully!")


if __name__ == "__main__":
    main()
