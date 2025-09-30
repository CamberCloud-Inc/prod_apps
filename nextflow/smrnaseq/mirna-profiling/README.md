# microRNA Profiling with nf-core/smrnaseq

## Overview
This Camber app implements the nf-core/smrnaseq pipeline (v2.3.1) for comprehensive microRNA (miRNA) profiling from small RNA sequencing data. The pipeline identifies and quantifies miRNAs, providing insights into post-transcriptional gene regulation.

## Biology Background
**MicroRNAs** are ~22 nucleotide non-coding RNAs that regulate gene expression by binding to messenger RNAs (mRNAs) and repressing translation or promoting mRNA degradation. They play critical roles in:
- Development and differentiation
- Cell cycle regulation
- Apoptosis and stress response
- Disease mechanisms (cancer, neurodegeneration)
- Immune response

Small RNA-seq captures the entire small RNA repertoire, enabling discovery of:
- Known miRNAs from miRBase
- Novel miRNAs through computational prediction
- Other small non-coding RNAs (piRNAs, snoRNAs, etc.)
- miRNA expression changes between conditions

## Target Users
This pipeline is designed for:
- **Molecular biologists** studying post-transcriptional gene regulation
- **Cancer researchers** investigating oncogenic miRNAs
- **Developmental biologists** tracking miRNA expression during differentiation
- **Clinical researchers** discovering circulating miRNA biomarkers
- **Pharmaceutical scientists** identifying miRNA therapeutic targets

## Pipeline Features

### Analysis Steps
1. **Quality Control** (FastQC)
   - Raw read quality assessment
   - Adapter content detection
   - Length distribution analysis

2. **Adapter Trimming** (fastp)
   - Remove 3' adapter sequences
   - Filter by length (17-100nt, miRNA-specific range)
   - Quality filtering

3. **Contamination Filtering**
   - Remove rRNA sequences
   - Filter tRNA sequences
   - Remove other non-miRNA contaminants

4. **miRNA Quantification**
   - Align to miRBase mature miRNAs
   - Quantify precursor miRNAs
   - Generate expression matrices

5. **miRNA QC** (miRTrace)
   - Species composition assessment
   - Contamination detection
   - RNA type classification

6. **Novel miRNA Discovery** (optional, miRDeep2)
   - Predict novel miRNAs from reads
   - Score by miRNA characteristics
   - Generate precursor structures

7. **Comprehensive Reporting** (MultiQC)
   - Aggregated QC metrics
   - Sample comparison plots
   - Interactive HTML report

### Hardcoded Optimizations
- **Length filtering**: 17-100nt (optimal for miRNAs)
- **Adapter detection**: Automatic Illumina adapter recognition
- **Protocol**: Illumina small RNA library prep (standard)
- **Database**: miRBase v22 (comprehensive miRNA annotations)

### Exposed Parameters
1. **Sample Sheet** (`--input`)
   - CSV format: `sample,fastq_1`
   - Single-end FASTQ files
   - Support for URLs or local paths

2. **Reference Genome** (`--genome`)
   - iGenomes references: GRCh38, GRCm38, etc.
   - Must match organism of study
   - Includes genome sequence for novel miRNA discovery

3. **miRTrace Species** (`--mirtrace_species`)
   - Three-letter miRBase code
   - Examples: hsa (human), mmu (mouse), rno (rat)
   - Used for QC and contamination assessment

4. **Output Directory** (`--outdir`)
   - Location for all results
   - Includes counts, reports, QC files

## Input Requirements

### Sample Sheet Format
```csv
sample,fastq_1
Control_Rep1,/path/to/control_1.fastq.gz
Control_Rep2,/path/to/control_2.fastq.gz
Treatment_Rep1,/path/to/treated_1.fastq.gz
Treatment_Rep2,/path/to/treated_2.fastq.gz
```

**Important Notes:**
- Small RNA-seq is **single-end** sequencing
- FASTQ files should be **gzip compressed**
- Sample names must be **unique**
- Can use **URLs** for public data (https://, s3://, etc.)

### Species Code Reference
| Organism | Genome | miRTrace Code |
|----------|--------|---------------|
| Human | GRCh38 | hsa |
| Mouse | GRCm38 | mmu |
| Rat | Rnor_6.0 | rno |
| C. elegans | WBcel235 | cel |
| Drosophila | BDGP6 | dme |
| Zebrafish | GRCz11 | dre |
| Arabidopsis | TAIR10 | ath |

## Key Outputs

### miRNA Expression Data
- `mirna_counts/miRBase_mature_counts.tsv` - Mature miRNA counts matrix
- `mirna_counts/miRBase_hairpin_counts.tsv` - Precursor miRNA counts
- `edger/` - Differential expression analysis (if enabled)

### Quality Control
- `multiqc/multiqc_report.html` - Comprehensive QC report
- `fastqc/` - Raw read QC metrics
- `mirtrace/mirtrace-report.html` - miRNA-specific QC

### Processed Data
- `fastp/` - Trimmed and filtered FASTQ files
- `mirdeep2/` - Novel miRNA predictions (if enabled)
- `pipeline_info/` - Execution reports and resource usage

### Visualization Files
- `mirtrace/mirtrace-stats-*.json` - Interactive plots data
- `multiqc_data/` - Data for custom visualizations

## Computational Requirements

### Resource Recommendations
| Dataset Size | Samples | Node Size | Expected Runtime |
|--------------|---------|-----------|------------------|
| Small/Test | 3-5 | SMALL | 15-30 min |
| Typical | 10-50 | MEDIUM | 1-2 hours |
| Large | 50+ | LARGE | 2-4 hours |

### Resource Considerations
- **Memory**: 8-16GB per sample for alignment
- **Storage**: ~2GB per sample for intermediate files
- **Network**: Downloads miRBase database (~50MB)

## Test Data
The app includes test data from nf-core/test-datasets:
- **Species**: Human (Homo sapiens)
- **Samples**: 3 test samples (Clone1_N1, Clone1_N3, Control_N1)
- **Source**: Public small RNA-seq data
- **Expected Runtime**: 15-20 minutes on MEDIUM node

### Test Command
```bash
nextflow run nf-core/smrnaseq \
  --input samplesheet.csv \
  --outdir results \
  --genome GRCh38 \
  --mirtrace_species hsa \
  -r 2.3.1 \
  -profile singularity
```

## Biological Interpretation

### Understanding miRNA Counts
- **Raw counts**: Number of reads mapping to each miRNA
- **Normalization**: TPM (Transcripts Per Million) for comparison
- **High abundance**: >1000 reads typically indicates functional relevance
- **Low abundance**: May still be biologically important in specific contexts

### Common Analysis Patterns
1. **Differential Expression**
   - Compare treatment vs. control
   - Identify dysregulated miRNAs
   - Statistical testing (DESeq2, edgeR)

2. **Target Prediction**
   - Use miRNA sequences to predict mRNA targets
   - Tools: TargetScan, miRanda, miRDB
   - Pathway enrichment analysis

3. **Biomarker Discovery**
   - Identify disease-specific miRNAs
   - Validate in independent cohorts
   - Assess diagnostic/prognostic value

### Quality Metrics to Check
- **Total reads**: >1M per sample (typical)
- **miRNA %**: >30% for good libraries
- **Species match**: >80% expected species
- **Adapter content**: Should be trimmed to <5%
- **Length distribution**: Peak at 20-23nt

## Troubleshooting

### Common Issues

**Low miRNA percentage (<20%)**
- Check library prep protocol
- Verify correct adapter sequences
- May indicate RNA degradation

**High contamination**
- Significant rRNA/tRNA presence
- May need better depletion
- Check RNA extraction protocol

**Species mismatch**
- Verify genome and mirtrace_species match
- Check for sample mixup
- May indicate contamination

**Failed alignment**
- Check FASTQ file integrity
- Verify genome reference correctness
- Check adapter trimming success

## Technical Details

### Software Versions
- **Pipeline**: nf-core/smrnaseq v2.3.1
- **Nextflow**: ≥23.04.0
- **Container**: Singularity (Camber platform)

### Key Tools
- **FastQC** v0.12.1: Quality control
- **fastp** v0.23.4: Adapter trimming
- **Bowtie** v1.3.1: Short read alignment
- **miRDeep2** v2.0.5: Novel miRNA prediction
- **miRTrace** v1.0.1: miRNA-specific QC
- **MultiQC** v1.18: Report aggregation

### References
- **miRBase** v22: miRNA sequences and annotations
- **Ensembl iGenomes**: Reference genomes and annotations

## Citations

### Pipeline
Ewels PA, et al. (2020). nf-core: Community curated bioinformatics pipelines. *Nature Biotechnology*. https://doi.org/10.1038/s41587-020-0439-x

### Key Tools
- **miRBase**: Kozomara A, et al. (2019). miRBase: from microRNA sequences to function. *Nucleic Acids Research*. https://doi.org/10.1093/nar/gky1141
- **miRTrace**: Kang W, et al. (2018). miRTrace reveals the organismal origins of microRNA sequencing data. *Genome Biology*. https://doi.org/10.1186/s13059-018-1588-9
- **miRDeep2**: Friedländer MR, et al. (2012). miRDeep2 accurately identifies known and hundreds of novel microRNA genes. *Nucleic Acids Research*. https://doi.org/10.1093/nar/gkr688

## Support
For pipeline issues:
- nf-core Slack: https://nf-co.re/join
- GitHub Issues: https://github.com/nf-core/smrnaseq/issues

For Camber platform support:
- Contact: support@cambercloud.com