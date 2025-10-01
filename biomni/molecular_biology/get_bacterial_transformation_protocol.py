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
    from biomni.tool.molecular_biology import get_bacterial_transformation_protocol
    parser = argparse.ArgumentParser(description='Get bacterial transformation protocol')
    parser.add_argument('--antibiotic', default='ampicillin',
                        help='Selection antibiotic (default: ampicillin)')
    parser.add_argument('--repetitive', action='store_true',
                        help='Sequence contains repetitive elements')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nGenerating bacterial transformation protocol...")
    print(f"Antibiotic: {args.antibiotic}")
    print(f"Repetitive sequence: {args.repetitive}")

    try:
        protocol = get_bacterial_transformation_protocol(
            antibiotic=args.antibiotic,
            is_repetitive=args.repetitive
        )

        # Generate output filename
        output_filename = "bacterial_transformation_protocol.json"
        output_path = os.path.join(args.output, output_filename)

        # Write protocol to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(protocol, f, indent=2, ensure_ascii=False)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
