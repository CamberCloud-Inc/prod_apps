import subprocess
import sys
import argparse

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "biopython"])

from biomni.tool.genetics import analyze_crispr_genome_editing



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
    parser = argparse.ArgumentParser(description='Analyze CRISPR-Cas9 genome editing results')
    parser.add_argument('original_sequence', help='Path to file with original DNA sequence or sequence string')
    parser.add_argument('edited_sequence', help='Path to file with edited DNA sequence or sequence string')
    parser.add_argument('guide_rna', help='CRISPR guide RNA (crRNA) sequence')
    parser.add_argument('-r', '--repair-template', help='Homology-directed repair template sequence (optional)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    print(f"Starting CRISPR-Cas9 genome editing analysis...")
    print(f"Guide RNA: {args.guide_rna}")

    try:
        import os

        # Check if inputs are files or sequences
        if os.path.isfile(args.original_sequence):
            print(f"Loading original sequence from file: {args.original_sequence}")
            with open(args.original_sequence, 'r') as f:
                original_seq = f.read().strip()
        else:
            original_seq = args.original_sequence

        if os.path.isfile(args.edited_sequence):
            print(f"Loading edited sequence from file: {args.edited_sequence}")
            with open(args.edited_sequence, 'r') as f:
                edited_seq = f.read().strip()
        else:
            edited_seq = args.edited_sequence

        # Load repair template if provided
        repair_template = None
        if args.repair_template:
            if os.path.isfile(args.repair_template):
                print(f"Loading repair template from file: {args.repair_template}")
                with open(args.repair_template, 'r') as f:
                    repair_template = f.read().strip()
            else:
                repair_template = args.repair_template

        print(f"Original sequence length: {len(original_seq)} bp")
        print(f"Edited sequence length: {len(edited_seq)} bp")

        result = analyze_crispr_genome_editing(
            original_sequence=original_seq,
            edited_sequence=edited_seq,
            guide_rna=args.guide_rna,
            repair_template=repair_template
        )

        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        print(result)

        # Save results to file
        os.makedirs(args.output_dir, exist_ok=True)
        output_file = os.path.join(args.output_dir, "crispr_editing_analysis.txt")
        with open(output_file, 'w') as f:
            f.write(result)

        print(f"\nResults saved to: {output_file}")

    except Exception as e:
        print(f"Error during CRISPR genome editing analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nCRISPR-Cas9 genome editing analysis completed!")


if __name__ == "__main__":
    main()
