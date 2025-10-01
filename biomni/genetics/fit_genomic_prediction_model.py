import subprocess
import sys
import argparse

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "scipy"])

from biomni.tool.genetics import fit_genomic_prediction_model
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
    parser = argparse.ArgumentParser(description='Fit linear mixed model for genomic prediction')
    parser.add_argument('genotypes', help='Path to genotype data file (numpy .npy format)')
    parser.add_argument('phenotypes', help='Path to phenotype data file (numpy .npy format)')
    parser.add_argument('-f', '--fixed-effects', help='Path to fixed effects file (numpy .npy format, optional)')
    parser.add_argument('-m', '--model-type', default='additive',
                        choices=['additive', 'additive_dominance'],
                        help='Type of genetic model (default: additive)')
    parser.add_argument('-p', '--output-file', default='genomic_prediction_results.csv',
                        help='Output filename for results (default: genomic_prediction_results.csv)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    print(f"Starting genomic prediction model fitting...")
    print(f"Genotypes file: {args.genotypes}")
    print(f"Phenotypes file: {args.phenotypes}")
    print(f"Model type: {args.model_type}")

    try:
        import os

        # Load genotype data
        print("\nLoading genotype data...")
        genotypes = np.load(args.genotypes)
        print(f"Genotype matrix shape: {genotypes.shape}")
        print(f"  - Individuals: {genotypes.shape[0]}")
        print(f"  - Markers: {genotypes.shape[1]}")

        # Load phenotype data
        print("\nLoading phenotype data...")
        phenotypes = np.load(args.phenotypes)
        print(f"Phenotype data shape: {phenotypes.shape}")

        # Load fixed effects if provided
        fixed_effects = None
        if args.fixed_effects:
            print("\nLoading fixed effects data...")
            fixed_effects = np.load(args.fixed_effects)
            print(f"Fixed effects shape: {fixed_effects.shape}")

        # Set up output directory
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = os.path.join(args.output_dir, args.output_file)

        result = fit_genomic_prediction_model(
            genotypes=genotypes,
            phenotypes=phenotypes,
            fixed_effects=fixed_effects,
            model_type=args.model_type,
            output_file=output_file
        )

        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        print(result)

        # Save log to file
        log_file = os.path.join(args.output_dir, "genomic_prediction_log.txt")
        with open(log_file, 'w') as f:
            f.write(result)

        print(f"\nAnalysis log saved to: {log_file}")
        print(f"Results CSV saved to: {output_file}")

    except Exception as e:
        print(f"Error during genomic prediction model fitting: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nGenomic prediction model fitting completed!")


if __name__ == "__main__":
    main()
