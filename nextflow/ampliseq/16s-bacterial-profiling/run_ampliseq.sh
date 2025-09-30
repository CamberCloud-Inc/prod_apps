#!/bin/bash

# 16S Bacterial Community Profiling with nf-core/ampliseq
# Configured for SILVA database and bacterial diversity analysis

# ============================================================================
# Configuration Parameters
# ============================================================================

# Input files
INPUT_SAMPLESHEET="${input}"
OUTDIR="${outdir:-/camber_outputs}"
METADATA="${metadata}"

# Primer sequences (V3-V4 region by default)
FW_PRIMER="${fw_primer:-CCTACGGGNGGCWGCAG}"
RV_PRIMER="${rv_primer:-GACTACHVGGGTATCTAATCC}"

# DADA2 truncation lengths (0 = automatic)
TRUNCLENF="${trunclenf:-0}"
TRUNCLENR="${trunclenr:-0}"

# Taxonomic database - SILVA v138 (hardcoded for bacterial profiling)
DADA_REF_TAXONOMY="silva=138"

# Pipeline version
REVISION="${revision:-2.11.0}"

# Skip options for optimization
SKIP_KRONA="${skip_krona:-true}"
SKIP_CUTADAPT="${skip_cutadapt:-false}"

# ============================================================================
# Build Nextflow Command
# ============================================================================

echo "=========================================="
echo "16S Bacterial Community Profiling"
echo "=========================================="
echo "Input samplesheet: $INPUT_SAMPLESHEET"
echo "Output directory: $OUTDIR"
echo "Forward primer: $FW_PRIMER"
echo "Reverse primer: $RV_PRIMER"
echo "Taxonomy database: $DADA_REF_TAXONOMY"
echo "Pipeline version: $REVISION"
echo "=========================================="

# Base command
CMD="nextflow run nf-core/ampliseq \
    -r $REVISION \
    --input $INPUT_SAMPLESHEET \
    --outdir $OUTDIR \
    --FW_primer $FW_PRIMER \
    --RV_primer $RV_PRIMER \
    --dada_ref_taxonomy $DADA_REF_TAXONOMY"

# Add metadata if provided
if [ ! -z "$METADATA" ]; then
    echo "Metadata file: $METADATA"
    CMD="$CMD --metadata $METADATA"
fi

# Add truncation lengths if not 0
if [ "$TRUNCLENF" != "0" ]; then
    CMD="$CMD --trunclenf $TRUNCLENF"
    echo "Truncate forward: $TRUNCLENF bp"
fi

if [ "$TRUNCLENR" != "0" ]; then
    CMD="$CMD --trunclenr $TRUNCLENR"
    echo "Truncate reverse: $TRUNCLENR bp"
fi

# Add skip options
if [ "$SKIP_KRONA" = "true" ]; then
    CMD="$CMD --skip_krona"
    echo "Skipping Krona plots"
fi

if [ "$SKIP_CUTADAPT" = "true" ]; then
    CMD="$CMD --skip_cutadapt"
    echo "Skipping Cutadapt (reads pre-trimmed)"
fi

# SILVA-specific optimizations for bacterial profiling
CMD="$CMD \
    --ignore_empty_input_files \
    --ignore_failed_trimming \
    --max_cpus 8"

echo "=========================================="
echo "Executing pipeline..."
echo "=========================================="

# Execute the command
eval $CMD

# Check exit status
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "=========================================="
    echo "Pipeline completed successfully!"
    echo "=========================================="
    echo ""
    echo "Output files:"
    echo "  - ASV table: $OUTDIR/dada2/ASV_table.tsv"
    echo "  - Taxonomy: $OUTDIR/dada2/ASV_tax.tsv"
    echo "  - Alpha diversity: $OUTDIR/qiime2/diversity/alpha_rarefaction/"
    echo "  - Beta diversity: $OUTDIR/qiime2/diversity/core-metrics-results/"
    echo "  - MultiQC report: $OUTDIR/multiqc/multiqc_report.html"
    echo ""
else
    echo "=========================================="
    echo "Pipeline failed with exit code: $EXIT_CODE"
    echo "=========================================="
    exit $EXIT_CODE
fi