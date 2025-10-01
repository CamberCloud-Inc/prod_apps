import subprocess
import sys
import argparse
import json

# No external packages needed for this tool
from biomni.tool.bioengineering import perform_crispr_cas9_genome_editing



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
    parser = argparse.ArgumentParser(description='Simulate CRISPR-Cas9 genome editing process')
    parser.add_argument('guide_rna_sequences', help='JSON string or comma-separated list of guide RNA sequences (20 nucleotides each)')
    parser.add_argument('target_genomic_loci', help='Target genomic sequence to be edited')
    parser.add_argument('cell_tissue_type', help='Type of cell or tissue being edited (e.g., HEK293, HeLa, iPSC)')

    args = parser.parse_args()

    # Parse guide RNA sequences (either JSON or comma-separated)
    try:
        guide_rnas = json.loads(args.guide_rna_sequences)
    except json.JSONDecodeError:
        # Assume comma-separated list
        guide_rnas = [g.strip() for g in args.guide_rna_sequences.split(',')]

    print(f"Guide RNAs: {guide_rnas}")
    print(f"Target sequence length: {len(args.target_genomic_loci)} bp")
    print(f"Cell/Tissue type: {args.cell_tissue_type}")
    print("\n" + "="*80)

    # Run the simulation
    try:
        result = perform_crispr_cas9_genome_editing(
            guide_rna_sequences=guide_rnas,
            target_genomic_loci=args.target_genomic_loci,
            cell_tissue_type=args.cell_tissue_type
        )
        print(result)
    except Exception as e:
        print(f"Error during CRISPR-Cas9 simulation: {e}")
        sys.exit(1)

    print("\n" + "="*80)
    print("CRISPR-Cas9 genome editing simulation completed successfully!")


if __name__ == "__main__":
    main()
