#!/bin/bash

# GROMACS Molecular Dynamics Simulation Script
# Modified Tutorial – GPL v3.0
# This work is a derivative of the original https://github.com/gromacstutorials/gromacstutorials-inputs.git

# Parse command line parameters with defaults
TEMPERATURE=${1:-300}      # Temperature in Kelvin (default: 300K)
SALT_CONC=${2:-1.0}       # Salt concentration in M (default: 1.0 M)
SIMULATION_TIME=${3:-100}  # Simulation time in ps (default: 100 ps)
PRESSURE=${4:-1.0}        # Pressure in bar (default: 1.0 bar)
CUTOFF=${5:-1.0}          # Cutoff distance in nm (default: 1.0 nm)
INTEGRATOR=${6:-md}       # Integrator type (default: md)

echo "===== GROMACS Molecular Dynamics Simulation ====="
echo "Parameters:"
echo "  Temperature: ${TEMPERATURE} K"
echo "  Salt concentration: ${SALT_CONC} M"
echo "  Simulation time: ${SIMULATION_TIME} ps"
echo "  Pressure: ${PRESSURE} bar"
echo "  Cutoff distance: ${CUTOFF} nm"
echo "  Integrator: ${INTEGRATOR}"
echo "=============================================="

mkdir -p output

# Convert PDB to GRO
printf "0\n0\n" | gmx_mpi trjconv -f 1cta.pdb -s 1cta.pdb -o output/1cta.gro -center -box 5 5 5

# Generate topology and force field files
printf "1\n" | gmx_mpi pdb2gmx -f output/1cta.gro -water spce -ignh -o output/unsolvated.gro -v

# Solvate the protein
gmx_mpi solvate -cs spc216.gro -cp output/unsolvated.gro -o output/solvated.gro -p topol.top

# Create parameterized minimize.mdp
cat > output/minimize_param.mdp << EOF
integrator = steep
nsteps = 50
nstxout = 10
cutoff-scheme = Verlet
nstlist = 10
ns_type = grid
couple-intramol = yes
vdw-type = Cut-off
rvdw = ${CUTOFF}
coulombtype = pme
fourierspacing = 0.1
pme-order = 4
rcoulomb = ${CUTOFF}
EOF

# Prepare energy minimization
gmx_mpi grompp -f output/minimize_param.mdp -c output/solvated.gro -p topol.top -o output/min.tpr -pp output/min -po output/min -maxwarn 1

# Run energy minimization
gmx_mpi mdrun -v -deffnm output/min -nb gpu

# Extract potential energy
printf "10\n" | gmx_mpi energy -f output/min.edr -o output/potential-energy-minimization.xvg

# Add salt (neutralize and set specified concentration)
printf "14\n" | gmx_mpi genion -s output/min.tpr -p topol.top -o output/salted.gro -conc ${SALT_CONC} -neutral

# Second energy minimization after adding ions
gmx_mpi grompp -f output/minimize_param.mdp -c output/salted.gro -p topol.top -o output/min-s.tpr -pp output/min-s -po output/min-s
gmx_mpi mdrun -v -deffnm output/min-s -nb gpu

# Create parameterized NVT mdp
NVTSTEPS=$((${SIMULATION_TIME} * 1000))  # Convert ps to steps (1 fs timestep)
cat > output/nvt_param.mdp << EOF
integrator = ${INTEGRATOR}
nsteps = ${NVTSTEPS}
dt = 0.001
comm_mode = linear
comm_grps = system
gen-vel = yes
gen-temp = ${TEMPERATURE}
cutoff-scheme = Verlet
nstlist = 10
ns_type = grid
nstxout-compressed = 1000
vdw-type = Cut-off
rvdw = ${CUTOFF}
couple-intramol = yes
coulombtype = pme
fourierspacing = 0.1
pme-order = 4
rcoulomb = ${CUTOFF}
constraint-algorithm = lincs
constraints = hbonds
tcoupl = v-rescale
ld-seed = 48456
tc-grps = system
tau-t = 0.5
ref-t = ${TEMPERATURE}
EOF

# Prepare and run NVT simulation
gmx_mpi grompp -f output/nvt_param.mdp -c output/min-s.gro -p topol.top -o output/nvt.tpr -pp output/nvt -po output/nvt
gmx_mpi mdrun -v -deffnm output/nvt -nb gpu

# Create parameterized NPT mdp
NPTSTEPS=$((${SIMULATION_TIME} * 200))  # Shorter NPT run (0.2x NVT time)
cat > output/npt_param.mdp << EOF
integrator = ${INTEGRATOR}
nsteps = ${NPTSTEPS}
dt = 0.001
comm_mode = linear
comm_grps = system
gen-vel = yes
gen-temp = ${TEMPERATURE}
cutoff-scheme = Verlet
nstlist = 10
ns_type = grid
nstxout-compressed = 1000
vdw-type = Cut-off
rvdw = ${CUTOFF}
couple-intramol = yes
coulombtype = pme
fourierspacing = 0.1
pme-order = 4
rcoulomb = ${CUTOFF}
constraint-algorithm = lincs
constraints = hbonds
tcoupl = v-rescale
ld-seed = 48456
tc-grps = system
tau-t = 0.5
ref-t = ${TEMPERATURE}
pcoupl = c-rescale
Pcoupltype = isotropic
tau_p = 1.0
ref_p = ${PRESSURE}
compressibility = 4.5e-5
EOF

# Run NPT simulation
gmx_mpi grompp -f output/npt_param.mdp -c output/nvt.gro -p topol.top -o output/npt.tpr -pp output/npt -po output/npt
gmx_mpi mdrun -v -deffnm output/npt -nb gpu

# Post-processing and trajectory formatting
printf "0\n" | gmx_mpi trjconv -s output/npt.tpr -f output/npt.xtc -pbc mol -ur compact -o output/npt_nopbc.xtc

# Extract energies
printf "10\n" | gmx_mpi energy -f output/nvt.edr -o output/nvt_temperature.xvg
printf "15\n" | gmx_mpi energy -f output/npt.edr -o output/npt_pressure.xvg
printf "22\n" | gmx_mpi energy -f output/npt.edr -o output/npt_density.xvg

# Generate summary statistics
echo "===== Simulation Summary ====="
echo "Final files generated:"
echo "  - output/npt_nopbc.xtc (trajectory)"
echo "  - output/nvt_temperature.xvg (temperature profile)"
echo "  - output/npt_pressure.xvg (pressure profile)"
echo "  - output/npt_density.xvg (density profile)"
echo "=============================="

echo "GROMACS simulation completed successfully!"