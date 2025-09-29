# Athena++ Polytrope Star Simulation with Self-Gravity

This project simulates a polytropic star using Athena++ with self-gravity enabled. The simulation models a star as a polytrope with index n=1.5, including gravitational effects.

## Files

- `athinput.polytrope` - Athena++ input configuration file
- `polytrope_ic.py` - Python script to generate initial conditions by solving the Lane-Emden equation
- `polytrope_ic.h5` - Generated initial conditions file (HDF5 format)
- `polytrope_profile.png` - Plot showing the density and pressure profiles
- `Makefile` - Build and run commands
- `run_simulation.sh` - Script to run the simulation on Camber

## Physics

The simulation solves the Lane-Emden equation to generate realistic initial conditions for a polytropic star:

```
d²θ/dξ² + (2/ξ)(dθ/dξ) + θⁿ = 0
```

Where:
- θ is the dimensionless density
- ξ is the dimensionless radius
- n = 1.5 is the polytropic index

The density and pressure profiles are related by:
- ρ(r) = ρc * θⁿ(ξ)
- P(r) = K * ρ^(1+1/n)

## Running on Camber Platform

The simulation is configured to run on the Camber cloud platform using Athena++.

### Requirements
- Athena++ compiled with:
  - Spherical polar coordinates
  - Self-gravity (FFT solver)
  - Polytrope problem generator

### Simulation Parameters
- Grid: 128 radial zones
- Domain: 0 to 10 stellar radii
- Time: Run to t = 1.0 (code units)
- Polytropic index: n = 1.5
- Adiabatic index: γ = 5/3

The simulation will output:
- HDF5 data files every 0.01 time units
- History files every 0.001 time units