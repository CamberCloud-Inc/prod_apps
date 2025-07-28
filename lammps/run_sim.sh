#!/bin/bash
[ $# -ne 1 ] && { echo "Usage: $0 <left_force_duration>"; exit 1; }

LEFT_FORCE_DURATION=$1
mkdir -p output
rm -f output/*.{lammpstrj,csv,log}

cd scripts && lmp -in unbreakable.lmp -var LEFT_FORCE_DURATION $LEFT_FORCE_DURATION && cd .. || exit 1

python3 -c "
import json
with open('analysis/visualization.ipynb', 'r') as f: nb = json.load(f)
for cell in nb['cells']:
    if cell['cell_type'] == 'code' and 'LEFT_FORCE_DURATION' in ''.join(cell['source']):
        for i, line in enumerate(cell['source']):
            if 'LEFT_FORCE_DURATION' in line and '=' in line:
                cell['source'][i] = f'LEFT_FORCE_DURATION = $LEFT_FORCE_DURATION\n'
                cell['source'].insert(i+1, 'LEFT_VELOCITY = 0.0005\n')
                break
        break
with open('analysis/visualization.ipynb', 'w') as f: json.dump(nb, f, indent=1)
"