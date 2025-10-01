import subprocess
import sys
import argparse

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "biopython", "matplotlib", "numpy"])

from biomni.tool.genetics import perform_pcr_and_gel_electrophoresis



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
    parser = argparse.ArgumentParser(description='Simulate PCR amplification and gel electrophoresis')
    parser.add_argument('genomic_dna', help='Path to genomic DNA FASTA file or DNA sequence string')
    parser.add_argument('-f', '--forward-primer', help='Forward primer sequence (optional)')
    parser.add_argument('-r', '--reverse-primer', help='Reverse primer sequence (optional)')
    parser.add_argument('-t', '--target-region', help='Target region as "start,end" (optional)')
    parser.add_argument('-a', '--annealing-temp', type=float, default=58,
                        help='Annealing temperature in °C (default: 58)')
    parser.add_argument('-e', '--extension-time', type=int, default=30,
                        help='Extension time in seconds (default: 30)')
    parser.add_argument('-c', '--cycles', type=int, default=35,
                        help='Number of PCR cycles (default: 35)')
    parser.add_argument('-g', '--gel-percentage', type=float, default=2.0,
                        help='Agarose gel percentage (default: 2.0)')
    parser.add_argument('-p', '--output-prefix', default='pcr_result',
                        help='Prefix for output files (default: pcr_result)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    print(f"Starting PCR and gel electrophoresis simulation...")
    print(f"Genomic DNA: {args.genomic_dna}")
    print(f"PCR parameters:")
    print(f"  Annealing temperature: {args.annealing_temp}°C")
    print(f"  Extension time: {args.extension_time}s")
    print(f"  Cycles: {args.cycles}")
    print(f"  Gel percentage: {args.gel_percentage}%")

    try:
        import os

        # Parse target region if provided
        target_region = None
        if args.target_region:
            parts = args.target_region.split(',')
            if len(parts) == 2:
                target_region = (int(parts[0]), int(parts[1]))
                print(f"  Target region: {target_region}")

        # Set up output directory
        os.makedirs(args.output_dir, exist_ok=True)
        output_prefix = os.path.join(args.output_dir, args.output_prefix)

        result = perform_pcr_and_gel_electrophoresis(
            genomic_dna=args.genomic_dna,
            forward_primer=args.forward_primer,
            reverse_primer=args.reverse_primer,
            target_region=target_region,
            annealing_temp=args.annealing_temp,
            extension_time=args.extension_time,
            cycles=args.cycles,
            gel_percentage=args.gel_percentage,
            output_prefix=output_prefix
        )

        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        print(result)

        # Save log to file
        log_file = os.path.join(args.output_dir, f"{args.output_prefix}_log.txt")
        with open(log_file, 'w') as f:
            f.write(result)

        print(f"\nAnalysis log saved to: {log_file}")

    except Exception as e:
        print(f"Error during PCR and gel electrophoresis simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nPCR and gel electrophoresis simulation completed!")


if __name__ == "__main__":
    main()
