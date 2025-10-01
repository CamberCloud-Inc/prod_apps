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
    from biomni.tool.cell_biology import quantify_and_cluster_cell_motility
    parser = argparse.ArgumentParser(description='Quantify and cluster cell motility')
    parser.add_argument('image_sequence_path', help='Path to directory containing time-lapse microscopy images or path to a multi-frame TIFF file')
    parser.add_argument('--output-dir', default='./results',
                        help='Directory path where results will be saved (default: ./results)')
    parser.add_argument('--num-clusters', type=int, default=3,
                        help='Number of distinct motility clusters to identify (default: 3)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    print(f"\nQuantifying and clustering cell motility...")
    print(f"Image sequence: {args.image_sequence_path}")
    print(f"Number of clusters: {args.num_clusters}")

    try:
        result = quantify_and_cluster_cell_motility(
            args.image_sequence_path,
            output_dir=args.output_dir,
            num_clusters=args.num_clusters
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
