#!/bin/bash
# Usage: ./run_sim.sh <left_force_duration>
if [ $# -ne 1 ]; then
    echo "Usage: $0 <left_force_duration>"
    echo "Example: $0 20000"
    echo ""
    echo "After running this script, use visualization.ipynb for Python-based analysis"
    exit 1
fi

LEFT_FORCE_DURATION=${1:-20000}  # Use default value if not provided

echo "Starting LAMMPS simulation with LEFT_FORCE_DURATION=$LEFT_FORCE_DURATION"

# Clean up previous simulation files
rm -f output/trajectory.lammpstrj output/temperature.csv output/thermo_full.log output/log.lammps

# Change to scripts directory and run LAMMPS simulation
cd scripts
mpirun -np 4 lmp -in unbreakable.lmp -var LEFT_FORCE_DURATION $LEFT_FORCE_DURATION
cd ..

# Check if simulation completed successfully
if [ $? -eq 0 ]; then
    echo "LAMMPS simulation completed successfully!"
    echo ""
    echo "Generated files in ./output/:"
    ls -la output/trajectory.lammpstrj output/temperature.csv output/thermo_full.log 2>/dev/null || echo "Some output files may be missing"
    echo ""
    echo "Next steps:"
    echo "1. Open analysis/visualization.ipynb in Jupyter"
    echo "2. Update LEFT_FORCE_DURATION parameter in the notebook if needed"
    echo "3. Run all cells to generate cnt_trajectory.gif in analysis/ folder"
else
    echo "LAMMPS simulation failed!"
    echo "Check the log files for errors"
    exit 1
fi