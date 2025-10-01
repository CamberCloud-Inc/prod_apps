import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "scikit-image"])




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
    from biomni.tool.bioengineering import analyze_myofiber_morphology
    parser = argparse.ArgumentParser(description='Quantify morphological properties of myofibers in microscopy images')
    parser.add_argument('input_file', help='JSON file containing input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    image_path = os.path.expanduser(input_data['image_path'])
    nuclei_channel = input_data.get('nuclei_channel', 2)
    myofiber_channel = input_data.get('myofiber_channel', 1)
    threshold_method = input_data.get('threshold_method', 'otsu')

    print(f"Analyzing myofiber morphology from: {image_path}")

    if not os.path.exists(image_path):
        print(f"Error: Image file not found at: {image_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_myofiber_morphology(
            image_path=image_path,
            nuclei_channel=nuclei_channel,
            myofiber_channel=myofiber_channel,
            threshold_method=threshold_method,
            output_dir=args.output
        )

        # Write result to file
        output_file = os.path.join(args.output, 'myofiber_morphology_results.txt')
        with open(output_file, 'w') as f:
            f.write(result)
        print(f"Complete! Results: {output_file}")
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
