import json
import sys
import os
import argparse
from biomni.tool.molecular_biology import get_plasmid_sequence



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
    parser = argparse.ArgumentParser(description='Retrieve plasmid sequences from Addgene or NCBI')
    parser.add_argument('identifier', help='Plasmid ID (Addgene) or name (NCBI)')
    parser.add_argument('--addgene', action='store_true',
                        help='Force Addgene lookup')
    parser.add_argument('--ncbi', action='store_true',
                        help='Force NCBI lookup')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nRetrieving plasmid sequence for: {args.identifier}")

    # Determine source
    is_addgene = None
    if args.addgene:
        is_addgene = True
    elif args.ncbi:
        is_addgene = False

    try:
        result = get_plasmid_sequence(args.identifier, is_addgene=is_addgene)

        if result is None:
            print("Error: Plasmid not found")
            sys.exit(1)

        # Generate output filename
        output_filename = f"plasmid_{args.identifier.replace(' ', '_')}.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")
        print(f"Source: {result.get('source', 'Unknown')}")
        print(f"Sequence length: {len(result.get('sequence', ''))} bp")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nPlasmid sequence retrieval completed successfully!")


if __name__ == "__main__":
    main()
