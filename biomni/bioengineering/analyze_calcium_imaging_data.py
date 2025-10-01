import subprocess
import sys
import os
import argparse
import json

# Install required packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy", "pandas", "scipy", "scikit-image"])




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
    from biomni.tool.bioengineering import analyze_calcium_imaging_data
    parser = argparse.ArgumentParser(description='Analyze calcium imaging data to quantify neuronal activity')
    parser.add_argument('input_file', help='JSON file containing input parameters')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()

    # Read input from file
    with open(args.input_file, 'r') as f:
        input_data = json.load(f)

    image_stack_path = os.path.expanduser(input_data['image_stack_path'])
    print(f"Analyzing calcium imaging data from: {image_stack_path}")

    if not os.path.exists(image_stack_path):
        print(f"Error: Image stack not found at: {image_stack_path}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Run the analysis
    try:
        result = analyze_calcium_imaging_data(
            image_stack_path=image_stack_path,
            output_dir=args.output
        )

        # Write result to file
        output_file = os.path.join(args.output, 'calcium_imaging_results.txt')
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
