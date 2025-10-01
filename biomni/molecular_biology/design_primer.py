import json
import sys
import os
import argparse



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'biopython', 'beautifulsoup4']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.molecular_biology import design_primer
    parser = argparse.ArgumentParser(description='Design a single primer')
    parser.add_argument('sequence', help='Target DNA sequence')
    parser.add_argument('start_pos', type=int, help='Starting position for primer search')
    parser.add_argument('--primer-length', type=int, default=20,
                        help='Primer length (default: 20)')
    parser.add_argument('--min-gc', type=float, default=0.4,
                        help='Minimum GC content (default: 0.4)')
    parser.add_argument('--max-gc', type=float, default=0.6,
                        help='Maximum GC content (default: 0.6)')
    parser.add_argument('--min-tm', type=float, default=55.0,
                        help='Minimum melting temperature (default: 55.0)')
    parser.add_argument('--max-tm', type=float, default=65.0,
                        help='Maximum melting temperature (default: 65.0)')
    parser.add_argument('--search-window', type=int, default=100,
                        help='Search window size (default: 100)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nDesigning primer...")
    print(f"Sequence length: {len(args.sequence)} bp")
    print(f"Start position: {args.start_pos}")
    print(f"Primer length: {args.primer_length}")

    try:
        primer = design_primer(
            args.sequence,
            args.start_pos,
            primer_length=args.primer_length,
            min_gc=args.min_gc,
            max_gc=args.max_gc,
            min_tm=args.min_tm,
            max_tm=args.max_tm,
            search_window=args.search_window
        )

        # Generate output filename
        output_filename = "designed_primer.json"
        output_path = os.path.join(args.output, output_filename)

        # Write result to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(primer, f, indent=2, ensure_ascii=False)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
