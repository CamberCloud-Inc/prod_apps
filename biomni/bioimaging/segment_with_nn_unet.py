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
    parser.add_argument('input_file', help='JSON config file from stash')
    parser.add_argument('-o', '--output', required=True, help='Output directory')

    args = parser.parse_args()
    install_dependencies()

    # Import after dependencies are installed
    from biomni.tool.bioimaging import segment_with_nn_unet

    with open(args.input_file, 'r') as f:
        config = json.load(f)

    image_path = config['image_path']
    output_dir = config['output_dir']
    task_id = config['task_id']
    model_type = config.get('model_type', '3d_fullres')
    folds = config.get('folds', [0, 1, 2, 3, 4])
    use_tta = config.get('use_tta', False)
    num_threads = config.get('num_threads', 1)
    mixed_precision = config.get('mixed_precision', True)
    verbose = config.get('verbose', True)
    auto_prepare_input = config.get('auto_prepare_input', True)
    results_folder = config.get('results_folder')

    result = segment_with_nn_unet(
        image_path=image_path,
        output_dir=output_dir,
        task_id=task_id,
        model_type=model_type,
        folds=folds,
        use_tta=use_tta,
        num_threads=num_threads,
        mixed_precision=mixed_precision,
        verbose=verbose,
        auto_prepare_input=auto_prepare_input,
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
