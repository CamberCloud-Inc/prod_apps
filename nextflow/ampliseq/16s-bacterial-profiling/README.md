# 16S Bacterial Community Profiling - nf-core/ampliseq

Camber app for characterizing bacterial communities from 16S rRNA V3-V4 amplicon sequencing data using the nf-core/ampliseq pipeline.

## Overview

This application analyzes paired-end Illumina sequencing data from 16S rRNA gene amplicons to:
- Characterize bacterial community composition
- Identify bacterial taxa with species-level resolution
- Calculate diversity metrics (alpha and beta diversity)
- Generate publication-ready visualizations

**Target Users:** Microbiome researchers, environmental microbiologists, clinical microbiome scientists

**Biological Context:** The 16S rRNA gene contains hypervariable regions that enable bacterial identification. This app targets the V3-V4 region (spanning ~460bp), which provides optimal taxonomic resolution for most bacterial taxa.

## Pipeline Workflow

1. **Quality Control** (FastQC): Assess raw read quality
2. **Primer Trimming** (Cutadapt): Remove V3-V4 primers from reads
3. **ASV Inference** (DADA2): Denoise and generate Amplicon Sequence Variants
4. **Taxonomic Classification** (SILVA v138): Assign taxonomy to ASVs
5. **Diversity Analysis** (QIIME2): Calculate alpha/beta diversity metrics
6. **Visualization** (MultiQC): Generate comprehensive QC and results reports

## Configuration

### Hardcoded Parameters

The following parameters are hardcoded for optimal bacterial 16S V3-V4 analysis:

- **Forward Primer:** `GTGYCAGCMGCCGCGGTAA` (341F primer, V3-V4 region)
- **Reverse Primer:** `GGACTACNVGGGTWTCTAAT` (805R primer, V3-V4 region)
- **Pipeline Version:** `2.9.0` (nf-core/ampliseq)
- **Execution Profile:** `singularity` (containerized execution)
- **Taxonomy Database:** SILVA (automatically downloaded by pipeline)

### User Inputs

Users provide two required inputs:

1. **Sample Sheet** (`input`): CSV file with columns:
   - `sampleID`: Unique sample identifier
   - `forwardReads`: Path or URL to R1 FASTQ file
   - `reverseReads`: Path or URL to R2 FASTQ file
   - `run`: Sequencing run identifier

2. **Output Directory** (`outdir`): Directory where results will be saved

### Example Samplesheet

```csv
sampleID,forwardReads,reverseReads,run
sample1,/path/to/sample1_R1.fastq.gz,/path/to/sample1_R2.fastq.gz,run1
sample2,/path/to/sample2_R1.fastq.gz,/path/to/sample2_R2.fastq.gz,run1
sample3,/path/to/sample3_R1.fastq.gz,/path/to/sample3_R2.fastq.gz,run1
```

## Test Data

Test dataset from nf-core/test-datasets (ampliseq branch):
- Location: `samplesheet.csv` in this directory
- Contains: 4 samples from 16S V3-V4 sequencing
- Source: https://github.com/nf-core/test-datasets/tree/ampliseq

## Usage

### 1. Create the App

```bash
camber app create --file app.json
```

### 2. Run the App

```bash
camber app run ampliseq-16s-bacterial \
  --input input=samplesheet.csv \
  --input outdir=results
```

### 3. Monitor Job Status

```bash
camber job get <JOB_ID>
```

### 4. View Logs

```bash
camber job logs <JOB_ID>
```

## Output Structure

```
results/
├── dada2/
│   ├── ASV_table.tsv              # ASV abundance table
│   ├── ASV_tax.tsv                # Taxonomic assignments
│   ├── ASV_seqs.fasta             # ASV sequences
│   └── DADA2_stats.tsv            # DADA2 processing statistics
├── qiime2/
│   └── diversity/
│       ├── alpha_rarefaction/     # Alpha diversity metrics
│       └── core-metrics-results/  # Beta diversity metrics
├── multiqc/
│   └── multiqc_report.html        # Comprehensive QC report
└── pipeline_info/
    └── execution_report.html      # Nextflow execution report
```

## Key Outputs

### 1. ASV Table (`dada2/ASV_table.tsv`)
Matrix of ASV counts per sample - the core data for downstream analysis

### 2. Taxonomy (`dada2/ASV_tax.tsv`)
Taxonomic assignments for each ASV from Kingdom to Species level

### 3. Diversity Metrics (`qiime2/diversity/`)
- **Alpha diversity**: Within-sample diversity (Shannon, Simpson, Chao1)
- **Beta diversity**: Between-sample diversity (Bray-Curtis, UniFrac)

### 4. QC Report (`multiqc/multiqc_report.html`)
Interactive HTML report with quality metrics, read statistics, and taxonomic summaries

## Computational Resources

The app offers three resource tiers:

- **SMALL**: Test datasets (<10 samples)
- **MEDIUM** (Recommended): Typical studies (20-100 samples)
- **LARGE**: Large studies (>100 samples)

## Technical Details

### Command Structure

The app executes the following command (with user inputs substituted):

```bash
nextflow run nf-core/ampliseq \
  --input ${input} \
  --outdir ${outdir} \
  --FW_primer GTGYCAGCMGCCGCGGTAA \
  --RV_primer GGACTACNVGGGTWTCTAAT \
  -r 2.9.0 \
  -profile singularity
```

### No Config Files

All parameters are specified directly in the command within `app.json`. No external configuration files are used, ensuring:
- Simplified deployment
- Transparent parameter specification
- Easy version control
- Reproducible execution

## Validation

### App Creation

```bash
$ camber app create --file app.json
App created successfully

Name:                ampliseq-16s-bacterial
Title:               16S Bacterial Community Profiling (nf-core/ampliseq)
Engine Type:         NEXTFLOW
Command:             nextflow run nf-core/ampliseq --input ${input} --outdir ${outdir} --FW_primer GTGYCAGCMGCCGCGGTAA --RV_primer GGACTACNVGGGTWTCTAAT -r 2.9.0 -profile singularity
Version:             1.0.0
```

### Test Run

```bash
$ camber app run ampliseq-16s-bacterial \
  --input input=samplesheet.csv \
  --input outdir=results

Job ID: 4325
Status: PENDING
```

## References

1. **nf-core/ampliseq pipeline**: https://nf-co.re/ampliseq
2. **SILVA database**: https://www.arb-silva.de/
3. **DADA2**: Callahan et al. (2016) Nature Methods. DOI: 10.1038/nmeth.3869
4. **Publication**: Straub et al. (2020) Frontiers in Microbiology. DOI: 10.3389/fmicb.2020.550420

## Version History

- **v1.0.0** (2025-09-30): Initial release
  - nf-core/ampliseq v2.9.0
  - Hardcoded V3-V4 primers (GTGYCAGCMGCCGCGGTAA / GGACTACNVGGGTWTCTAAT)
  - SILVA database for taxonomic classification
  - Simplified input (samplesheet and output directory only)

## Support

For issues with:
- **Camber app**: Contact Camber support
- **nf-core/ampliseq pipeline**: https://github.com/nf-core/ampliseq/issues
- **Scientific questions**: Refer to the nf-core/ampliseq documentation and published literature