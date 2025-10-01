#!/usr/bin/env python3
"""
Batch registration of multiple images to a single reference.
"""

import argparse
import sys
import json
import os



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
    parser = argparse.ArgumentParser(
        description='Batch registration of multiple images to a single reference'
    )
    parser.add_argument('input_file', help='JSON config file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import batch_register_images

    with open(args.input_file, 'r') as f:
        config = json.load(f)

    fixed_image_path = config['fixed_image_path']
    moving_images_dir = config['moving_images_dir']
    output_dir = config['output_dir']
    transform_type = config.get('transform_type', 'rigid')
    metric = config.get('metric', 'mutual_information')
    optimizer = config.get('optimizer', 'gradient_descent')
    preprocess = config.get('preprocess', True)
    create_visualizations = config.get('create_visualizations', True)
    learning_rate = config.get('learning_rate', 0.01)
    number_of_iterations = config.get('number_of_iterations', 100)
    gradient_convergence_tolerance = config.get('gradient_convergence_tolerance', 1e-6)

    result = batch_register_images(
        fixed_image_path=fixed_image_path,
        moving_images_dir=moving_images_dir,
        output_dir=output_dir,
        transform_type=transform_type,
        metric=metric,
        optimizer=optimizer,
        preprocess=preprocess,
        create_visualizations=create_visualizations,
        learning_rate=learning_rate,
        number_of_iterations=number_of_iterations,
        gradient_convergence_tolerance=gradient_convergence_tolerance
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'batch_registration_results.json')
    with open(output_file, 'w') as f:
        json.dump({
            "results": result,
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
