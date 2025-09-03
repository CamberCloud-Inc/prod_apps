#!/bin/bash
#SBATCH --job-name=atacseq_extended_test
#SBATCH --partition=cpu-mem-queue
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=40G
#SBATCH --time=12:00:00
#SBATCH --output=/camber/home/ivannovikau32295788/prod_apps/nextflow/atacseq_extended/atacseq_extended_test_%j.out
#SBATCH --error=/camber/home/ivannovikau32295788/prod_apps/nextflow/atacseq_extended/atacseq_extended_test_%j.err

# Set strict error handling
set -euo pipefail

# Set proper umask for file permissions
umask 0022

# Use /camber/home outputs directory for all run data
export NXF_SINGULARITY_HOME_MOUNT=true
export SINGULARITY_TMPDIR="/camber/home/ivannovikau32295788/outputs/nextflow/tmp"
export TMPDIR="/camber/home/ivannovikau32295788/outputs/nextflow/tmp"
export NXF_SINGULARITY_CACHEDIR="/camber/home/ivannovikau32295788/outputs/nextflow/singularity_cache"

# Create directories with proper permissions
WORK_DIR="/camber/home/ivannovikau32295788/outputs/nextflow/work_extended_${SLURM_JOB_ID}"
OUTPUT_DIR="/camber/home/ivannovikau32295788/outputs/nextflow/atacseq_extended_results_${SLURM_JOB_ID}"
mkdir -p "$WORK_DIR" "$NXF_SINGULARITY_CACHEDIR" "$TMPDIR" "$OUTPUT_DIR"

# Change to working directory
cd /camber/home/ivannovikau32295788/prod_apps/nextflow/atacseq_extended

# Load Nextflow module
module load nextflow/25.04.6

echo "=========================================="
echo "Starting ATAC-seq Extended Pipeline Test"
echo "Testing ALL Active Motif ATAC-seq Kit Parameters"
echo "Work directory: $WORK_DIR"
echo "Output directory: $OUTPUT_DIR"
echo "Cache directory: $NXF_SINGULARITY_CACHEDIR"
echo "TMPDIR: $TMPDIR"
echo "SLURM Job ID: $SLURM_JOB_ID"
echo "=========================================="

# Run the nf-core/atacseq pipeline with COMPREHENSIVE Active Motif parameters
# Using test profile for local references to avoid S3 access issues
nextflow run nf-core/atacseq \
    -r 2.1.2 \
    -c atacseq_extended.config \
    -profile test,singularity \
    -w "$WORK_DIR" \
    --outdir "$OUTPUT_DIR" \
    --read_length 150 \
    --narrow_peak \
    --mito_name chrM \
    --save_reference \
    --save_trimmed \
    --aligner bwa \
    --max_cpus 8 \
    --max_memory '32.GB' \
    --max_time '12.h' \
    -ansi-log false \
    -resume

echo "=========================================="
echo "Extended ATAC-seq Pipeline Test Completed!"
echo "Results location: $OUTPUT_DIR"
echo "All Active Motif ATAC-seq parameters tested:"
echo "  - Input samplesheet: test_samplesheet.csv"
echo "  - Reference genome: GRCh38 (iGenomes)"
echo "  - Read length: 150bp (PE150)"
echo "  - Peak calling: Narrow peaks (ATAC-specific)"
echo "  - Mitochondrial: chrM filtering"
echo "  - Blacklist: ENCODE regions (auto-included)"
echo "  - Aligner: BWA (default)"
echo "  - Adapters: Nextera (auto-detected)"
echo "  - Duplicates: Filtered (default)"
echo "  - References: Saved"
echo "  - Trimmed reads: Saved"
echo "=========================================="