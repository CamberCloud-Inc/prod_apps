# Microbiome Taxonomic Profiling with Kraken2

## Use Case: Rapid Taxonomic Classification for Microbiome Studies

**App Name**: `taxprofiler-microbiome-kraken2`

**Version**: nf-core/taxprofiler 1.2.3

**Last Updated**: 2025-09-30

---

## Overview

This app performs rapid taxonomic classification of metagenomic sequencing data using Kraken2, the fastest k-mer based classifier. It's designed for microbiome researchers who need to quickly identify and quantify microorganisms in their samples.

### What It Does

- **Taxonomic Classification**: Assigns taxonomic labels to sequencing reads using Kraken2
- **Abundance Estimation**: Estimates relative abundances using Bracken (Bayesian reestimation)
- **Quality Control**: Assesses read quality and classification rates
- **Standardized Outputs**: Produces analysis-ready taxonomic tables

### Why Kraken2

- **Speed**: Processes millions of reads per minute
- **Accuracy**: High precision for well-characterized organisms
- **Flexibility**: Works with custom databases for specific research needs
- **Standard Tool**: Widely used and validated in the field

---

## Input Requirements

### 1. Sample Information Sheet (CSV)

Required columns:
- `sample`: Unique sample identifier
- `run_accession`: Sequencing run ID (can match sample)
- `instrument_platform`: `ILLUMINA` or `OXFORD_NANOPORE`
- `fastq_1`: Path to Read 1 FASTQ file
- `fastq_2`: Path to Read 2 FASTQ file (empty for single-end)
- `fasta`: Path to FASTA file (empty if using FASTQ)

**Example**:
```csv
sample,run_accession,instrument_platform,fastq_1,fastq_2,fasta
gut_ctrl_1,run001,ILLUMINA,ctrl1_R1.fastq.gz,ctrl1_R2.fastq.gz,
gut_treat_1,run002,ILLUMINA,treat1_R1.fastq.gz,treat1_R2.fastq.gz,
soil_sample,run003,ILLUMINA,soil_R1.fastq.gz,,
```

### 2. Database Information Sheet (CSV)

Required columns:
- `tool`: Must be `kraken2` for this app
- `db_name`: Descriptive database name
- `db_params`: Optional Kraken2 parameters (e.g., `--quick`)
- `db_type`: `short` for Illumina short reads
- `db_path`: Path to Kraken2 database directory or .tar.gz

**Example**:
```csv
tool,db_name,db_params,db_type,db_path
kraken2,standard,--quick,short,/data/kraken2_standard_db
```

**Common Databases**:
- Standard: archaea, bacteria, viruses, human (~50GB)
- PlusPF: Standard + protozoa + fungi (~75GB)
- PlusPFP: PlusPF + plants (~100GB)

### 3. Sequencing Data

- **Format**: FASTQ (gzipped)
- **Type**: Illumina paired-end or single-end
- **Depth**: 1-10M reads for basic profiling
- **Quality**: Standard Illumina quality scores

---

## Expected Outputs

### Main Results

Located in `output/results/`:

1. **Kraken2 Classification Reports** (`kraken2/`)
   - `.kreport` files: Detailed taxonomic breakdown per sample
   - `.kraken2.report.txt`: Standard Kraken2 output format

2. **Bracken Abundance Estimates** (`bracken/`)
   - Species-level abundance refinement
   - More accurate abundance estimates than raw Kraken2

3. **Standardized Tables** (`taxpasta/`)
   - Combined abundance tables across all samples
   - Ready for downstream analysis in R/Python

4. **Quality Control** (`multiqc/`)
   - MultiQC report with all sample QC metrics
   - Classification rates and read quality

5. **Krona Charts** (if enabled)
   - Interactive hierarchical taxonomic visualizations

### File Formats

- **Kraken2 Reports**: Tab-separated with taxonomy tree structure
- **Bracken Output**: Abundance estimates at species level
- **TAXPASTA**: Standardized TSV tables for cross-tool comparison
- **MultiQC HTML**: Interactive quality control dashboard

---

## Resource Requirements

| Dataset Size | Node Size | RAM | Runtime Estimate |
|--------------|-----------|-----|------------------|
| Test data (nf-core) | XSMALL | 15GB | 10-20 min |
| 1-5 samples, 1-5M reads | SMALL | 30GB | 30-60 min |
| 5-20 samples, 5M reads | MEDIUM | 120GB | 1-3 hours |
| 20-50 samples | LARGE | 360GB | 3-6 hours |

**Note**: Runtime heavily depends on:
- Database size (larger databases = more memory needed)
- Total number of reads
- Whether using `--quick` mode (faster but slightly less sensitive)

---

## Testing with nf-core Data

The app is pre-configured with nf-core test data URLs for easy testing:

**Sample Sheet**: `https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/samplesheet.csv`

**Database Sheet**: `https://raw.githubusercontent.com/nf-core/test-datasets/taxprofiler/database_v1.2.csv`

These miniature datasets are perfect for validating the app works correctly before running production data.

---

## Parameters Hardcoded for This Use Case

The following parameters are pre-configured for microbiome profiling:

- `--run_kraken2`: Enable Kraken2 profiler
- `--run_bracken`: Enable Bracken abundance refinement
- `--perform_runmerging`: Merge multiple runs per sample
- `--skip_downstream_qc`: Skip optional downstream QC (faster)
- `--skip_krona`: Skip Krona chart generation (can be slow)
- `-profile singularity`: Use Singularity containers (Camber compatible)

Users only need to provide:
1. Sample sheet (their sequencing data)
2. Database sheet (which Kraken2 database to use)
3. Output directory

---

## Troubleshooting

### Common Issues

**Issue**: "Database not found"
- **Solution**: Ensure database path in database sheet is absolute and accessible
- **Note**: For Camber platform, databases must be in stash or accessible storage

**Issue**: "Out of memory"
- **Solution**: Standard Kraken2 DB requires ~50GB RAM minimum. Use MEDIUM or LARGE node
- **Alternative**: Use smaller custom database or `--quick` mode

**Issue**: "No reads classified"
- **Solution**: Check database contains appropriate organisms for your sample type
- **Note**: Environmental samples need environmental databases, not just human pathogens

**Issue**: "Bracken fails"
- **Solution**: Ensure database was built with Bracken support (includes `database*mers.kmer_distrib`)
- **Alternative**: Run Kraken2 only without Bracken

---

## Biological Interpretation

### Understanding Kraken2 Reports

Columns in `.kreport`:
1. Percentage of reads
2. Number of reads at this taxon
3. Number of reads directly assigned
4. Taxonomic rank (U, D, P, C, O, F, G, S)
5. NCBI taxonomy ID
6. Scientific name

### Classification Rate

- **High (>80%)**: Good database match to sample
- **Medium (50-80%)**: Partial database coverage
- **Low (<50%)**: May indicate novel organisms or contamination

### Next Steps After Profiling

1. **Alpha Diversity**: Calculate species richness and diversity metrics
2. **Beta Diversity**: Compare taxonomic composition between samples
3. **Differential Abundance**: Find organisms enriched in conditions
4. **Functional Profiling**: Predict metabolic capabilities (separate analysis)

---

## Citations

**nf-core/taxprofiler**:
- Stamouli, S., et al. (2023). nf-core/taxprofiler: Highly parallelised and flexible pipeline for metagenomic taxonomic classification and profiling. bioRxiv.

**Kraken2**:
- Wood, D.E., Lu, J., Langmead, B. (2019). Improved metagenomic analysis with Kraken 2. Genome Biology, 20(1), 257.

**Bracken**:
- Lu, J., et al. (2017). Bracken: estimating species abundance in metagenomics data. PeerJ Computer Science, 3, e104.

---

## Advanced Configuration

For advanced users who need custom parameters, you can modify the command in the app definition to add:

- `--perform_shortread_qc`: Enable additional read QC and trimming
- `--shortread_qc_tool fastp`: Specify QC/trimming tool
- `--perform_shortread_hostremoval`: Remove host reads (e.g., human)
- `--hostremoval_reference /path/to/human_genome.fasta`: Host genome for removal
- `--kraken2_save_reads`: Save classified/unclassified reads
- `--kraken2_save_readclassifications`: Save per-read classifications

---

## Support

- **Pipeline Documentation**: https://nf-co.re/taxprofiler
- **GitHub Issues**: https://github.com/nf-core/taxprofiler/issues
- **nf-core Slack**: https://nfcore.slack.com (channel: #taxprofiler)

---

## Version History

- **v1.0** (2025-09-30): Initial implementation with Kraken2 + Bracken
  - Based on nf-core/taxprofiler 1.2.3
  - Optimized for microbiome profiling use case
  - XSMALL default for testing