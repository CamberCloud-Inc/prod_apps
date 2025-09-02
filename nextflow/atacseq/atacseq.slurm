#!/bin/bash
#SBATCH --job-name=atacseq_test
#SBATCH --partition=cpu-mem-queue
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=40G
#SBATCH --time=12:00:00
#SBATCH --output=/home/ec2-user/prod_apps/nextflow/atacseq/atacseq_test_%j.out
#SBATCH --error=/home/ec2-user/prod_apps/nextflow/atacseq/atacseq_test_%j.err

# Set strict error handling
set -euo pipefail

# Set proper umask for file permissions
umask 0022

# Use /home/ec2-user/data/nextflow with permission fixes (as specified)
export NXF_SINGULARITY_HOME_MOUNT=true
export SINGULARITY_TMPDIR="/home/ec2-user/data/nextflow/tmp"
export TMPDIR="/home/ec2-user/data/nextflow/tmp"
export NXF_SINGULARITY_CACHEDIR="/home/ec2-user/data/nextflow/singularity_cache"

# Create directories with proper permissions
WORK_DIR="/home/ec2-user/data/nextflow/work_${SLURM_JOB_ID}"
mkdir -p "$WORK_DIR" "$NXF_SINGULARITY_CACHEDIR" "$TMPDIR"

# Change to working directory
cd /home/ec2-user/prod_apps/nextflow/atacseq

# Load Nextflow module
module load nextflow/25.04.6

echo "=========================================="
echo "Starting ATAC-seq pipeline (TEST)"
echo "Work directory: $WORK_DIR"
echo "Cache directory: $NXF_SINGULARITY_CACHEDIR"
echo "TMPDIR: $TMPDIR"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "=========================================="

# Run the nf-core/atacseq pipeline with test profile
nextflow run nf-core/atacseq \
    -r 2.1.2 \
    --outdir results \
    -w "$WORK_DIR" \
    -c atacseq.config \
    -profile test,singularity \
    -ansi-log false \
    --max_cpus 8 \
    --max_memory '32.GB' \
    -resume

echo "=========================================="
echo "Pipeline execution completed successfully!"
echo "Results location: $(pwd)/results"
echo "=========================================="