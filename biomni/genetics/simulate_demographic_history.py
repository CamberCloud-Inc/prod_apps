import subprocess
import sys
import argparse
import json

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "msprime"])




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
    from biomni.tool.genetics import simulate_demographic_history
    parser = argparse.ArgumentParser(description='Simulate DNA sequences with demographic and coalescent histories')
    parser.add_argument('-n', '--num-samples', type=int, default=10,
                        help='Number of sample sequences to simulate (default: 10)')
    parser.add_argument('-l', '--sequence-length', type=int, default=100000,
                        help='Length of simulated sequence in base pairs (default: 100000)')
    parser.add_argument('-r', '--recombination-rate', type=float, default=1e-8,
                        help='Per-base recombination rate (default: 1e-8)')
    parser.add_argument('-m', '--mutation-rate', type=float, default=1e-8,
                        help='Per-base mutation rate (default: 1e-8)')
    parser.add_argument('-d', '--demographic-model', default='constant',
                        choices=['constant', 'bottleneck', 'expansion', 'contraction', 'sawtooth'],
                        help='Type of demographic model (default: constant)')
    parser.add_argument('-p', '--demographic-params', help='Path to JSON file with demographic parameters (optional)')
    parser.add_argument('-c', '--coalescent-model', default='kingman',
                        choices=['kingman', 'beta'],
                        help='Type of coalescent model (default: kingman)')
    parser.add_argument('-b', '--beta-param', type=float, help='Beta-coalescent parameter (required if coalescent-model=beta)')
    parser.add_argument('-s', '--random-seed', type=int, help='Random seed for reproducibility (optional)')
    parser.add_argument('-f', '--output-file', default='simulated_sequences.vcf',
                        help='Output filename for VCF (default: simulated_sequences.vcf)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    print(f"Starting demographic history simulation...")
    print(f"Parameters:")
    print(f"  Number of samples: {args.num_samples}")
    print(f"  Sequence length: {args.sequence_length} bp")
    print(f"  Recombination rate: {args.recombination_rate}")
    print(f"  Mutation rate: {args.mutation_rate}")
    print(f"  Demographic model: {args.demographic_model}")
    print(f"  Coalescent model: {args.coalescent_model}")

    try:
        import os

        # Load demographic parameters if provided
        demographic_params = None
        if args.demographic_params:
            print(f"Loading demographic parameters from: {args.demographic_params}")
            with open(args.demographic_params, 'r') as f:
                demographic_params = json.load(f)

        # Change to output directory
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = os.path.join(args.output_dir, args.output_file)

        result = simulate_demographic_history(
            num_samples=args.num_samples,
            sequence_length=args.sequence_length,
            recombination_rate=args.recombination_rate,
            mutation_rate=args.mutation_rate,
            demographic_model=args.demographic_model,
            demographic_params=demographic_params,
            coalescent_model=args.coalescent_model,
            beta_coalescent_param=args.beta_param,
            random_seed=args.random_seed,
            output_file=output_file
        )

        print("\n" + "="*80)
        print("SIMULATION RESULTS")
        print("="*80)
        print(result)

        # Save log to file
        log_file = os.path.join(args.output_dir, "demographic_simulation_log.txt")
        with open(log_file, 'w') as f:
            f.write(result)

        print(f"\nSimulation log saved to: {log_file}")

    except Exception as e:
        print(f"Error during demographic history simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nDemographic history simulation completed!")


if __name__ == "__main__":
    main()
