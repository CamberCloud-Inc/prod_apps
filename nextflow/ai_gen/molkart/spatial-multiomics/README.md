# Molkart Spatial Multiomics Pipeline

## Overview

The **nf-core/molkart** pipeline is a comprehensive bioinformatics workflow for processing Molecular Cartography spatial transcriptomics data from Resolve Bioscience. This pipeline performs end-to-end analysis of combinatorial FISH (Fluorescence In Situ Hybridization) data, including image preprocessing, cell segmentation, spot-to-cell assignment, and quality control.

## Pipeline Features

### 1. Image Preprocessing
- **Grid Pattern Filling**: Uses Mindagap to fill gaps between imaging tiles
- **Contrast Enhancement**: Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) for improved image quality
- **Multichannel Stacking**: Combines nuclear (DAPI) and membrane (WGA) staining images

### 2. Cell Segmentation Methods
Multiple state-of-the-art segmentation algorithms are supported:
- **Mesmer** (default): Optimized for nuclear and membrane stains
- **Cellpose**: Versatile deep learning segmentation with pre-trained models
- **ilastik**: Pixel classification-based segmentation
- **Stardist**: Specialized for star-convex nuclei detection

### 3. Spot Processing
- Identifies and removes duplicated FISH spots near grid lines
- Assigns spots to segmented cells based on spatial proximity
- Filters spots based on configurable distance thresholds

### 4. Quality Control
- Generates comprehensive QC metrics:
  - Spot assignment rates
  - Average spots per cell
  - Segmentation mask size distributions
  - Cell count statistics
- Produces MultiQC reports for pipeline-wide quality assessment

## Input Requirements

### Samplesheet Format
The pipeline requires a CSV samplesheet with the following columns:

```csv
sample,nuclear_image,spot_locations,membrane_image
sample1,sample1_DAPI.tiff,sample1_spots.txt,sample1_WGA.tiff
sample2,sample2_DAPI.tiff,sample2_spots.txt,
```

**Columns:**
- `sample`: Unique sample identifier
- `nuclear_image`: Path to DAPI nuclear staining image (TIFF format)
- `spot_locations`: Path to table of FISH spot positions (x,y,z,gene coordinates)
- `membrane_image`: Optional path to membrane staining image (e.g., WGA)

### Input File Formats
- **Images**: TIFF format (single or multi-channel)
- **Spot Locations**: Tab-delimited text file with columns for x, y, z coordinates and gene identifiers
- **Resolution**: Compatible with standard Molecular Cartography output formats

## Output Files

The pipeline generates:

1. **Cell-by-Transcript Tables**: Matched spot assignments to segmented cells
2. **Segmentation Masks**: Cell boundary definitions in standard formats
3. **Preprocessed Images**: Gap-filled and contrast-enhanced images
4. **QC Metrics**: Detailed statistics on segmentation and spot assignment quality
5. **MultiQC Report**: Comprehensive HTML quality control report
6. **Intermediate Files**: Preprocessing and segmentation intermediaries for troubleshooting

## Key Parameters

### Segmentation Parameters
- `segmentation_method`: Choose between mesmer, cellpose, ilastik, stardist (default: mesmer)
- `segmentation_min_area`: Minimum cell area in pixels to filter artifacts (default: 100)
- `segmentation_max_area`: Maximum cell area in pixels to remove clumps (default: 10000)

### Image Preprocessing
- `skip_mindagap`: Skip grid pattern filling if not needed (default: false)
- `mindagap_boxsize`: Size of box for gap filling algorithm (default: 3)
- `clahe_cliplimit`: Contrast limit for CLAHE enhancement (default: 0.01)
- `clahe_kernel`: Kernel size for CLAHE processing (default: 8)

### Cellpose-Specific
- `cellpose_diameter`: Expected cell diameter in pixels (0 = auto-estimate)
- `cellpose_model`: Pre-trained model: nuclei, cyto, or cyto2 (default: nuclei)
- `cellpose_flow_threshold`: Flow threshold for segmentation (default: 0.4)
- `cellpose_cellprob_threshold`: Cell probability threshold (default: 0.0)

### Mesmer-Specific
- `mesmer_image_mpp`: Microns per pixel resolution (default: 0.5)

### Spot Assignment
- `spot_distance_threshold`: Maximum distance in pixels for spot-to-cell assignment (default: 5)

### Training Subset Creation
- `create_training_subset`: Generate image crops for training custom models (default: false)
- `crop_size_x`: Width of training image crops (default: 400)
- `crop_size_y`: Height of training image crops (default: 400)
- `crop_amount`: Number of crops to extract per image (default: 4)

## Usage

### Basic Command
```bash
nextflow run nf-core/molkart \
  -profile docker \
  --input samplesheet.csv \
  --outdir results \
  -r 1.0.0
```

### With Custom Segmentation
```bash
nextflow run nf-core/molkart \
  -profile docker \
  --input samplesheet.csv \
  --outdir results \
  --segmentation_method cellpose \
  --cellpose_model cyto2 \
  --segmentation_min_area 150 \
  -r 1.0.0
```

### Optimized for Large Datasets
```bash
nextflow run nf-core/molkart \
  -profile docker \
  --input samplesheet.csv \
  --outdir results \
  --segmentation_method mesmer \
  --skip_mindagap \
  --create_training_subset false \
  -r 1.0.0
```

## System Requirements

### Resource Recommendations
- **Small datasets** (< 5 samples): SMALL system (2 nodes, 8-16 GB RAM each)
- **Medium datasets** (5-20 samples): MEDIUM system (4 nodes, 16-32 GB RAM each)
- **Large datasets** (> 20 samples): LARGE system (8 nodes, 32-64 GB RAM each)

### Software Requirements
- Nextflow >= 21.04.0
- Docker or Singularity (for containerization)
- nf-core/molkart version 1.0.0

## Pipeline Workflow

```
Input Data (TIFF images + spot tables)
    ↓
Image Preprocessing (Mindagap + CLAHE)
    ↓
Cell Segmentation (Mesmer/Cellpose/ilastik/Stardist)
    ↓
Spot Processing & Assignment
    ↓
Quality Control & Reporting
    ↓
Output: Cell-by-transcript tables + QC reports
```

## Applications

This pipeline is ideal for:
- **Spatial transcriptomics analysis** of Molecular Cartography data
- **Single-cell spatial profiling** in tissue sections
- **Cell type identification** using spatial gene expression patterns
- **Tumor microenvironment studies** with spatial context
- **Developmental biology** research with spatial resolution
- **MERSCOPE targeted spatial transcriptomics** data processing

## Supported Technologies
- Resolve Bioscience Molecular Cartography
- Combinatorial FISH (fluorescence in situ hybridization)
- MERSCOPE targeted spatial transcriptomics
- Compatible with other FISH-based spatial transcriptomics platforms

## References

- **Pipeline**: nf-core/molkart (https://nf-co.re/molkart)
- **Developed by**: @kbestak and @FloWuenne
- **Documentation**: https://nf-co.re/molkart/1.0.0/docs/usage
- **GitHub**: https://github.com/nf-core/molkart

## Version Information
- **Pipeline Version**: 1.0.0
- **nf-core Version**: Compatible with nf-core framework
- **Last Updated**: 2025

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/nf-core/molkart/issues
- nf-core Slack: https://nfcore.slack.com/
- Documentation: https://nf-co.re/molkart

---

*This pipeline is part of the nf-core collection of bioinformatics pipelines and follows nf-core best practices for reproducibility and scalability.*
