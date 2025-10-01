import json
import sys
import os
import argparse
from biomni.tool.molecular_biology import find_restriction_sites



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
    parser = argparse.ArgumentParser(description='Find restriction enzyme sites in DNA sequence')
    parser.add_argument('dna_sequence', help='DNA sequence to analyze')
    parser.add_argument('enzymes', nargs='+', help='One or more restriction enzyme names')
    parser.add_argument('--linear', action='store_true',
                        help='Sequence is linear (default: circular)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nFinding restriction sites...")
    print(f"Sequence length: {len(args.dna_sequence)} bp")
    print(f"Enzymes: {', '.join(args.enzymes)}")
    print(f"Topology: {'Linear' if args.linear else 'Circular'}")

    try:
        result = find_restriction_sites(args.dna_sequence, args.enzymes, is_circular=not args.linear)

        # Generate output filename
        output_filename = "restriction_sites.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")
        for enzyme, info in result.get('restriction_sites', {}).items():
            print(f"{enzyme}: {len(info.get('sites', []))} site(s)")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nRestriction site search completed successfully!")


if __name__ == "__main__":
    main()
