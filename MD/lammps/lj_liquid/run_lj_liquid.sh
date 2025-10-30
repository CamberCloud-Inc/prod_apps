#!/bin/bash
#SBATCH --job-name=lj_liquid
#SBATCH --output=lj_liquid_%j.out
#SBATCH --error=lj_liquid_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=1
#SBATCH --time=01:00:00
#SBATCH --partition=cpu-queue
#SBATCH --mem=4G

# Set LAMMPS path
LAMMPS_BIN=/camber/home/tools/spack-deployments/v1.0.0/spack_20251017_183107/opt/spack/linux-sapphirerapids/lammps-20250722-pgb6fjz52t7acgoi3q24rjjqjtnojotx/bin/lmp

# Print job information
echo "Job started at: $(date)"
echo "Running on node: $(hostname)"
echo "Job ID: $SLURM_JOB_ID"
echo "Working directory: $(pwd)"
echo ""

# Run LAMMPS simulation
echo "Running LAMMPS simulation..."
srun $LAMMPS_BIN -in in.lj_liquid

# Print completion
echo ""
echo "Job completed at: $(date)"
