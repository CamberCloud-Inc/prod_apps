#!/usr/bin/env python3
"""Biomni Tool: Bayesian Fine-mapping with Deep VI
Wraps: biomni.tool.genetics.bayesian_finemapping_with_deep_vi
"""
import subprocess
import sys
import argparse
import os

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "torch", "numpy", "pandas", "scipy", "matplotlib"])

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
    from biomni.tool.genetics import bayesian_finemapping_with_deep_vi
    parser = argparse.ArgumentParser(description='Bayesian fine-mapping from GWAS summary statistics using deep variational inference')
    parser.add_argument('gwas_summary', help='Path to GWAS summary statistics file (CSV or TSV)')
    parser.add_argument('ld_matrix', help='Path to LD matrix file (numpy .npy format)')
    parser.add_argument('-n', '--n-iterations', type=int, default=5000,
                        help='Number of training iterations (default: 5000)')
    parser.add_argument('-lr', '--learning-rate', type=float, default=0.01,
                        help='Learning rate for optimization (default: 0.01)')
    parser.add_argument('-hd', '--hidden-dim', type=int, default=64,
                        help='Hidden dimension size for neural network (default: 64)')
    parser.add_argument('-ct', '--credible-threshold', type=float, default=0.95,
                        help='Threshold for credible set (default: 0.95)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    print(f"Starting Bayesian fine-mapping analysis...")
    print(f"GWAS summary file: {args.gwas_summary}")
    print(f"LD matrix file: {args.ld_matrix}")
    print(f"Parameters: n_iterations={args.n_iterations}, learning_rate={args.learning_rate}")
    print(f"Hidden dimension: {args.hidden_dim}, credible threshold: {args.credible_threshold}")

    try:
        # Load LD matrix
        print("\nLoading LD matrix...")
        ld_matrix = np.load(args.ld_matrix)
        print(f"LD matrix shape: {ld_matrix.shape}")

        # Create output directory
        os.makedirs(args.output, exist_ok=True)
        os.chdir(args.output)

        result = bayesian_finemapping_with_deep_vi(
            gwas_summary_path=args.gwas_summary,
            ld_matrix=ld_matrix,
            n_iterations=args.n_iterations,
            learning_rate=args.learning_rate,
            hidden_dim=args.hidden_dim,
            credible_threshold=args.credible_threshold
        )

        # Save full results to log file
        output_file = os.path.join(args.output, "bayesian_finemapping_log.txt")
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")

    except Exception as e:
        print(f"Error during Bayesian fine-mapping analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
