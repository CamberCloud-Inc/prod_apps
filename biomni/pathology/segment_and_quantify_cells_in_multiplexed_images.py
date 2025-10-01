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
    from biomni.tool.pathology import segment_and_quantify_cells_in_multiplexed_images
    parser = argparse.ArgumentParser(description='Segment cells and quantify protein expression levels from multichannel tissue images')
    parser.add_argument('image_path', help='Path to the multiplexed multichannel tissue image file')
    parser.add_argument('markers_list', help='JSON string or file path defining list of protein markers/antibodies used in each channel')
    parser.add_argument('--nuclear-channel-index', type=int, default=0,
                        help='Index of the nuclear staining channel for cell segmentation (default: 0)')
    parser.add_argument('--output-dir', default='./output',
                        help='Directory where analysis results will be saved (default: ./output)')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Parse markers_list - can be JSON string or file path
    try:
        if os.path.isfile(args.markers_list):
            with open(args.markers_list, 'r') as f:
                markers_list = json.load(f)
        else:
            markers_list = json.loads(args.markers_list)
    except json.JSONDecodeError as e:
        print(f"Error parsing markers_list: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading markers_list: {e}")
        sys.exit(1)

    print(f"\nSegmenting and quantifying cells in multiplexed images...")
    print(f"Image path: {args.image_path}")
    print(f"Markers list: {markers_list}")

    try:
        result = segment_and_quantify_cells_in_multiplexed_images(
            args.image_path,
            markers_list=markers_list,
            nuclear_channel_index=args.nuclear_channel_index,
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
