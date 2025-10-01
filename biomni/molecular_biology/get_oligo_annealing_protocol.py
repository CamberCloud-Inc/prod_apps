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
    from biomni.tool.molecular_biology import get_oligo_annealing_protocol
    parser = argparse.ArgumentParser(description='Get standard oligo annealing protocol')
    parser.add_argument('-o', '--output-dir', default='./',
                        help='Output directory for results (default: ./)')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    print(f"\nRetrieving oligo annealing protocol...")

    try:
        protocol = get_oligo_annealing_protocol()

        # Generate output filename
        output_filename = "oligo_annealing_protocol.json"
        output_path = os.path.join(args.output_dir, output_filename)

        # Write protocol to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(protocol, f, indent=2, ensure_ascii=False)

        print(f"\nProtocol saved to: {output_path}")
        print(f"Protocol: {protocol['title']}")
        print(f"Steps: {len(protocol.get('steps', []))}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    print("\nProtocol retrieval completed successfully!")


if __name__ == "__main__":
    main()
