import json
import sys
import os
import argparse



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'biopython']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.molecular_biology import find_restriction_sites
    parser = argparse.ArgumentParser(description='Find restriction enzyme sites in DNA sequence')
    parser.add_argument('dna_sequence', help='DNA sequence to analyze')
    parser.add_argument('enzymes', nargs='+', help='One or more restriction enzyme names')
    parser.add_argument('--linear', action='store_true',
                        help='Sequence is linear (default: circular)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nFinding restriction sites...")
    print(f"Sequence length: {len(args.dna_sequence)} bp")
    print(f"Enzymes: {', '.join(args.enzymes)}")
    print(f"Topology: {'Linear' if args.linear else 'Circular'}")

    try:
        result = find_restriction_sites(args.dna_sequence, args.enzymes, is_circular=not args.linear)

        # Generate output filename
        output_filename = "restriction_sites.json"
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
