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
    from biomni.tool.molecular_biology import annotate_plasmid
    parser = argparse.ArgumentParser(description='Annotate a DNA sequence using pLannotate')
    parser.add_argument('sequence', help='DNA sequence to annotate')
    parser.add_argument('--linear', action='store_true',
                        help='Sequence is linear (default: circular)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nAnnotating plasmid sequence...")
    print(f"Sequence length: {len(args.sequence)} bp")
    print(f"Topology: {'Linear' if args.linear else 'Circular'}")

    try:
        result = annotate_plasmid(args.sequence, is_circular=not args.linear)

        if result is None:
            print("Error: Annotation failed")
            sys.exit(1)

        # Generate output filename
        output_filename = "plasmid_annotations.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        print(f"\nResults saved to: {output_path}")
        print(f"Total annotations found: {len(result.get('annotations', []))}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nPlasmid annotation completed successfully!")


if __name__ == "__main__":
    main()
