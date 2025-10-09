#!/bin/bash
#
# Bacterial Genome Assembly from Oxford Nanopore Data
# Uses nf-core/bacass pipeline with Flye assembler for bacterial isolates
#
# Usage: bash run_assembly.sh
#

set -euo pipefail

# Check required files
if [ ! -f "samplesheet.csv" ]; then
    echo "ERROR: samplesheet.csv not found"
    echo "Please create a samplesheet with columns: ID,R1,R2,LongFastQ,Fast5,GenomeSize"
    exit 1
fi

# Assembly configuration (hardcoded for bacterial genomes)
ASSEMBLER="dragonflye"        # Uses Flye for ONT data
ASSEMBLY_TYPE="long"          # Long-read only assembly
FLYE_MODE="--nano-hq"         # For Q20+ ONT reads (modern basecalling)

# Quality thresholds (hardcoded for high-quality assemblies)
MIN_CONTIG_LENGTH="1000"      # Minimum contig length to report
GENOME_SIZE="5000000"         # Default bacterial genome size (5 Mb)

# Output directory
OUTDIR="${OUTDIR:-/camber_outputs}"

echo "========================================="
echo "Bacterial Genome Assembly Pipeline"
echo "========================================="
echo "Input samplesheet: samplesheet.csv"
echo "Output directory: $OUTDIR"
echo "Assembler: $ASSEMBLER (Flye)"
echo "Assembly type: Long-read only (ONT)"
echo "Flye mode: nano-hq (Q20+)"
echo "========================================="

# Run nf-core/bacass pipeline
nextflow run nf-core/bacass \
    -r 2.3.1 \
    --input samplesheet.csv \
    --outdir "$OUTDIR" \
    --assembler "$ASSEMBLER" \
    --assembly_type "$ASSEMBLY_TYPE" \
    --skip_kraken2 \
    --skip_polish \
    -profile docker \
    -resume

echo "========================================="
echo "Pipeline completed successfully!"
echo "Results available in: $OUTDIR"
echo "========================================="
echo ""
echo "Key outputs:"
echo "  - Assembled genomes: $OUTDIR/Assembly/"
echo "  - Quality reports: $OUTDIR/QC/"
echo "  - Annotations: $OUTDIR/Annotation/"
echo "  - MultiQC report: $OUTDIR/multiqc/multiqc_report.html"
echo "========================================="