import json
import sys
import os
import argparse
from biomni.tool.molecular_biology import design_knockout_sgrna



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
    parser = argparse.ArgumentParser(description='Design sgRNAs for CRISPR knockout')
    parser.add_argument('gene_name', help='Target gene symbol (e.g., EGFR, TP53)')
    parser.add_argument('data_lake_path', help='Path to sgRNA library data')
    parser.add_argument('--species', default='human',
                        help='Target species (default: human)')
    parser.add_argument('--num-guides', type=int, default=1,
                        help='Number of guides to return (default: 1)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

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
        output_path = os.path.join(args.output_dir, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")
        print(f"Guide sequences: {len(result.get('guides', []))}")
        for i, guide in enumerate(result.get('guides', []), 1):
            print(f"  Guide {i}: {guide}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nsgRNA design completed successfully!")


if __name__ == "__main__":
    main()
