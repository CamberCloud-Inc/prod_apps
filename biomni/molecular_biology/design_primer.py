import json
import sys
import os
import argparse
from biomni.tool.molecular_biology import design_primer



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
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

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
        output_path = os.path.join(args.output_dir, output_filename)

        # Write result to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(primer, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")
        if primer:
            print(f"Primer sequence: {primer['sequence']}")
            print(f"Position: {primer['position']}")
            print(f"GC content: {primer['gc']:.2%}")
            print(f"Tm: {primer['tm']:.1f}°C")
        else:
            print("No suitable primer found")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nPrimer design completed!")


if __name__ == "__main__":
    main()
