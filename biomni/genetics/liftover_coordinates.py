#!/usr/bin/env python3
"""Biomni Tool: Liftover Coordinates
Wraps: biomni.tool.genetics.liftover_coordinates
"""
import subprocess
import sys
import argparse
import os

# Install required dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "pyliftover"])




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
    from biomni.tool.genetics import liftover_coordinates
    parser = argparse.ArgumentParser(description='Perform liftover of genomic coordinates between hg19 and hg38 formats')
    parser.add_argument('chromosome', help='Chromosome number (e.g., "1", "X")')
    parser.add_argument('position', type=int, help='Genomic position')
    parser.add_argument('input_format', help='Input genome build (hg19 or hg38)')
    parser.add_argument('output_format', help='Output genome build (hg19 or hg38)')
    parser.add_argument('data_path', help='Path to liftover chain files')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    print(f"Starting liftover coordinates analysis...")
    print(f"Chromosome: {args.chromosome}")
    print(f"Position: {args.position}")
    print(f"Converting from {args.input_format} to {args.output_format}")

    try:
        result = liftover_coordinates(
            chromosome=args.chromosome,
            position=args.position,
            input_format=args.input_format,
            output_format=args.output_format,
            data_path=args.data_path
        )

        # Save results to file
        os.makedirs(args.output, exist_ok=True)
        output_file = os.path.join(args.output, f"liftover_{args.chromosome}_{args.position}_results.txt")
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")

    except Exception as e:
        print(f"Error during liftover analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
