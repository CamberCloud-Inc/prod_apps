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
    from biomni.tool.molecular_biology import pcr_simple
    parser = argparse.ArgumentParser(description='Simulate PCR amplification with given primers')
    parser.add_argument('sequence', help='DNA sequence or plasmid')
    parser.add_argument('forward_primer', help='Forward primer sequence (5\' to 3\')')
    parser.add_argument('reverse_primer', help='Reverse primer sequence (5\' to 3\')')
    parser.add_argument('--circular', action='store_true',
                        help='Sequence is circular (default: linear)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nSimulating PCR amplification...")
    print(f"Template length: {len(args.sequence)} bp")
    print(f"Forward primer: {args.forward_primer}")
    print(f"Reverse primer: {args.reverse_primer}")
    print(f"Topology: {'Circular' if args.circular else 'Linear'}")

    try:
        result = pcr_simple(
            args.sequence,
            args.forward_primer,
            args.reverse_primer,
            circular=args.circular
        )

        # Generate output filename
        output_filename = "pcr_results.json"
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
