#!/bin/bash

# Molkart Spatial Multiomics Pipeline Runner
# This script executes the nf-core/molkart pipeline for Molecular Cartography data analysis

set -e  # Exit on error

echo "Starting nf-core/molkart pipeline..."
echo "Pipeline version: 1.0.0"
echo "Analysis type: Spatial transcriptomics - Molecular Cartography"

# Check if samplesheet is provided
if [ ! -f "samplesheet.csv" ]; then
    echo "ERROR: samplesheet.csv not found in current directory"
    echo "Please provide a samplesheet with format: sample,nuclear_image,spot_locations,membrane_image"
    exit 1
fi

# Display samplesheet for verification
echo ""
echo "Using samplesheet:"
cat samplesheet.csv
echo ""

# Set output directory
OUTDIR="${outdir:-/camber_outputs}"
echo "Output directory: $OUTDIR"

# Build the nextflow command with parameters
CMD="nextflow run nf-core/molkart -r 1.0.0"
CMD="$CMD --input samplesheet.csv"
CMD="$CMD --outdir $OUTDIR"

# Add segmentation method if specified
if [ ! -z "$segmentation_method" ]; then
    CMD="$CMD --segmentation_method $segmentation_method"
    echo "Segmentation method: $segmentation_method"
fi

# Add segmentation area filters if specified
if [ ! -z "$segmentation_min_area" ]; then
    CMD="$CMD --segmentation_min_area $segmentation_min_area"
fi

if [ ! -z "$segmentation_max_area" ]; then
    CMD="$CMD --segmentation_max_area $segmentation_max_area"
fi

# Add image preprocessing options
if [ "$skip_mindagap" = "true" ]; then
    CMD="$CMD --skip_mindagap"
fi

if [ ! -z "$mindagap_boxsize" ]; then
    CMD="$CMD --mindagap_boxsize $mindagap_boxsize"
fi

if [ ! -z "$clahe_cliplimit" ]; then
    CMD="$CMD --clahe_cliplimit $clahe_cliplimit"
fi

if [ ! -z "$clahe_kernel" ]; then
    CMD="$CMD --clahe_kernel $clahe_kernel"
fi

# Add training subset options
if [ "$create_training_subset" = "true" ]; then
    CMD="$CMD --create_training_subset"
    
    if [ ! -z "$crop_size_x" ]; then
        CMD="$CMD --crop_size_x $crop_size_x"
    fi
    
    if [ ! -z "$crop_size_y" ]; then
        CMD="$CMD --crop_size_y $crop_size_y"
    fi
    
    if [ ! -z "$crop_amount" ]; then
        CMD="$CMD --crop_amount $crop_amount"
    fi
fi

# Add Cellpose-specific parameters
if [ ! -z "$cellpose_diameter" ]; then
    CMD="$CMD --cellpose_diameter $cellpose_diameter"
fi

if [ ! -z "$cellpose_model" ]; then
    CMD="$CMD --cellpose_model $cellpose_model"
fi

if [ ! -z "$cellpose_flow_threshold" ]; then
    CMD="$CMD --cellpose_flow_threshold $cellpose_flow_threshold"
fi

if [ ! -z "$cellpose_cellprob_threshold" ]; then
    CMD="$CMD --cellpose_cellprob_threshold $cellpose_cellprob_threshold"
fi

# Add Mesmer-specific parameters
if [ ! -z "$mesmer_image_mpp" ]; then
    CMD="$CMD --mesmer_image_mpp $mesmer_image_mpp"
fi

# Add spot assignment parameters
if [ ! -z "$spot_distance_threshold" ]; then
    CMD="$CMD --spot_distance_threshold $spot_distance_threshold"
fi

# Add MultiQC parameters
if [ ! -z "$multiqc_title" ]; then
    CMD="$CMD --multiqc_title '$multiqc_title'"
fi

if [ ! -z "$email" ]; then
    CMD="$CMD --email $email"
fi

# Execute the pipeline
echo ""
echo "Executing command:"
echo "$CMD"
echo ""

eval $CMD

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "Pipeline completed successfully!"
    echo "Results are available in: $OUTDIR"
    echo ""
    echo "Output includes:"
    echo "  - Cell-by-transcript tables"
    echo "  - Segmentation masks"
    echo "  - Preprocessed images"
    echo "  - Quality control metrics"
    echo "  - MultiQC report"
else
    echo ""
    echo "Pipeline failed. Please check the logs for details."
    exit 1
fi
