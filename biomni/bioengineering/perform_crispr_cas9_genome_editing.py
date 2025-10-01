import subprocess
import sys
import os
import argparse
import json

# No external packages needed for this tool



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
    from biomni.tool.bioengineering import perform_crispr_cas9_genome_editing
    parser = argparse.ArgumentParser(description='Simulate CRISPR-Cas9 genome editing process')
    parser.add_argument('input_file', help='JSON file containing input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    guide_rnas = input_data['guide_rna_sequences']
    target_genomic_loci = input_data['target_genomic_loci']
    cell_tissue_type = input_data['cell_tissue_type']

    print(f"Guide RNAs: {guide_rnas}")
    print(f"Target sequence length: {len(target_genomic_loci)} bp")
    print(f"Cell/Tissue type: {cell_tissue_type}")

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Run the simulation
    try:
        result = perform_crispr_cas9_genome_editing(
            guide_rna_sequences=guide_rnas,
            target_genomic_loci=target_genomic_loci,
            cell_tissue_type=cell_tissue_type
        )

        # Write result to file
        output_file = os.path.join(args.output, 'crispr_cas9_results.txt')
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")
    except Exception as e:
        print(f"Error during CRISPR-Cas9 simulation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
