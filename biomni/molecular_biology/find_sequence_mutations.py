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
    from biomni.tool.molecular_biology import find_sequence_mutations
    parser = argparse.ArgumentParser(description='Find mutations by comparing query and reference sequences')
    parser.add_argument('query_sequence', help='Query sequence to analyze')
    parser.add_argument('reference_sequence', help='Reference sequence to compare against')
    parser.add_argument('--query-start', type=int, default=1,
                        help='Start position of query sequence (default: 1)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nComparing sequences for mutations...")
    print(f"Query length: {len(args.query_sequence)}")
    print(f"Reference length: {len(args.reference_sequence)}")

    try:
        result = find_sequence_mutations(
            args.query_sequence,
            args.reference_sequence,
            query_start=args.query_start
        )

        # Generate output filename
        output_filename = "mutations.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write results to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")
        if result.get('success'):
            print(f"Mutations found: {len(result.get('mutations', []))}")
            for mut in result.get('mutations', []):
                print(f"  {mut}")
        else:
            print("Comparison failed")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nMutation analysis completed successfully!")


if __name__ == "__main__":
    main()
