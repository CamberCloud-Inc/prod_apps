#!/usr/bin/env python3
"""
Segment medical images using nnUNet.
"""

import sys
import json
from biomni.tool.bioimaging import segment_with_nn_unet



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
    if len(sys.argv) != 2:
        print("Error: Expected config file as argument", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
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

    print(json.dumps({
        "output_dir": result,
        "status": "success"
    }))


if __name__ == '__main__':
    main()
