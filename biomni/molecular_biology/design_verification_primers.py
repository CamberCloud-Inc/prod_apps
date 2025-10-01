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
    from biomni.tool.molecular_biology import design_verification_primers
    parser = argparse.ArgumentParser(description='Design Sanger sequencing verification primers')
    parser.add_argument('plasmid_sequence', help='Complete plasmid sequence')
    parser.add_argument('start', type=int, help='Target region start position (0-based)')
    parser.add_argument('end', type=int, help='Target region end position')
    parser.add_argument('--linear', action='store_true',
                        help='Plasmid is linear (default: circular)')
    parser.add_argument('--coverage-length', type=int, default=800,
                        help='Typical read length per primer (default: 800)')
    parser.add_argument('--primer-length', type=int, default=20,
                        help='Length of designed primers (default: 20)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nDesigning verification primers...")
    print(f"Plasmid length: {len(args.plasmid_sequence)} bp")
    print(f"Target region: {args.start}-{args.end}")
    print(f"Coverage length: {args.coverage_length} bp")

    try:
        result = design_verification_primers(
            args.plasmid_sequence,
            (args.start, args.end),
            is_circular=not args.linear,
            coverage_length=args.coverage_length,
            primer_length=args.primer_length
        )

        # Generate output filename
        output_filename = "verification_primers.json"
        output_path = os.path.join(args.output, output_filename)

        # Write result to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False, default=str)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
