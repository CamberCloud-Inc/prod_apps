import json
import sys
import os
import argparse



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'biopython', 'beautifulsoup4']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.molecular_biology import get_gene_coding_sequence
    parser = argparse.ArgumentParser(description='Retrieve gene coding sequences from NCBI')
    parser.add_argument('gene_name', help='Name of the gene')
    parser.add_argument('organism', help='Name of the organism (e.g., "Homo sapiens", "Mus musculus")')
    parser.add_argument('--email', help='Email address for NCBI Entrez (recommended)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nRetrieving coding sequence for gene: {args.gene_name}")
    print(f"Organism: {args.organism}")

    try:
        result = get_gene_coding_sequence(args.gene_name, args.organism, email=args.email)

        # Generate output filename
        output_filename = f"{args.gene_name}_{args.organism.replace(' ', '_')}_cds.json"
        output_path = os.path.join(args.output, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
