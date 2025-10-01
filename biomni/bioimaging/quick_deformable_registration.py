#!/usr/bin/env python3
"""
Quick deformable registration of medical images.
"""

import argparse
import sys
import json
import os



def install_dependencies():
    """Install required dependencies"""
    import subprocess
    import sys
    deps = ['biomni', 'nibabel']
    print("Installing dependencies...")
    for dep in deps:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', dep],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    parser = argparse.ArgumentParser(
        description='Quick deformable registration of medical images'
    )
    parser.add_argument('--fixed_image_path', required=True, help='Path to the reference/fixed image file')
    parser.add_argument('--moving_image_path', required=True, help='Path to the moving image file')
    parser.add_argument('--output_dir', required=True, help='Directory for output files')
    parser.add_argument('--metric', default='mutual_information', help='Similarity metric')
    parser.add_argument('--optimizer', default='gradient_descent', help='Optimization algorithm')
    parser.add_argument('--preprocess', type=lambda x: x.lower() == 'true', default=True, help='Enable preprocessing')
    parser.add_argument('--create_visualizations', type=lambda x: x.lower() == 'true', default=True, help='Create visualizations')
    parser.add_argument('--learning_rate', type=float, default=0.01, help='Learning rate')
    parser.add_argument('--number_of_iterations', type=int, default=100, help='Number of iterations')
    parser.add_argument('--gradient_convergence_tolerance', type=float, default=1e-6, help='Convergence tolerance')
    parser.add_argument('--number_of_control_points', type=int, default=4, help='Grid density for B-spline control points')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import quick_deformable_registration

    result = quick_deformable_registration(
        fixed_image_path=args.fixed_image_path,
        moving_image_path=args.moving_image_path,
        output_dir=args.output_dir,
        metric=args.metric,
        optimizer=args.optimizer,
        preprocess=args.preprocess,
        create_visualizations=args.create_visualizations,
        learning_rate=args.learning_rate,
        number_of_iterations=args.number_of_iterations,
        gradient_convergence_tolerance=args.gradient_convergence_tolerance,
        number_of_control_points=args.number_of_control_points
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'deformable_registration_results.json')
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
