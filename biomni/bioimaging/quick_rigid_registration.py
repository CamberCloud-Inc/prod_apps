#!/usr/bin/env python3
"""
Quick rigid registration of medical images.
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
        description='Quick rigid registration of medical images'
    )
    parser.add_argument('input_file', help='JSON config file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import quick_rigid_registration

    with open(args.input_file, 'r') as f:
        config = json.load(f)

    fixed_image_path = config['fixed_image_path']
    moving_image_path = config['moving_image_path']
    output_dir = config['output_dir']
    metric = config.get('metric', 'mutual_information')
    optimizer = config.get('optimizer', 'gradient_descent')
    preprocess = config.get('preprocess', True)
    create_visualizations = config.get('create_visualizations', True)
    learning_rate = config.get('learning_rate', 0.01)
    number_of_iterations = config.get('number_of_iterations', 100)
    gradient_convergence_tolerance = config.get('gradient_convergence_tolerance', 1e-6)

    result = quick_rigid_registration(
        fixed_image_path=fixed_image_path,
        moving_image_path=moving_image_path,
        output_dir=output_dir,
        metric=metric,
        optimizer=optimizer,
        preprocess=preprocess,
        create_visualizations=create_visualizations,
        learning_rate=learning_rate,
        number_of_iterations=number_of_iterations,
        gradient_convergence_tolerance=gradient_convergence_tolerance
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'rigid_registration_results.json')
    with open(output_file, 'w') as f:
        json.dump({
            "registered_image_path": result["registered_image_path"],
            "transform_path": result["transform_path"],
            "metrics_before": result["metrics_before"],
            "metrics_after": result["metrics_after"],
            "registration_type": result["registration_type"],
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
