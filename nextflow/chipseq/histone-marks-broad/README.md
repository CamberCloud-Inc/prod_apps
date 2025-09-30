# ChIP-seq: Histone Modification Mapping with Broad Peak Calling

## Overview

This Camber app implements the nf-core/chipseq pipeline (v2.1.0) optimized for histone modification ChIP-seq analysis with broad peak calling. It is specifically designed for mapping diffuse chromatin marks like H3K27me3, H3K36me3, H3K9me3, and other histone modifications that spread across large genomic domains.

## Biological Use Case

**Target Audience**: Epigenetics researchers studying chromatin states, gene regulation, and epigenetic modifications.

**Research Questions Addressed**:
- Where are specific histone modifications located across the genome?
- Which genes are marked by activating (H3K4me3, H3K27ac) or repressive (H3K27me3, H3K9me3) marks?
- How do chromatin states change between conditions (e.g., disease vs healthy, treated vs untreated)?
- What are the broad chromatin domains associated with gene silencing or activation?

**Key Features**:
- **Broad peak calling**: Optimized for diffuse histone marks using MACS2 --broad flag
- **BWA-MEM alignment**: Robust and accurate read mapping
- **Comprehensive QC**: FRiP scores, cross-correlation, library complexity
- **Normalized tracks**: BigWig files for genome browser visualization
- **Peak annotation**: Gene assignments and genomic feature analysis
- **Replicate analysis**: Consensus peaks and reproducibility metrics

## Input Requirements

### Sample Sheet Format

CSV file with the following columns:

| Column | Description | Required |
|--------|-------------|----------|
| sample | Unique sample identifier | Yes |
| fastq_1 | Path to Read 1 FASTQ file (or single-end) | Yes |
| fastq_2 | Path to Read 2 FASTQ file (leave empty for SE) | No |
| replicate | Biological replicate number (1, 2, 3...) | Yes |
| antibody | Histone mark name (e.g., H3K27me3, H3K36me3) | Yes for ChIP |
| control | Name of matching input control sample | Yes for ChIP |
| control_replicate | Replicate number of control | Yes for ChIP |

**Example**:
```csv
sample,fastq_1,fastq_2,replicate,antibody,control,control_replicate
H3K27me3_WT_R1,WT_H3K27me3_R1.fastq.gz,,1,H3K27me3,WT_INPUT,1
H3K27me3_WT_R2,WT_H3K27me3_R2.fastq.gz,,2,H3K27me3,WT_INPUT,2
H3K27me3_KO_R1,KO_H3K27me3_R1.fastq.gz,,1,H3K27me3,KO_INPUT,1
H3K27me3_KO_R2,KO_H3K27me3_R2.fastq.gz,,2,H3K27me3,KO_INPUT,2
WT_INPUT,WT_Input_R1.fastq.gz,,1,,,
WT_INPUT,WT_Input_R2.fastq.gz,,2,,,
KO_INPUT,KO_Input_R1.fastq.gz,,1,,,
KO_INPUT,KO_Input_R2.fastq.gz,,2,,,
```

### Data Requirements

- **Sequencing type**: Single-end or paired-end Illumina sequencing
- **Read length**: 50-150 bp (75 bp typical)
- **Sequencing depth**: 20-40 million reads per sample for mammalian genomes
- **File format**: FASTQ.gz (gzip-compressed)
- **Controls**: Input (chromatin control) for each ChIP sample

## Parameters

### Required Parameters

- **input**: Sample sheet CSV file (path or stash:// URL)
- **output**: Output directory for results (path or stash:// URL)
- **genome**: Reference genome (e.g., GRCh38, GRCm39)
- **macs_gsize**: Effective genome size for MACS2 peak calling

### Hardcoded Parameters (Optimized for Histone Marks)

- **aligner**: BWA-MEM (robust and accurate)
- **broad_cutoff**: 0.1 (MACS2 broad peak threshold)
- **Peak calling mode**: Broad peaks (NOT narrow peaks)
- **Quality filters**: MAPQ ≥ 20, properly paired reads
- **Duplicate handling**: Marked and filtered to prevent PCR bias

### Genome Options

| Genome | Description | MACS gsize |
|--------|-------------|------------|
| GRCh38 | Human (latest) | 2.7e9 |
| GRCh37 | Human (legacy) | 2.7e9 |
| GRCm39 | Mouse (latest) | 1.87e9 |
| GRCm38 | Mouse (legacy) | 1.87e9 |
| TAIR10 | Arabidopsis | 1.2e8 |
| R64-1-1 | Yeast | 1.2e7 |

## Output Files

### Key Results

1. **Peaks** (`{sample}/macs2/{sample}_peaks.broadPeak`)
   - BED format with broad peak coordinates
   - Signal value, p-value, q-value for each peak

2. **Consensus Peaks** (`consensus_peaks/`)
   - Reproducible peaks across biological replicates
   - Boolean presence/absence matrix

3. **BigWig Tracks** (`{sample}/bigwig/{sample}.bigWig`)
   - Normalized genome-wide signal tracks
   - Load into IGV or UCSC Genome Browser

4. **Peak Annotations** (`{sample}/macs2/{sample}_peaks.annotatePeaks.txt`)
   - Gene assignments for each peak
   - Distance to TSS, genomic features

5. **MultiQC Report** (`multiqc/multiqc_report.html`)
   - Comprehensive quality control summary
   - FRiP scores, alignment statistics, library complexity

### Quality Metrics

- **FRiP score**: Fraction of Reads in Peaks (expect 1-5% for histone marks)
- **NSC**: Normalized Strand Cross-correlation (> 1.05)
- **RSC**: Relative Strand Cross-correlation (> 0.8)
- **Duplication rate**: Percent duplicate reads (< 20% ideal)
- **Alignment rate**: Percent of reads mapped (> 70%)

## Computational Resources

- **Recommended**: LARGE (64 CPUs, 360GB RAM)
- **Runtime**: ~2-4 hours for test data, 6-12 hours for full experiments
- **Storage**: ~5-10 GB per sample for outputs

## Testing

This app has been tested with:
- **Test data**: nf-core/test-datasets chipseq branch (SPT5 ChIP-seq from yeast)
- **Validation**: Successful broad peak calling with expected QC metrics

See `TESTING_LOG.md` for detailed testing results.

## Common Histone Marks

### Active Chromatin
- **H3K4me3**: Active promoters, TSS
- **H3K27ac**: Active enhancers, super-enhancers
- **H3K4me1**: Enhancers, primed regulatory regions
- **H3K36me3**: Active gene bodies, transcription elongation

### Repressive Chromatin
- **H3K27me3**: Polycomb repression, developmentally silenced genes
- **H3K9me3**: Constitutive heterochromatin, repetitive elements
- **H3K9me2**: Facultative heterochromatin, tissue-specific silencing

## Citation

If you use this app, please cite:

1. **nf-core/chipseq**: Ewels PA et al. (2020). Nature Biotechnology. [doi:10.1038/s41587-020-0439-x](https://doi.org/10.1038/s41587-020-0439-x)

2. **MACS2**: Zhang Y et al. (2008). Genome Biology. [doi:10.1186/gb-2008-9-9-r137](https://doi.org/10.1186/gb-2008-9-9-r137)

3. **BWA**: Li H and Durbin R (2009). Bioinformatics. [doi:10.1093/bioinformatics/btp324](https://doi.org/10.1093/bioinformatics/btp324)

## Troubleshooting

### Common Issues

1. **Low FRiP scores (< 1%)**
   - Check antibody quality and IP efficiency
   - Verify correct input controls are used
   - Consider different peak calling parameters

2. **No peaks called**
   - Insufficient sequencing depth
   - Poor ChIP enrichment
   - Check if samples and controls are correctly paired

3. **High duplication rates (> 30%)**
   - Low library complexity (may need more input DNA)
   - Over-amplification during library prep
   - Still usable but may reduce peak detection sensitivity

## Support

- **Pipeline documentation**: https://nf-co.re/chipseq/2.1.0/
- **Issues**: Report to Camber support or nf-core GitHub
- **Community**: nf-core Slack channel #chipseq

## Version Information

- **Pipeline**: nf-core/chipseq v2.1.0
- **App version**: 1.0.0
- **Last updated**: 2025-09-30