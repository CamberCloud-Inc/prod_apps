# Tumor-Phylogeny App.json Enhancement Report

## Summary
Successfully enhanced `/Users/david/git/prod_apps/nextflow/tumourevo/tumor-phylogeny/app.json` with comprehensive documentation, fixed command structure, and rich content based on official nf-core/tumourevo pipeline documentation.

## What Was Changed

### 1. Fixed Command Line (Critical Bug Fix)
**Before:**
```bash
nextflow run nf-core/tumourevo --input ${input} --outdir ${outdir} -r  Clonal evolution and tumor heterogeneity:1.0.0 
```
**Issues:** Malformed `-r` parameter with embedded text instead of version tag

**After:**
```bash
nextflow run nf-core/tumourevo --input ${input} --outdir ${outdir} --tools ${tools} -r ${revision}
```
**Improvements:**
- Fixed `-r` parameter to accept proper version tags
- Added `--tools` parameter for selecting analysis tools
- Made version configurable via UI
- Follows nf-core standard command patterns

### 2. Enhanced Title and Description
**Before:**
- Title: "Tumor Evolution"
- Description: " Phylogenetic Analysis" (minimal, with leading space)

**After:**
- Title: "Tumor Clonal Evolution Analysis"
- Description: "Comprehensive phylogenetic analysis to reconstruct tumor evolution from whole-genome sequencing data. Models clonal populations, mutational signatures, and evolutionary processes driving tumor development from variant and copy-number calls."

### 3. Rich Content Documentation
Expanded from 2 lines to comprehensive HTML documentation covering:

#### Core Sections Added:
- **What This Analysis Does**: Clear explanation of tumor evolution analysis
- **When To Use This**: 7 specific use cases (heterogeneity, multi-region, longitudinal, treatment response, metastasis, cancer evolution, cohort studies)
- **What You Need**: Detailed input requirements
  - Samplesheet format with all 10 required columns explained
  - VCF file requirements and supported callers
  - Copy number data specifications
- **Analysis Tools**: Complete list of selectable tools
  - Subclonal deconvolution: PyClone-VI, MOBSTER, VIBER, Ctree
  - Signature analysis: SparseSignatures, SigProfiler
  - Recommended tool combinations
- **What You'll Get**: Comprehensive outputs
  - Clonal population analysis
  - Quality control reports
  - Mutational signatures
  - Driver annotations
  - Visualizations
- **Expected Analysis Time**: Realistic time estimates (2-24 hours based on sample count)
- **Scientific Background**: Methods and tools explanation
- **Key Concepts**: CCF, clonal evolution, subclonal structure, mutational signatures
- **Clinical Applications**: Treatment planning, metastasis prediction, minimal residual disease, biomarkers
- **Getting Started**: Step-by-step workflow

### 4. Improved Input Specifications
**Samplesheet (input):**
- Added detailed description of 10 required columns
- Kept proper file restrictions (.csv, .tsv)

**Output Directory:**
- Enhanced description explaining result organization

**New: Analysis Tools Selector:**
- Added dropdown with 9 tool options
- Individual tools (pyclonevi, mobster, viber, ctree, sparsesignatures, sigprofiler)
- Pre-configured combinations (Standard, Comprehensive, Quick)
- Default: "pyclonevi,mobster,viber,sparsesignatures"

**New: Pipeline Version:**
- Input field for version control
- Default: "dev" (latest)
- Supports version tags for reproducibility

### 5. Enhanced Job Configuration
**Before:** Single LARGE option only

**After:** Three resource tiers with descriptions:
- **Medium**: Testing only
- **Large**: Single sample (Recommended) - default
- **XLarge**: Multi-region or cohort studies

Added description: "Computational resources. Use LARGE for single samples, XLARGE for multi-region or cohort analyses."

### 6. Comprehensive Tagging
**Before:**
```json
[{"name": "tumourevo", "type": "task"}]
```

**After:**
```json
[
  {"name": "genomics", "type": "subfield"},
  {"name": "cancer-evolution", "type": "task"},
  {"name": "tumor-phylogeny", "type": "task"},
  {"name": "clonal-analysis", "type": "task"},
  {"name": "biology", "type": "field"}
]
```

## Documentation Sources
Information gathered from:
1. **nf-co.re/tumourevo/dev/** - Official pipeline documentation
2. **nf-co.re/tumourevo/output** - Output specifications
3. **Web search results** - Usage examples and parameters
4. **Similar nf-core pipelines** - sarek, rnaseq, raredisease patterns

## Key Technical Details Documented

### Samplesheet Format
10 required columns:
1. dataset - Study/cohort identifier
2. patient - Patient ID
3. tumour_sample - Tumor sample name
4. normal_sample - Normal sample name
5. vcf - Path to VCF file
6. tbi - VCF index file
7. cna_segments - Copy number segments
8. cna_extra - Additional CNA files
9. cna_caller - CNA tool used (ascat, battenberg, facets, purple, sequenza)
10. cancer_type - Cancer type code (LUAD, BRCA, etc.)

### Supported Analysis Tools
**Subclonal Deconvolution:**
- PyClone-VI: Bayesian clonal clustering
- MOBSTER: Beta-Binomial mixture models
- VIBER: Variational clone tree inference
- Ctree: Phylogenetic trees from PyClone

**Mutational Signatures:**
- SparseSignatures: Sparse signature identification
- SigProfiler: COSMIC signature extraction/fitting

### Quality Control
- CNAqc: Copy number and variant concordance validation
- TINC: Tumor contamination assessment
- VEP: Variant Effect Predictor for annotation

## Validation
- JSON syntax validated successfully
- Command structure follows nf-core standards
- Parameter names match pipeline expectations
- Resource configurations appropriate for workload

## Impact
This enhancement transforms the app.json from a minimal placeholder to a production-ready, user-friendly application with:
- **Fixed critical command bug** that would have prevented execution
- **Comprehensive user guidance** for proper usage
- **Flexible tool selection** for different analysis needs
- **Appropriate resource scaling** based on workload
- **Rich educational content** explaining tumor evolution analysis
- **Professional presentation** matching other nf-core apps

## File Location
`/Users/david/git/prod_apps/nextflow/tumourevo/tumor-phylogeny/app.json`
