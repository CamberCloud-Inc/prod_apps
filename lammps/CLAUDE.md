# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator) molecular dynamics simulation project focused on carbon nanotube mechanics. The simulation models the breaking behavior of carbon nanotubes under applied velocity forces.

## Running the Simulation

The main command to run the simulation is:
```bash
sh ./run_sim.sh <left_force_duration>
```

Example:
```bash
sh ./run_sim.sh 20000
```

The script:
1. Runs the LAMMPS simulation using MPI with 4 processes, passing left_force_duration as a variable
2. Generates trajectory and temperature data files
3. For visualization, use the separate `visualization.ipynb` Jupyter notebook

## Key Files

- `app.json` - Application configuration for the Camber Cloud platform, defines UI parameters and job configurations
- `run_sim.sh` - Main simulation runner script that runs LAMMPS only
- `unbreakable.lmp` - Main LAMMPS input script with simulation parameters and force field definitions
- `unbreakable.inc` - Force field coefficients (LJ, bond, angle, dihedral, improper parameters)
- `unbreakable.data` - Initial atomic coordinates and topology for a 700-atom carbon nanotube system
- `visualization.ipynb` - Jupyter notebook for Python-based visualization and analysis
- `requirements.txt` - Python package dependencies for visualization
- `trajectory_with_arrows.gif` - Output visualization showing nanotube deformation with force arrows

## Simulation Architecture

The simulation uses a three-region approach:
- `cnt_top` - Top region atoms with applied leftward velocity (0.003)
- `cnt_bot` - Bottom region atoms with applied rightward velocity (-0.003)
- `cnt_mid` - Middle region atoms under NVT thermostat at 300K

The force application follows this sequence:
1. Initial equilibration (100 timesteps)
2. Apply opposing velocities to top/bottom regions (LEFT_FORCE_DURATION timesteps)
3. Gradual force release and equilibration (300 timesteps total)
4. Final dynamics run (3,000 timesteps)

## Visualization

The `visualization.ipynb` Jupyter notebook handles all Python-based analysis:
- Automatically installs required dependencies
- Configurable parameters (LEFT_FORCE_DURATION, LEFT_VELOCITY)
- Interactive visualization development environment

The visualization combines:
- Molecular structure with bonds (pink lines, depth-based alpha)
- Force arrows (blue) - left arrow disappears when external forces are removed, right arrow stays throughout
- Temperature vs time plot showing thermal response (automatically scaled to simulation length)

## Workflow

1. Run LAMMPS simulation: `./run_sim.sh 20000`
2. Open `visualization.ipynb` in Jupyter
3. Modify parameters if needed in the notebook
4. Run all cells to generate `trajectory_with_arrows.gif`

## Environment Requirements

### For LAMMPS Simulation:
- LAMMPS executable (`lmp`) accessible in PATH
- MPI (mpirun) for parallel execution

### For Visualization (Jupyter notebook):
- Python 3.7+ with pip
- Jupyter notebook environment
- Dependencies (auto-installed): MDAnalysis, matplotlib, imageio, numpy, pandas

## Usage Notes

- The shell script now focuses purely on LAMMPS execution
- All Python dependencies and visualization are handled in the Jupyter notebook
- The notebook automatically detects simulation parameters and file paths
- No environment variables required - the notebook handles dependency installation