import json
import sys
import os
import argparse
from biomni.tool.molecular_biology import design_golden_gate_oligos



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
    parser = argparse.ArgumentParser(description='Design oligos for Golden Gate assembly')
    parser.add_argument('backbone_sequence', help='Plasmid/backbone sequence')
    parser.add_argument('insert_sequence', help='Sequence to be inserted')
    parser.add_argument('enzyme', help='Type IIS enzyme (BsaI, BsmBI, BbsI, Esp3I, BtgZI, SapI)')
    parser.add_argument('--linear', action='store_true',
                        help='Backbone is linear (default: circular)')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nDesigning Golden Gate oligos...")
    print(f"Backbone length: {len(args.backbone_sequence)} bp")
    print(f"Insert length: {len(args.insert_sequence)} bp")
    print(f"Enzyme: {args.enzyme}")

    try:
        result = design_golden_gate_oligos(
            args.backbone_sequence,
            args.insert_sequence,
            args.enzyme,
            is_circular=not args.linear
        )

        # Generate output filename
        output_filename = "golden_gate_oligos.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write result to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to: {output_path}")
        if result.get('success'):
            print(f"Forward oligo: {result['oligos']['forward']}")
            print(f"Reverse oligo: {result['oligos']['reverse']}")
        else:
            print(f"Design failed: {result.get('message')}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nOligo design completed!")


if __name__ == "__main__":
    main()
