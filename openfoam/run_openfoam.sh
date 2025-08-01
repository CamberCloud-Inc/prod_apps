#!/bin/bash

# OpenFOAM Cylinder Flow Simulation
# Usage: ./run_openfoam.sh <reynolds_number> <inlet_velocity> <cylinder_radius>

[ $# -ne 3 ] && { echo "Usage: $0 <reynolds_number> <inlet_velocity> <cylinder_radius>"; exit 1; }

REYNOLDS_NUMBER=$1
INLET_VELOCITY=$2
CYLINDER_RADIUS=$3

# ---- OpenFOAM + Spack -------------------------------------------------------
source /opt/spack/share/spack/setup-env.sh          # enable Spack
eval "$(spack load --sh openfoam@2312)"             # inject FOAM env vars
export PATH=$WM_PROJECT_DIR/wmake:$PATH

# ---- Setup simulation -------------------------------------------------------
cd "${0%/*}" || exit                                # Run from this directory
. ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions        # Tutorial run functions

canCompile || exit 0    # Dynamic code

# Create output directory
mkdir -p output
rm -rf output/*
rm -rf [0-9]* constant/polyMesh processor*

# Copy initial conditions
cp -r 0.orig 0

# Update parameters in blockMeshDict
sed -i "s/rInner.*0.5;/rInner  $CYLINDER_RADIUS;/" system/blockMeshDict
ROUTER=$(awk "BEGIN {print $CYLINDER_RADIUS * 2}")
sed -i "s/rOuter.*1;/rOuter  $ROUTER;/" system/blockMeshDict

# Update inlet velocity in boundary conditions
sed -i "s/uniformValue.*constant (1 0 0);/uniformValue    constant ($INLET_VELOCITY 0 0);/" 0/U

# Update simulation parameters based on Reynolds number
VISCOSITY=$(awk "BEGIN {printf \"%.8f\", $INLET_VELOCITY * $CYLINDER_RADIUS * 2 / $REYNOLDS_NUMBER}")
echo "
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      transportProperties;
}

transportModel  linear;

linear
{
    nu              [0 2 -1 0 0 0 0] $VISCOSITY;
}
" > constant/transportProperties

echo "Running OpenFOAM cylinder flow simulation..."
echo "Reynolds Number: $REYNOLDS_NUMBER"
echo "Inlet Velocity: $INLET_VELOCITY m/s"
echo "Cylinder Radius: $CYLINDER_RADIUS m"
echo "Calculated Viscosity: $VISCOSITY m²/s"

# Restore initial conditions
restore0Dir

# Generate mesh
echo "Generating mesh..."
runApplication blockMesh

# Run simulation
echo "Running potentialFoam solver..."
runApplication $(getApplication) -withFunctionObjects -writePhi -writephi -writep

# Post-processing
echo "Post-processing..."
runApplication postProcess -func "(streamFunction writeCellCentres)"

# Generate VTK files for analysis
echo "Converting to VTK format..."
runApplication foamToVTK -time 1

# Move results to output directory (ensure logs are captured)
mv log.* output/ 2>/dev/null || true
mv *.log output/ 2>/dev/null || true
mv VTK/ output/ 2>/dev/null || true
cp -r 0 output/ 2>/dev/null || true

echo "Simulation completed. Results in output/ directory."

# Update visualization notebook parameters
python3 -c "
import json
import os

notebook_path = 'analysis/visualization.ipynb'
if os.path.exists(notebook_path):
    with open(notebook_path, 'r') as f: 
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_text = ''.join(cell['source'])
            if 'REYNOLDS_NUMBER' in source_text:
                for i, line in enumerate(cell['source']):
                    if 'REYNOLDS_NUMBER' in line and '=' in line:
                        cell['source'][i] = f'REYNOLDS_NUMBER = $REYNOLDS_NUMBER\n'
                    elif 'INLET_VELOCITY' in line and '=' in line:
                        cell['source'][i] = f'INLET_VELOCITY = $INLET_VELOCITY\n'
                    elif 'CYLINDER_RADIUS' in line and '=' in line:
                        cell['source'][i] = f'CYLINDER_RADIUS = $CYLINDER_RADIUS\n'
                break
    
    with open(notebook_path, 'w') as f: 
        json.dump(nb, f, indent=1)
        
    print('Updated visualization notebook parameters')
else:
    print('Visualization notebook not found, skipping parameter update')
"