import json
import sys
import os
import argparse



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
    from biomni.tool.molecular_biology import align_sequences
    parser = argparse.ArgumentParser(description='Align short sequences (primers) to a longer sequence')
    parser.add_argument('long_seq', help='Target DNA sequence')
    parser.add_argument('short_seqs', nargs='+', help='One or more short sequences to align')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nAligning sequences...")
    print(f"Target sequence length: {len(args.long_seq)} bp")
    print(f"Number of sequences to align: {len(args.short_seqs)}")

    try:
        result = align_sequences(args.long_seq, args.short_seqs)

        # Generate output filename
        output_filename = "alignment_results.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")
        for seq_result in result.get('sequences', []):
            print(f"Sequence: {seq_result['sequence']} - {len(seq_result['alignments'])} alignments found")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nSequence alignment completed successfully!")


if __name__ == "__main__":
    main()
