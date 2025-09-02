#!/bin/bash
#SBATCH --job-name=crisprseq_success
#SBATCH --partition=cpu-mem-queue
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=40G
#SBATCH --time=12:00:00
#SBATCH --output=/home/ec2-user/prod_apps/nextflow/scrnaseq/crisprseq_success_%j.out
#SBATCH --error=/home/ec2-user/prod_apps/nextflow/scrnaseq/crisprseq_success_%j.err

# Set strict error handling
set -euo pipefail

# Set proper umask for file permissions
umask 0022

# FINAL FIX: Use /home/ec2-user/data/nextflow with permission fixes
export NXF_SINGULARITY_HOME_MOUNT=true
export SINGULARITY_TMPDIR="/home/ec2-user/data/nextflow/tmp"
export TMPDIR="/home/ec2-user/data/nextflow/tmp"
export NXF_SINGULARITY_CACHEDIR="/home/ec2-user/data/nextflow/singularity_cache"

# Create directories with proper permissions
WORK_DIR="/home/ec2-user/data/nextflow/work_${SLURM_JOB_ID}"
mkdir -p "$WORK_DIR" "$NXF_SINGULARITY_CACHEDIR" "$TMPDIR"

# Change to working directory
cd /home/ec2-user/prod_apps/nextflow/scrnaseq

# Load Nextflow module
module load nextflow/25.04.6

echo "=========================================="
echo "Starting CRISPR-seq pipeline (SUCCESS)"
echo "Work directory: $WORK_DIR"
echo "Cache directory: $NXF_SINGULARITY_CACHEDIR"
echo "TMPDIR: $TMPDIR"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "=========================================="

# Run the pipeline with custom config that fixes permissions
nextflow run nf-core/crisprseq \
    -r 2.3.0 \
    --input https://raw.githubusercontent.com/nf-core/test-datasets/crisprseq/testdata-edition/samplesheet_test.csv \
    --analysis targeted \
    --outdir results \
    -w "$WORK_DIR" \
    -c success.config \
    -profile test,singularity \
    -ansi-log false \
    --max_cpus 8 \
    --max_memory '32.GB' \
    -resume

echo "=========================================="
echo "Pipeline execution completed successfully!"
echo "Results location: $(pwd)/results"
echo "=========================================="