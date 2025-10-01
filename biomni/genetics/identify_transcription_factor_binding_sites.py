import subprocess
import sys
import argparse

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "biopython", "requests"])




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
    from biomni.tool.genetics import identify_transcription_factor_binding_sites
    parser = argparse.ArgumentParser(description='Identify transcription factor binding sites in genomic sequences')
    parser.add_argument('sequence', help='Path to file with genomic DNA sequence or sequence string')
    parser.add_argument('tf_name', help='Name of transcription factor (e.g., "Hsf1", "GATA1")')
    parser.add_argument('-t', '--threshold', type=float, default=0.8,
                        help='Minimum score threshold for binding sites (0.0-1.0, default: 0.8)')
    parser.add_argument('-f', '--output-file', help='Path to save results (optional)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    print(f"Starting transcription factor binding site analysis...")
    print(f"Transcription factor: {args.tf_name}")
    print(f"Threshold: {args.threshold}")

    try:
        import os

        # Check if input is file or sequence
        if os.path.isfile(args.sequence):
            print(f"Loading sequence from file: {args.sequence}")
            with open(args.sequence, 'r') as f:
                sequence = f.read().strip()
        else:
            sequence = args.sequence

        print(f"Sequence length: {len(sequence)} bp")

        # Set up output file path
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = None
        if args.output_file:
            output_file = os.path.join(args.output_dir, args.output_file)
        else:
            output_file = os.path.join(args.output_dir, f"{args.tf_name}_binding_sites.tsv")

        result = identify_transcription_factor_binding_sites(
            sequence=sequence,
            tf_name=args.tf_name,
            threshold=args.threshold,
            output_file=output_file
        )

        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        print(result)

        # Save log to file
        log_file = os.path.join(args.output_dir, f"{args.tf_name}_tfbs_analysis_log.txt")
        with open(log_file, 'w') as f:
            f.write(result)

        print(f"\nAnalysis log saved to: {log_file}")

    except Exception as e:
        print(f"Error during transcription factor binding site analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nTranscription factor binding site analysis completed!")


if __name__ == "__main__":
    main()
