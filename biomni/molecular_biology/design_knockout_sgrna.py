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
    from biomni.tool.molecular_biology import design_knockout_sgrna
    parser = argparse.ArgumentParser(description='Design sgRNAs for CRISPR knockout')
    parser.add_argument('gene_name', help='Target gene symbol (e.g., EGFR, TP53)')
    parser.add_argument('data_lake_path', help='Path to sgRNA library data')
    parser.add_argument('--species', default='human',
                        help='Target species (default: human)')
    parser.add_argument('--num-guides', type=int, default=1,
                        help='Number of guides to return (default: 1)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nDesigning sgRNAs for gene knockout...")
    print(f"Gene: {args.gene_name}")
    print(f"Species: {args.species}")
    print(f"Number of guides: {args.num_guides}")

    try:
        result = design_knockout_sgrna(
            args.gene_name,
            args.data_lake_path,
            species=args.species,
            num_guides=args.num_guides
        )

        # Generate output filename
        output_filename = f"{args.gene_name}_sgrnas.json"
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
