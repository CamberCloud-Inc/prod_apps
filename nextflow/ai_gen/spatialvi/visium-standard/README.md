# Spatial Transcriptomics: 10x Visium Tissue Architecture Analysis

## Overview

This app processes 10x Genomics Visium spatial transcriptomics data to map gene expression patterns across tissue sections while preserving spatial coordinates. It identifies spatial domains, discovers spatially variable genes, and performs differential expression analysis.

## Use Case

**Biological Question**: How are different cell types and functional zones organized spatially within a tissue section?

**Applications**:
- Tumor microenvironment mapping
- Brain region characterization
- Tissue architecture analysis
- Developmental biology studies
- Disease pathology investigation

## Input Requirements

### Option A: Pre-processed Space Ranger Data (Recommended)

Create a CSV samplesheet:
```csv
sample,spaceranger_dir
section1,stash://username/data/section1/outs
section2,stash://username/data/section2/outs
```

### Option B: Raw FASTQ Files

Create a CSV samplesheet:
```csv
sample,fastq_dir,image,slide,area
section1,stash://username/fastqs/,hires_image.png,V11J26-123,A1
```

## Parameters

- **input**: Path to CSV samplesheet
- **outdir**: Output directory for results
- **genome**: Reference genome (GRCh38 for human, GRCm39 for mouse)

## Expected Outputs

1. **Spatial Analysis**:
   - Spatial cluster maps
   - Spatially variable genes (Moran's I)
   - Spatial coordinates for all spots

2. **Gene Expression**:
   - Expression matrices with coordinates
   - H5AD files (Scanpy/Seurat compatible)
   - Zarr format data

3. **Quality Control**:
   - Spot QC metrics
   - Tissue detection results
   - MultiQC report

4. **Differential Expression**:
   - Between-cluster comparisons
   - Marker genes per spatial domain

## Resource Requirements

| Dataset Size | Node Size | Expected Runtime |
|--------------|-----------|------------------|
| Test data (1 section) | XSMALL | 30-60 min |
| 1-2 sections | SMALL | 1-2 hours |
| 4-8 sections | MEDIUM | 2-4 hours |
| Large/Visium HD | LARGE | 4-8 hours |

## Test Data

This app uses nf-core test-datasets for validation:
- Sample: Human brain cancer tissue (FFPE, Visium v2)
- Data: Pre-processed Space Ranger outputs
- Source: 10x Genomics public datasets (sub-sampled)

## Pipeline Details

- **Pipeline**: nf-core/spatialvi (dev version)
- **Workflow**:
  1. Quality control and filtering
  2. Normalization (scanpy)
  3. Leiden clustering
  4. Spatial variable gene detection (Moran's I)
  5. Differential expression testing
  6. Output generation (H5AD, Zarr)

## Notes

- For raw FASTQ processing, Space Ranger will run first (adds 4-8 hours)
- Visium HD data requires LARGE node size due to higher spot density
- Output files are compatible with TissUUmaps for interactive visualization
- Pipeline is currently in development (dev branch)

## Links

- [nf-core/spatialvi documentation](https://nf-co.re/spatialvi)
- [10x Genomics Visium](https://www.10xgenomics.com/products/spatial-gene-expression)
- [TissUUmaps visualization](https://tissuumaps.github.io/)