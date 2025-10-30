# Lennard-Jones Liquid Simulation

A comprehensive LAMMPS application for simulating Lennard-Jones liquids with configurable thermodynamic ensembles and detailed property calculations.

## Overview

This application simulates a simple atomic liquid using the classical Lennard-Jones (LJ) potential. It's designed for studying fundamental liquid-state behavior, phase transitions, and thermodynamic properties.

## Features

- **Multiple Ensembles**: NVE (microcanonical), NVT (canonical), NPT (isothermal-isobaric)
- **Temperature Control**: Optional real-time temperature monitoring and thermostat control
- **Comprehensive Output**: Energy, pressure, temperature time series and trajectory data
- **Flexible Parameters**: Customize system size, density, temperature, cutoff, timestep
- **Analysis Tools**: Jupyter notebook for post-processing and visualization

## Quick Start

### Running on Camber Cloud

1. Navigate to the Apps section on Camber Cloud
2. Find "Lennard-Jones Liquid Simulation"
3. Configure parameters:
   - Number of atoms (e.g., 2000)
   - Reduced density ρ* (e.g., 0.8 for liquid)
   - Reduced temperature T* (e.g., 1.0 for liquid)
   - Ensemble type (NVT recommended for beginners)
   - Enable temperature calculation
4. Launch the simulation
5. Wait for completion and download results

### Local Testing

```bash
cd /path/to/lj-liquid
bash run_sim.sh 2000 0.8 1.0 nvt true 2.5 0.002 20000 100000 500
```

Parameters in order:
1. Number of atoms
2. Reduced density (ρ*)
3. Reduced temperature (T*)
4. Ensemble (nve/nvt/npt)
5. Calculate temperature (true/false)
6. Cutoff radius (σ units)
7. Timestep (τ units)
8. Equilibration steps
9. Production steps
10. Output frequency

## Scientific Background

### Lennard-Jones Potential

The LJ potential models interactions between neutral atoms:

```
V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]
```

Where:
- **ε** = depth of potential well (energy scale)
- **σ** = distance where potential is zero (length scale)
- **r** = interatomic distance

### Reduced Units

All quantities are in LJ reduced units:
- Length: σ
- Energy: ε
- Time: τ = σ√(m/ε)
- Temperature: T* = kᵦT/ε
- Density: ρ* = ρσ³
- Pressure: P* = Pσ³/ε

### Phase Diagram Reference

Key thermodynamic states:
- **Triple point**: T* ≈ 0.68, ρ* ≈ 0.85
- **Critical point**: T* ≈ 1.32, ρ* ≈ 0.32
- **Liquid region**: 0.7 < T* < 1.3, 0.7 < ρ* < 0.95
- **Gas region**: T* > 1.5, ρ* < 0.3

## Output Files

After simulation completion, find these files in `output/`:

1. **trajectory.lammpstrj** - Atomic positions and velocities over time
2. **energy.csv** - Potential, kinetic, and total energy time series
3. **pressure.csv** - Pressure evolution
4. **temperature.csv** - Temperature evolution (if enabled)
5. **lammps.log** - Full LAMMPS output with all thermodynamic data
6. **final_config.data** - Final atomic configuration (for restarts)
7. **final_restart.restart** - LAMMPS restart file

## Analysis and Visualization

Open `analysis/visualization.ipynb` in Jupyter to:
- Plot thermodynamic properties (T, P, E) vs time
- Calculate statistical averages and fluctuations
- Assess equilibration quality
- Generate publication-ready figures

The notebook automatically:
- Installs required packages (matplotlib, numpy, pandas)
- Loads all output files
- Creates comprehensive plots
- Computes statistics

## Parameter Guidelines

### System Size
- **Small tests**: 500-2000 atoms
- **Good statistics**: 2000-5000 atoms
- **Publication quality**: 5000-20000 atoms

### Density (ρ*)
- **Gas**: < 0.3
- **Liquid**: 0.7-0.9
- **Solid**: > 1.0

### Temperature (T*)
- **Solid**: < 0.7
- **Liquid**: 0.7-1.5
- **Gas**: > 1.5

### Cutoff Radius
- **Minimum**: 2.5σ (standard)
- **Recommended**: 2.5-3.0σ
- **Long-range**: > 3.5σ (with long-range corrections)

### Timestep
- **Safe**: 0.001-0.002τ
- **Standard**: 0.002-0.005τ
- **Fast**: 0.005τ (check energy conservation!)

### Simulation Length
- **Equilibration**: 20,000-50,000 steps (10-20% of production)
- **Production**: 100,000-500,000 steps
- **Long runs**: 1,000,000+ steps for slow dynamics

## Expected Results

### Typical Output for Default Parameters
(2000 atoms, ρ*=0.8, T*=1.0, NVT ensemble)

- **Mean temperature**: ~1.00 ± 0.03
- **Mean pressure**: ~2-4 (depends on state)
- **Potential energy per atom**: ~-5.5
- **Kinetic energy per atom**: ~1.5
- **Simulation time**: 2-5 minutes

### Quality Checks

1. **Temperature stability**: Fluctuations < 5% of mean
2. **Energy conservation (NVE)**: Drift < 0.1% over simulation
3. **Pressure equilibration**: Reaches stable mean after ~20% of run
4. **No atom overlaps**: Check trajectory visually

## Applications

This simulation is useful for:

1. **Education**
   - Learning MD fundamentals
   - Understanding statistical mechanics
   - Visualizing molecular motion

2. **Research**
   - Phase diagram mapping
   - Transport property calculations
   - Testing new simulation methods
   - Benchmarking algorithms

3. **Method Development**
   - Testing thermostats/barostats
   - Validating integration schemes
   - Developing analysis tools

## Troubleshooting

### Simulation Crashes
- Reduce timestep (try 0.001)
- Lower initial temperature
- Check density is reasonable
- Ensure cutoff > 2.5σ

### High Energy Drift (NVE)
- Decrease timestep
- Ensure proper equilibration
- Check for atom overlaps

### Poor Statistics
- Run longer production phase
- Increase system size
- Use better equilibration

### Temperature Oscillations (NVT)
- Adjust thermostat damping parameter
- Increase system size
- Check equilibration length

## References

1. Allen & Tildesley, "Computer Simulation of Liquids" (2017)
2. Frenkel & Smit, "Understanding Molecular Simulation" (2002)
3. LAMMPS documentation: https://docs.lammps.org

## Project Structure

```
lj-liquid/
├── app.json                 # Camber Cloud app configuration
├── README.md                # This file
├── run_sim.sh               # Main simulation runner
├── scripts/
│   └── lj_liquid.lmp        # LAMMPS input script
├── output/                  # Generated simulation output
│   ├── trajectory.lammpstrj
│   ├── energy.csv
│   ├── pressure.csv
│   ├── temperature.csv
│   └── lammps.log
└── analysis/
    ├── visualization.ipynb  # Analysis notebook
    └── thermodynamics.png   # Generated plots
```

## Technical Details

- **LAMMPS version**: Any recent version (tested with 29Oct20+)
- **Parallelization**: MPI-based (automatically uses available cores)
- **Memory requirements**: ~100 MB for 10,000 atoms
- **Typical runtime**: 2-10 minutes (depends on system size and steps)

## Support

For issues or questions:
- Check LAMMPS documentation
- Review parameter guidelines above
- Examine log files for error messages
- Verify input parameters are physically reasonable
