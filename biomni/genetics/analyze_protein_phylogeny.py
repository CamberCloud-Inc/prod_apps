import subprocess
import sys
import argparse

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "biopython", "matplotlib"])

from biomni.tool.genetics import analyze_protein_phylogeny



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
    parser = argparse.ArgumentParser(description='Perform phylogenetic analysis on protein sequences')
    parser.add_argument('fasta_sequences', help='Path to FASTA file with protein sequences')
    parser.add_argument('-a', '--alignment-method', default='clustalw',
                        choices=['clustalw', 'muscle', 'pre-aligned'],
                        help='Method for sequence alignment (default: clustalw)')
    parser.add_argument('-t', '--tree-method', default='iqtree',
                        choices=['iqtree', 'fasttree'],
                        help='Method for tree construction (default: iqtree)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    print(f"Starting protein phylogeny analysis...")
    print(f"Input FASTA file: {args.fasta_sequences}")
    print(f"Alignment method: {args.alignment_method}")
    print(f"Tree method: {args.tree_method}")

    try:
        import os

        # Set up output directory
        os.makedirs(args.output_dir, exist_ok=True)

        result = analyze_protein_phylogeny(
            fasta_sequences=args.fasta_sequences,
            output_dir=args.output_dir,
            alignment_method=args.alignment_method,
            tree_method=args.tree_method
        )

        print("\n" + "="*80)
        print("ANALYSIS RESULTS")
        print("="*80)
        print(result)

        # Save log to file
        log_file = os.path.join(args.output_dir, "phylogeny_analysis_log.txt")
        with open(log_file, 'w') as f:
            f.write(result)

        print(f"\nAnalysis log saved to: {log_file}")

    except Exception as e:
        print(f"Error during protein phylogeny analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\nProtein phylogeny analysis completed!")


if __name__ == "__main__":
    main()
