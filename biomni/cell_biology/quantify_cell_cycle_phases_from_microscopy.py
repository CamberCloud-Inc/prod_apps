import json
import sys
import os
import argparse



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'skimage']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():

    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.cell_biology import quantify_cell_cycle_phases_from_microscopy
    parser = argparse.ArgumentParser(description='Quantify cell cycle phases from microscopy')
    parser.add_argument('image_paths', nargs='+', help='List of file paths to microscopy images for analysis')
    parser.add_argument('--output-dir', default='./results',
                        help='Directory path where results will be saved (default: ./results)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nQuantifying cell cycle phases from microscopy...")
    print(f"Number of images: {len(args.image_paths)}")

    try:
        result = quantify_cell_cycle_phases_from_microscopy(
            image_paths=args.image_paths,
            output_dir=args.output_dir
        )

        # Generate output filename
        output_filename = "result.json"
        output_path = os.path.join(args.output, output_filename)

        # Write result to JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({"research_log": result}, f, indent=2, ensure_ascii=False)

        print(f"Complete! Results: {output_path}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
