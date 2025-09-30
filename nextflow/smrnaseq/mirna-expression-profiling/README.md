# miRNA Expression Profiling

## Overview

This Camber app quantifies microRNA (miRNA) expression from small RNA sequencing data using the nf-core/smrnaseq pipeline (v2.4.0).

## Use Case

**Research Question**: What are the expression levels of known miRNAs in my samples?

**Target Users**:
- Cancer researchers studying miRNA dysregulation
- Developmental biologists tracking miRNA expression changes
- Disease researchers comparing healthy vs. diseased tissues
- Biomarker discovery projects

## What This App Does

1. **Quality Control**: Assess raw read quality with FastQC
2. **Adapter Trimming**: Remove adapter sequences automatically
3. **Size Filtering**: Filter reads to expected small RNA size range (18-30 nt)
4. **Contamination Removal**: Filter out rRNA, tRNA, and other contaminants
5. **miRNA Quantification**: Count reads mapping to known miRNAs
6. **Expression Matrix**: Generate normalized expression tables
7. **miRTrace QC**: Small RNA-specific quality metrics
8. **MultiQC Report**: Comprehensive quality control summary

## Input Requirements

### Samplesheet Format

CSV file with two columns:
- `sample`: Unique sample identifier
- `fastq_1`: Path or URL to single-end FASTQ file

**Example**:
```csv
sample,fastq_1
Control_Rep1,stash://username/data/control_1.fastq.gz
Control_Rep2,stash://username/data/control_2.fastq.gz
Treatment_Rep1,stash://username/data/treatment_1.fastq.gz
Treatment_Rep2,stash://username/data/treatment_2.fastq.gz
```

### Data Requirements

- **Sequencing**: Single-end small RNA-seq (typically 50-75 bp reads)
- **Library Prep**: Adapter-ligated small RNA library (Illumina TruSeq, QIAseq, etc.)
- **Depth**: 5-10 million reads per sample minimum
- **Replicates**: Minimum 3 biological replicates per condition
- **Size Selection**: 18-30 nt during library prep (captures miRNAs)

## Parameters

### Required

1. **Sample Sheet**: CSV file with sample information
2. **Output Directory**: Where results will be saved
3. **Reference Genome**: Match your experimental organism (e.g., GRCh38 for human)
4. **Species Code**: For miRTrace QC (e.g., 'hsa' for human, 'mmu' for mouse)

### Hardcoded (Best Practices)

- Pipeline version: 2.4.0
- Quantification method: EdgeR + Mirtop
- Quality filtering: Standard thresholds
- Adapter detection: Automatic
- Contamination filtering: Enabled

## Outputs

### Key Result Files

```
results/
├── edger/
│   ├── counts.tsv                    # Raw miRNA count matrix
│   └── normalized_counts.tsv          # Normalized expression values
├── mirtrace/
│   └── mirtrace-report.html          # Small RNA-specific QC
├── multiqc/
│   └── multiqc_report.html           # Comprehensive QC report
├── fastqc/
│   └── *.html                        # Per-sample quality reports
├── trimgalore/
│   └── *.fastq.gz                    # Trimmed reads
└── bowtie/
    └── *.bam                         # Aligned reads
```

### Main Outputs Explained

1. **counts.tsv**: Raw read counts for each miRNA in each sample
   - Rows: miRNAs
   - Columns: Samples
   - Use for differential expression analysis

2. **normalized_counts.tsv**: Normalized expression values
   - Accounts for library size differences
   - Ready for visualization and comparison

3. **mirtrace-report.html**: Small RNA-specific QC
   - RNA type composition
   - miRNA complexity
   - Length distribution
   - Quality metrics

4. **multiqc_report.html**: Overall quality summary
   - All samples in one report
   - FastQC metrics
   - Alignment statistics
   - Adapter content

## Quality Metrics to Check

### Good Library Indicators

- ✅ **Read length peak at ~22 nt**: Indicates miRNA enrichment
- ✅ **>50% miRNA content**: Good miRNA capture
- ✅ **<5% rRNA/tRNA**: Low contamination
- ✅ **High adapter content**: Normal (miRNAs shorter than read length)

### Potential Issues

- ⚠️ **Flat length distribution**: Poor size selection
- ⚠️ **Low miRNA %**: Library quality issues
- ⚠️ **High rRNA %**: RNA extraction contamination
- ⚠️ **Low mapping rate**: Wrong reference genome

## Compute Resources

- **XSMALL**: Testing with nf-core test data (~10-15 min)
- **SMALL**: Typical studies with 10-50 samples (recommended)
- **MEDIUM**: Large studies with >50 samples

## Testing

Test data from nf-core:
```bash
# Test samplesheet included: test_samplesheet.csv
# 8 human samples with 3 biological groups
# Species: hsa (human)
# Expected runtime: 10-15 minutes on XSMALL
```

## Downstream Analysis

After this pipeline, you can:

1. **Differential Expression**: Use counts.tsv with DESeq2 or edgeR
2. **Clustering**: Hierarchical clustering of samples by miRNA expression
3. **Target Prediction**: Identify mRNA targets of differentially expressed miRNAs
4. **Pathway Analysis**: Enrichment analysis of miRNA target genes
5. **Biomarker Validation**: Validate candidate biomarkers in independent cohorts

## Common Use Cases

### Cancer Research
Compare tumor vs. normal tissue to identify oncogenic miRNAs (oncomiRs) or tumor suppressor miRNAs.

### Developmental Biology
Track miRNA expression changes during cell differentiation or tissue development.

### Disease Studies
Identify miRNA dysregulation in disease states (neurodegeneration, cardiovascular, metabolic diseases).

### Drug Response
Study miRNA changes after drug treatment to understand mechanisms of action.

## References

- nf-core/smrnaseq: https://nf-co.re/smrnaseq/2.4.0
- miRBase (miRNA database): https://mirbase.org
- miRTrace paper: DOI: 10.1186/s13059-018-1588-9
- 2024 Nobel Prize in Physiology or Medicine: miRNA discovery

## Support

For pipeline issues, see: https://github.com/nf-core/smrnaseq/issues
