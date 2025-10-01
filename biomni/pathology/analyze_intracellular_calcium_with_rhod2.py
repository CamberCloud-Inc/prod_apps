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
    from biomni.tool.pathology import analyze_intracellular_calcium_with_rhod2
    parser = argparse.ArgumentParser(description='Analyze intracellular calcium concentration using Rhod-2 fluorescent indicator')
    parser.add_argument('background_image_path', help='Path to the background fluorescence image (no cells/dye)')
    parser.add_argument('control_image_path', help='Path to the control sample image (baseline calcium levels)')
    parser.add_argument('sample_image_path', help='Path to the experimental sample fluorescence image')
    parser.add_argument('--output-dir', default='./output',
                        help='Directory where analysis results will be saved (default: ./output)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nAnalyzing intracellular calcium with Rhod-2...")
    print(f"Background image: {args.background_image_path}")
    print(f"Control image: {args.control_image_path}")
    print(f"Sample image: {args.sample_image_path}")

    try:
        result = analyze_intracellular_calcium_with_rhod2(
            args.background_image_path,
            control_image_path=args.control_image_path,
            sample_image_path=args.sample_image_path,
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
