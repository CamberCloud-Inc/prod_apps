#!/usr/bin/env python3
"""
Segment medical images using nnUNet.
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
        description='Segment medical images using nnUNet'
    )
    parser.add_argument('--image_path', required=True, help='Path to the input medical image file or directory')
    parser.add_argument('--output_dir', required=True, help='Directory for segmentation results')
    parser.add_argument('--task_id', required=True, help='nnUNet task identifier')
    parser.add_argument('--model_type', default='3d_fullres', help='Model architecture type')
    parser.add_argument('--folds', default='0,1,2,3,4', help='Cross-validation folds (comma-separated)')
    parser.add_argument('--use_tta', type=lambda x: x.lower() == 'true', default=False, help='Enable test-time augmentation')
    parser.add_argument('--num_threads', type=int, default=1, help='Number of CPU threads')
    parser.add_argument('--mixed_precision', type=lambda x: x.lower() == 'true', default=True, help='Use mixed precision')
    parser.add_argument('--verbose', type=lambda x: x.lower() == 'true', default=True, help='Enable detailed logging')
    parser.add_argument('--auto_prepare_input', type=lambda x: x.lower() == 'true', default=True, help='Auto-prepare input data')
    parser.add_argument('--results_folder', default='', help='Path to custom nnUNet results folder')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import segment_with_nn_unet

    # Parse folds from comma-separated string to list
    folds = [int(f.strip()) for f in args.folds.split(',') if f.strip()]
    results_folder = args.results_folder if args.results_folder else None

    result = segment_with_nn_unet(
        image_path=args.image_path,
        output_dir=args.output_dir,
        task_id=args.task_id,
        model_type=args.model_type,
        folds=folds,
        use_tta=args.use_tta,
        num_threads=args.num_threads,
        mixed_precision=args.mixed_precision,
        verbose=args.verbose,
        auto_prepare_input=args.auto_prepare_input,
        results_folder=results_folder
    )

    os.makedirs(args.output, exist_ok=True)
    output_file = os.path.join(args.output, 'nnunet_segmentation_results.json')
    with open(output_file, 'w') as f:
        json.dump({
            "output_dir": result,
            "status": "success"
        }, f, indent=2)
    print(f"Complete! Results: {output_file}")


if __name__ == '__main__':
    main()
