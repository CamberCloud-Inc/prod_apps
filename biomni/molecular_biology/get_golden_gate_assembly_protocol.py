import json
import sys
import os
import argparse



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['beautifulsoup4', 'biomni', 'biopython']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.molecular_biology import get_golden_gate_assembly_protocol
    parser = argparse.ArgumentParser(description='Get Golden Gate assembly protocol')
    parser.add_argument('--num-inserts', type=int, default=1,
                        help='Number of inserts (default: 1)')
    parser.add_argument('--enzyme', required=True,
                        help='Type IIS enzyme (BsaI, BsmBI, BbsI, Esp3I, BtgZI, SapI)')
    parser.add_argument('--vector-length', type=int,
                        help='Vector length in bp')
    parser.add_argument('--vector-amount', type=float, default=75.0,
                        help='Vector amount in ng (default: 75.0)')
    parser.add_argument('--insert-lengths', type=int, nargs='*',
                        help='Insert lengths in bp (space-separated)')
    parser.add_argument('--library-prep', action='store_true',
                        help='Protocol is for library preparation')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nGenerating Golden Gate assembly protocol...")
    print(f"Enzyme: {args.enzyme}")
    print(f"Number of inserts: {args.num_inserts}")
    if args.vector_length:
        print(f"Vector length: {args.vector_length} bp")

    try:
        protocol = get_golden_gate_assembly_protocol(
            num_inserts=args.num_inserts,
            enzyme_name=args.enzyme,
            vector_length=args.vector_length,
            vector_amount_ng=args.vector_amount,
            insert_lengths=args.insert_lengths,
            is_library_prep=args.library_prep
        )

        # Generate output filename
        output_filename = "golden_gate_protocol.json"
        output_path = os.path.join(args.output, output_filename)

        # Write protocol to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(protocol, f, indent=2, ensure_ascii=False, default=str)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
