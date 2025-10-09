# nf-core/spatialvi Use Cases

## Overview

Spatial transcriptomics with 10x Genomics Visium technology combines gene expression measurement with spatial coordinates, revealing tissue architecture and cellular organization in their native context.

---

## Use Case 1: 10x Visium Tissue Architecture Analysis (HIGHEST PRIORITY)

**Priority**: P0

**Biological Question**: How are different cell types and functional zones organized spatially within a tissue section?

**Target Audience**:
- Developmental biologists studying tissue organization
- Pathologists investigating tissue structure
- Cancer researchers analyzing solid tumors
- Immunologists studying lymphoid organ architecture

**Typical Experimental Design**:
- Sample type: Fresh frozen or FFPE tissue sections on Visium slides
- Data type: 10x Genomics Visium spatial gene expression
- Technology: Visium v1, v2, or HD
- Scale: 1-12 tissue sections per slide (typically 2-4 sections per experiment)
- Organism: Human or mouse

**Scientific Use Cases**:
- Identify spatially distinct tissue regions (cortex vs medulla, tumor vs stroma)
- Map cell type distributions across tissue sections
- Discover spatial gene expression gradients
- Characterize tissue microenvironments

**Key Parameters**:
- **Hardcoded**:
  - Analysis workflow: Full QC, normalization, clustering, spatial analysis
  - Clustering method: Leiden algorithm
  - Spatial statistics: Moran's I for spatially variable genes
  - QC thresholds: Standard filtering (total counts, gene counts, tissue presence)

- **Exposed**:
  - Input samplesheet (with Space Ranger outputs or raw FASTQs)
  - Reference genome (human GRCh38 or mouse GRCm38)
  - Output directory
  - Organism (human/mouse)

**Expected Outputs**:
- Spatial clustering plots with tissue coordinates
- Spatially variable genes ranked by Moran's I score
- Differential expression results between spatial clusters
- Quality control reports with tissue coverage metrics
- H5AD files for downstream analysis in Scanpy/Seurat

**Resource Requirements**:
- XSMALL for testing with nf-core test data
- SMALL-MEDIUM for real Visium datasets (1-4 sections)
- LARGE for multi-section experiments or Visium HD

**Test Data Available**: Yes - nf-core/test-datasets spatialvi branch

---

## Use Case 2: Tumor Microenvironment Spatial Profiling

**Priority**: P0

**Biological Question**: How do tumor cells interact with immune cells, fibroblasts, and vasculature in the tumor microenvironment?

**Target Audience**:
- Cancer researchers studying tumor biology
- Immunologists investigating anti-tumor immunity
- Drug discovery scientists analyzing treatment responses
- Pathologists characterizing tumor heterogeneity

**Typical Experimental Design**:
- Sample type: Tumor biopsies or resections on Visium slides
- Comparison: Tumor core vs invasive margin vs normal tissue
- Data type: Visium spatial transcriptomics
- Scale: 2-8 tissue sections (tumor + control)
- Organism: Human (patient samples) or mouse (tumor models)

**Scientific Use Cases**:
- Map immune infiltration patterns in tumors
- Identify tumor-stromal interaction zones
- Discover spatial biomarkers of treatment response
- Characterize cancer stem cell niches

**Key Parameters**:
- **Hardcoded**:
  - Focus on differential expression between spatial regions
  - Immune gene signature analysis
  - Spatial neighborhood analysis

- **Exposed**:
  - Input samplesheet with tumor sections
  - Reference genome
  - Output directory
  - Organism

**Expected Outputs**:
- Spatial maps of tumor vs stromal vs immune regions
- Ligand-receptor interaction predictions
- Spatially variable immune markers
- Differential expression: tumor core vs margin

**Resource Requirements**: MEDIUM-LARGE (tumor data often larger)

---

## Use Case 3: Brain Region Spatial Transcriptomics

**Priority**: P1

**Biological Question**: How do gene expression patterns define anatomical structures and functional zones in the brain?

**Target Audience**:
- Neuroscientists studying brain organization
- Neurologists investigating neurodegenerative diseases
- Developmental biologists mapping brain development
- Psychiatrists studying mental health disorders

**Typical Experimental Design**:
- Sample type: Brain tissue sections (cortex, hippocampus, etc.)
- Data type: Visium spatial transcriptomics
- Scale: 2-12 sections across brain regions
- Organism: Mouse or human (post-mortem)

**Scientific Use Cases**:
- Map cortical layers and hippocampal zones
- Identify region-specific marker genes
- Study neuronal vs glial spatial distributions
- Characterize disease-affected brain regions

**Key Parameters**:
- **Hardcoded**:
  - Brain-specific gene sets for annotation
  - High-resolution clustering for fine anatomical structures

- **Exposed**:
  - Input samplesheet
  - Reference genome
  - Output directory
  - Organism

**Expected Outputs**:
- Spatial clustering matching anatomical structures
- Layer-specific and region-specific markers
- Spatially variable genes across brain regions
- Annotated spatial maps

**Resource Requirements**: SMALL-MEDIUM

---

## Use Case 4: Developmental Biology Spatial Mapping

**Priority**: P1

**Biological Question**: How do gene expression patterns change spatially during tissue development and organogenesis?

**Target Audience**:
- Developmental biologists studying embryogenesis
- Stem cell researchers analyzing differentiation
- Regenerative medicine scientists
- Evolutionary biologists comparing development

**Typical Experimental Design**:
- Sample type: Embryonic or developing tissue sections
- Time points: Multiple developmental stages
- Data type: Visium spatial transcriptomics
- Scale: 2-16 sections across stages/regions
- Organism: Mouse, zebrafish, or other model organisms

**Scientific Use Cases**:
- Map developmental gene expression gradients
- Identify organizing centers and signaling sources
- Track cell fate commitment spatially
- Discover novel developmental regulators

**Key Parameters**:
- **Hardcoded**:
  - Developmental gene signatures
  - Gradient detection algorithms
  - Spatial trajectory analysis

- **Exposed**:
  - Input samplesheet with developmental stages
  - Reference genome
  - Output directory
  - Organism

**Expected Outputs**:
- Spatial maps of developmental zones
- Morphogen gradient visualizations
- Stage-specific spatially variable genes
- Developmental trajectory analyses

**Resource Requirements**: SMALL-MEDIUM

---

## Implementation Priority

**Order of Implementation**:

1. **Use Case 1: 10x Visium Tissue Architecture Analysis** (IMPLEMENT FIRST)
   - Most general use case
   - Best test data availability
   - Foundation for other use cases
   - Broadest applicability

2. **Use Case 2: Tumor Microenvironment** (if Use Case 1 succeeds)
   - High biological impact
   - Strong clinical relevance
   - Builds on Use Case 1

3. **Use Case 3: Brain Spatial Analysis** (if resources permit)
   - Specialized but important application
   - Active research community

4. **Use Case 4: Developmental Mapping** (if resources permit)
   - More specialized use case
   - Fewer potential users

---

## Common Requirements Across Use Cases

**All use cases require**:
- 10x Genomics Visium platform data
- Tissue section images (H&E staining)
- Space Ranger outputs OR raw FASTQ files
- Reference genome (human or mouse primarily)

**All use cases produce**:
- Spatial cluster assignments
- Spatially variable genes
- Quality control metrics
- Interactive visualizations
- Analysis-ready H5AD files

**Resource considerations**:
- Visium v1/v2: ~5000 spots per section
- Visium HD: Up to 16.5M barcoded spots (requires LARGE nodes)
- Processing time: 1-4 hours per section (depending on workflow)