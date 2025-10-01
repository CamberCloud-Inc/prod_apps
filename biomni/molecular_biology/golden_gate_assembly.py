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
    from biomni.tool.molecular_biology import golden_gate_assembly
    parser = argparse.ArgumentParser(description='Simulate Golden Gate assembly')
    parser.add_argument('backbone_sequence', help='Complete backbone sequence')
    parser.add_argument('enzyme', help='Type IIS enzyme (BsaI, BsmBI, BbsI, Esp3I, BtgZI, SapI)')
    parser.add_argument('fragments_file', help='JSON file with fragment definitions')
    parser.add_argument('--linear', action='store_true',
                        help='Backbone is linear (default: circular)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nSimulating Golden Gate assembly...")
    print(f"Backbone length: {len(args.backbone_sequence)} bp")
    print(f"Enzyme: {args.enzyme}")

    # Read fragments from JSON file
    try:
        with open(args.fragments_file, 'r') as f:
            fragments = json.load(f)
        if not isinstance(fragments, list):
            fragments = [fragments]
    except Exception as e:
        print(f"Error reading fragments file: {e}")
        sys.exit(1)

    print(f"Fragments to assemble: {len(fragments)}")

    try:
        result = golden_gate_assembly(
            args.backbone_sequence,
            args.enzyme,
            fragments,
            is_circular=not args.linear
        )

        # Generate output filename
        output_filename = "golden_gate_assembly.json"
        output_path = os.path.join(args.output, output_filename)

        # Write result to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
