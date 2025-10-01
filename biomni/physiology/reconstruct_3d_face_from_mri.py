#!/usr/bin/env python3
"""
Reconstruct 3D Face from MRI

Generate a 3D model of facial anatomy from MRI scans of the head and neck.
"""

import sys
import json



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
    from biomni.tool.physiology import reconstruct_3d_face_from_mri
    if len(sys.argv) != 2:
        print("Usage: reconstruct_3d_face_from_mri.py <input_json>")
        sys.exit(1)

    with open(sys.argv[1], 'r') as f:
        inputs = json.load(f)

    mri_file_path = inputs['mri_file_path']
    output_dir = inputs.get('output_dir', './output')
    subject_id = inputs.get('subject_id', 'subject')
    threshold_value = inputs.get('threshold_value', 300)

    result = reconstruct_3d_face_from_mri(
        mri_file_path=mri_file_path,
        output_dir=output_dir,
        subject_id=subject_id,
        threshold_value=threshold_value
    )

    print(json.dumps({"result": result}))


if __name__ == "__main__":
    main()
