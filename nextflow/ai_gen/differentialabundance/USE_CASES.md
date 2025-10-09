# Differential Abundance Analysis: Use Cases

## Overview

The nf-core/differentialabundance pipeline is a downstream analysis tool that takes count matrices and performs statistical comparison between experimental groups. It's commonly used after nf-core/rnaseq or proteomics pipelines.

---

## Use Case 1: RNA-seq Differential Expression (Two-Group Comparison) 🔥

**Priority**: P0 (Highest - Most Common)

### Biological Question
Which genes are differentially expressed between two experimental conditions (e.g., treatment vs control, disease vs healthy, knockout vs wild-type)?

### Target Audience
- Molecular biologists studying gene regulation
- Cancer researchers comparing tumor vs normal tissue
- Drug discovery scientists testing treatment effects
- Geneticists analyzing knockout phenotypes

### Typical Experimental Design
- **Sample Type**: Bulk RNA-seq count data (from nf-core/rnaseq)
- **Design**: Two groups (control vs treatment)
- **Replicates**: 3-6 biological replicates per group
- **Scale**: Analyzing thousands of genes across samples

### Input Requirements
1. **Gene Count Matrix**: TSV file with genes (rows) × samples (columns)
2. **Samplesheet**: CSV with sample IDs, condition labels, optional batch info
3. **Contrasts File**: CSV defining which groups to compare
4. **GTF File**: Gene annotations for functional context

### Key Parameters

**Hardcoded** (use-case specific):
- `--features_type`: "gene" (not transcript-level)
- `--deseq2_test`: "Wald" (standard two-group test)
- `--exploratory_clustering_method`: "ward.D2"
- `--exploratory_cor_method`: "spearman"
- `--features_log2_assays`: "normalised_counts" (for visualization)

**Exposed** (user-configurable):
- `--input`: Sample information sheet
- `--matrix`: Gene count matrix from RNA-seq
- `--contrasts`: Comparison definitions
- `--gtf`: Gene annotations
- `--outdir`: Output directory
- `--genome`: Reference genome (for annotation compatibility)

### Statistical Methods
- **Primary**: DESeq2 (default for RNA-seq)
- **Alternative**: edgeR, limma-voom (can be configured)

### Expected Outputs
1. **Differential Expression Tables**:
   - Log2 fold changes
   - Adjusted p-values (FDR)
   - Gene annotations
   - Significant genes lists

2. **Visualizations**:
   - Volcano plots (fold change vs significance)
   - MA plots (mean expression vs fold change)
   - Heatmaps of top genes
   - PCA plots for sample clustering

3. **Quality Control**:
   - Sample correlation matrices
   - Dispersion estimates
   - Count distribution plots

4. **Interactive Report**:
   - HTML report with all analyses
   - Optional Shiny app for data exploration

### Resource Requirements
- **Node Size**: XSMALL for testing (typical datasets < 10 samples)
- **Runtime**: 10-30 minutes for standard datasets
- **Memory**: 8-15GB sufficient for most experiments

### Example Experimental Scenarios
1. **Cancer Research**: Tumor vs adjacent normal tissue
2. **Drug Discovery**: Cells treated with compound vs vehicle control
3. **Genetics**: Gene knockout mice vs wild-type
4. **Immunology**: Activated vs resting immune cells
5. **Development**: Early vs late developmental stage

### Test Data
- **Dataset**: Mouse RNA-seq (SRP254919)
- **Source**: nf-core/test-datasets
- **Samples**: Multiple conditions with replicates
- **Size**: Top 1000 genes (manageable for testing)

---

## Use Case 2: Proteomics Differential Abundance

**Priority**: P1

### Biological Question
Which proteins show differential abundance between experimental conditions?

### Target Audience
- Proteomics researchers
- Systems biologists studying protein-level regulation
- Cancer researchers analyzing proteome changes
- Drug response studies

### Typical Experimental Design
- **Sample Type**: MaxQuant proteinGroups.txt or similar
- **Design**: Two or more conditions
- **Replicates**: 3-5 biological replicates
- **Scale**: Hundreds to thousands of proteins

### Input Requirements
1. **Protein Abundance Matrix**: Quantification from mass spectrometry
2. **Samplesheet**: Sample metadata with conditions
3. **Contrasts File**: Comparisons to perform
4. **Protein Annotations**: Optional protein ID mappings

### Key Parameters

**Hardcoded**:
- `--features_type`: "protein"
- `--limma_method`: "ls" (least squares for proteomics)
- `--exploratory_main_variable`: "condition"
- `--proteus_measurecol_prefix`: "Intensity" (MaxQuant format)
- `--proteus_norm_function`: "normalizeMedian"

**Exposed**:
- `--input`: Samplesheet
- `--matrix`: Protein quantification matrix
- `--contrasts`: Comparisons
- `--outdir`: Output directory

### Statistical Methods
- **Primary**: limma (standard for proteomics)
- **Alternative**: DEqMS (peptide-level consideration)

### Expected Outputs
- Differential abundance tables with fold changes
- Volcano plots and heatmaps
- Protein pathway enrichment (if annotations provided)

### Resource Requirements
- **Node Size**: XSMALL for testing, SMALL for production
- **Runtime**: 15-45 minutes

---

## Use Case 3: Multi-Factor RNA-seq Analysis (Complex Design)

**Priority**: P1

### Biological Question
How do genes respond to multiple factors (e.g., treatment + genotype + time point)?

### Target Audience
- Researchers with factorial experimental designs
- Studies with batch effects to correct
- Multi-condition comparison studies
- Interaction effect studies

### Typical Experimental Design
- **Sample Type**: Bulk RNA-seq count data
- **Design**: Multiple factors (2+ variables)
- **Example**: 2 genotypes × 2 treatments × 3 time points
- **Replicates**: 3+ per combination

### Input Requirements
1. **Gene Count Matrix**: From RNA-seq pipeline
2. **Samplesheet**: Multiple columns for factors (genotype, treatment, time, batch)
3. **Contrasts File**: Complex contrasts including interactions
4. **GTF File**: Gene annotations

### Key Parameters

**Hardcoded**:
- `--features_type`: "gene"
- `--deseq2_test`: "LRT" (likelihood ratio test for complex designs)
- `--blocking_variables`: "batch" (control for batch effects)
- `--exploratory_palette_name`: "Set1" (multi-color palette)

**Exposed**:
- `--input`: Samplesheet with multiple factors
- `--matrix`: Gene counts
- `--contrasts`: Complex contrast definitions
- `--gtf`: Annotations
- `--outdir`: Output directory

### Statistical Methods
- **DESeq2**: With model matrix for multiple factors
- **Batch correction**: Built-in blocking

### Expected Outputs
- Main effect and interaction analyses
- Factor-specific gene lists
- Batch-corrected visualizations
- Complex heatmaps showing multi-factor effects

### Resource Requirements
- **Node Size**: SMALL-MEDIUM (more complex models)
- **Runtime**: 30-90 minutes depending on model complexity

---

## Use Case 4: Time-Series Gene Expression Analysis

**Priority**: P2

### Biological Question
How does gene expression change over time in response to a stimulus?

### Target Audience
- Developmental biologists studying differentiation
- Circadian rhythm researchers
- Infection time-course studies
- Drug response kinetics

### Typical Experimental Design
- **Sample Type**: Bulk RNA-seq with multiple time points
- **Design**: Time series (e.g., 0h, 2h, 6h, 12h, 24h)
- **Replicates**: 3+ per time point
- **Analysis**: Trend detection, temporal patterns

### Input Requirements
1. **Gene Count Matrix**: Time-series RNA-seq data
2. **Samplesheet**: Time point information
3. **Contrasts File**: Time point comparisons
4. **GTF File**: Gene annotations

### Key Parameters

**Hardcoded**:
- `--features_type`: "gene"
- `--deseq2_test`: "LRT" (for time trend)
- `--time_variable`: "time_point"
- `--exploratory_clustering_method`: "ward.D2"

**Exposed**:
- `--input`: Samplesheet with time information
- `--matrix`: Gene counts
- `--contrasts`: Sequential time comparisons
- `--gtf`: Annotations
- `--outdir`: Output directory

### Statistical Methods
- **DESeq2**: LRT test for time effect
- **Trend analysis**: Linear and polynomial models

### Expected Outputs
- Time-dependent gene expression profiles
- Temporal clustering (early/late response genes)
- Trajectory plots
- Dynamic heatmaps

### Resource Requirements
- **Node Size**: SMALL-MEDIUM
- **Runtime**: 20-60 minutes

---

## Priority Ranking Summary

1. **P0 - RNA-seq Two-Group Comparison**: Most common, simplest, best tested
2. **P1 - Proteomics Differential Abundance**: Common in proteomics labs
3. **P1 - Multi-Factor RNA-seq**: Important but complex
4. **P2 - Time-Series Analysis**: Specialized but valuable

## Implementation Order

We will implement in priority order:
1. ✅ **First**: RNA-seq Two-Group (P0) - most users, clearest use case
2. **Second**: Proteomics Abundance (P1) - different data modality
3. **Third**: Multi-Factor RNA-seq (P1) - more complex
4. **Fourth**: Time-Series (P2) - specialized

---

## Common Parameters Across All Use Cases

### Input Files
- Samplesheet (CSV): Always required
- Matrix (TSV): Feature × sample abundances
- Contrasts (CSV/YAML): Comparison definitions

### Optional Enhancements
- Gene set enrichment (`--gsea_run`)
- Interactive Shiny app (`--shinyngs_build_app`)
- Custom feature annotations

### Output Structure
```
results/
├── differential/
│   ├── deseq2_results.tsv
│   ├── volcano_plots.pdf
│   └── heatmaps.pdf
├── exploratory/
│   ├── pca_plot.pdf
│   ├── sample_correlations.pdf
│   └── clustering.pdf
├── qc/
│   └── multiqc_report.html
└── report.html
```