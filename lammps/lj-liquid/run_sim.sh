#!/bin/bash

# Lennard-Jones Liquid Simulation Runner
# Usage: bash run_sim.sh <numAtoms> <density> <temperature> <ensemble> <calculateTemp> <cutoff> <timestep> <equilSteps> <prodSteps> <outputFreq>

# Parse command line arguments
NUM_ATOMS=${1:-2000}
DENSITY=${2:-0.8}
TEMPERATURE=${3:-1.0}
ENSEMBLE=${4:-nvt}
CALC_TEMP=${5:-true}
CUTOFF=${6:-2.5}
TIMESTEP=${7:-0.002}
EQUIL_STEPS=${8:-20000}
PROD_STEPS=${9:-100000}
OUTPUT_FREQ=${10:-500}

# Create output directory
mkdir -p output
cd output
rm -f *.csv *.lammpstrj *.log *.data *.restart

echo "=========================================="
echo "Lennard-Jones Liquid Simulation"
echo "=========================================="
echo "Parameters:"
echo "  Number of atoms: $NUM_ATOMS"
echo "  Reduced density: $DENSITY"
echo "  Reduced temperature: $TEMPERATURE"
echo "  Ensemble: $ENSEMBLE"
echo "  Calculate temperature: $CALC_TEMP"
echo "  Cutoff radius: $CUTOFF"
echo "  Timestep: $TIMESTEP"
echo "  Equilibration steps: $EQUIL_STEPS"
echo "  Production steps: $PROD_STEPS"
echo "  Output frequency: $OUTPUT_FREQ"
echo "=========================================="

# Run LAMMPS simulation
echo "Starting LAMMPS simulation..."
mpirun -np ${OMPI_COMM_WORLD_SIZE:-1} lmp -var numAtoms $NUM_ATOMS \
    -var density $DENSITY \
    -var temperature $TEMPERATURE \
    -var ensemble $ENSEMBLE \
    -var calcTemp $CALC_TEMP \
    -var cutoff $CUTOFF \
    -var timestep $TIMESTEP \
    -var equilSteps $EQUIL_STEPS \
    -var prodSteps $PROD_STEPS \
    -var outputFreq $OUTPUT_FREQ \
    -in ../scripts/lj_liquid.lmp \
    -log lammps.log

echo "=========================================="
echo "Simulation completed!"
echo "=========================================="
echo "Output files:"
ls -lh *.csv *.lammpstrj *.log *.data 2>/dev/null || echo "No output files found"
echo "=========================================="
