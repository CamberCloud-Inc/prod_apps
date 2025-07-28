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
1. Substitutes the left_force_duration parameter in the LAMMPS input file
2. Runs the LAMMPS simulation using MPI with 4 processes (with fixed velocity of 0.003)
3. Generates trajectory visualization with force arrows that disappear when external forces are removed

## Key Files

- `app.json` - Application configuration for the Camber Cloud platform, defines UI parameters and job configurations
- `run_sim.sh` - Main simulation runner script that orchestrates the LAMMPS run and visualization
- `unbreakable.lmp` - Main LAMMPS input script with simulation parameters and force field definitions
- `unbreakable.inc` - Force field coefficients (LJ, bond, angle, dihedral, improper parameters)
- `unbreakable.data` - Initial atomic coordinates and topology for a 700-atom carbon nanotube system
- `vis_stop.py` - Python visualization script that creates animated GIFs from trajectory data with temperature plots
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

The `vis_stop.py` script automatically receives parameters from `run_sim.sh`:
- `--left_force_duration` - Number of timesteps the force is applied (controls when arrows disappear)
- `--left_velocity` - Fixed velocity magnitude (0.003) for arrow scaling

The visualization combines:
- Molecular structure with bonds (pink lines, depth-based alpha)
- Force arrows (blue) that disappear when external forces are removed
- Temperature vs time plot showing thermal response (automatically scaled to simulation length)

## Environment Requirements

- LAMMPS executable accessible via `$LAMMPS_BIN`
- MPI (mpirun) for parallel execution
- Apptainer/Singularity container system
- Python dependencies: MDAnalysis, matplotlib, imageio, numpy, pandas

## File Dependencies

The simulation expects these environment variables:
- `$WORKDIR` - Working directory path
- `$SIF` - Singularity image file path
- `$LAMMPS_BIN` - LAMMPS executable path within container