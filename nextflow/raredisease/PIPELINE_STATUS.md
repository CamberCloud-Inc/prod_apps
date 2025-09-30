# nf-core/raredisease Pipeline Status

## Overview

**Pipeline**: nf-core/raredisease
**Latest Version**: 2.6.0
**Purpose**: Comprehensive bioinformatics analysis pipeline for calling and scoring variants from WGS/WES data of rare disease patients
**Status**: Under Development

## Pipeline Description

The nf-core/raredisease pipeline is a best-practice workflow for analyzing genomic data from patients with rare genetic diseases. Originally developed as an extension of the workflow used in the Stockholm region (analyzing ~3000 WGS and ~1000 WES samples annually with ~40% diagnostic yield), this pipeline aims to become a national standard for rare disease genomic diagnostics.

## Key Capabilities

### Supported Analysis Types
- **Whole Genome Sequencing (WGS)**: Comprehensive analysis of entire genome
- **Whole Exome Sequencing (WES)**: Targeted analysis of protein-coding regions
- **Mitochondrial Analysis (MITO)**: Specialized workflow for mitochondrial variants

### Variant Detection
- **SNVs and Small Indels**: Single nucleotide variants and insertions/deletions
- **Structural Variants (SVs)**: Large genomic rearrangements
- **Copy Number Variants (CNVs)**: Duplications and deletions
- **Repeat Expansions**: Detection of pathogenic repeat sequences
- **Mobile Elements**: Insertion of transposable elements

### Core Features
- Alignment with BWA-mem2 or Sentieon DNAseq
- Variant calling with DeepVariant (default), GATK HaplotypeCaller, or Sentieon
- Structural variant calling with Manta
- CNV detection with GATK and Tiddit
- Comprehensive annotation with VEP and CADD scoring
- Variant ranking and prioritization
- Quality control metrics with FastQC, Mosdepth, and MultiQC
- Family-based analysis support (trios, pedigrees)

## Clinical Application

This pipeline is designed for **clinical diagnostic laboratories** analyzing rare disease cases:

- **High Diagnostic Yield**: Proven 40% diagnostic rate in production use
- **Healthcare Integration**: Used in clinical settings for patient diagnosis
- **Comprehensive Reporting**: Generates ranked variant lists for clinical interpretation
- **Family Analysis**: Supports inheritance pattern analysis with parental samples

## Input Requirements

### Samplesheet Format (CSV)
```csv
sample,lane,fastq_1,fastq_2,sex,phenotype,paternal_id,maternal_id,case_id
patient01,L001,reads_R1.fastq.gz,reads_R2.fastq.gz,2,2,,,case001
father01,L001,father_R1.fastq.gz,father_R2.fastq.gz,1,1,,,case001
mother01,L001,mother_R1.fastq.gz,mother_R2.fastq.gz,2,1,,,case001
```

**Column Definitions**:
- `sample`: Unique sample identifier
- `lane`: Sequencing lane (typically L001, L002, etc.)
- `fastq_1`: Path to Read 1 FASTQ file
- `fastq_2`: Path to Read 2 FASTQ file
- `sex`: 0=unknown, 1=male, 2=female
- `phenotype`: 0=missing, 1=unaffected, 2=affected
- `paternal_id`: Father's sample ID (leave empty if not applicable)
- `maternal_id`: Mother's sample ID (leave empty if not applicable)
- `case_id`: Identifier grouping related samples (family)

### Data Requirements
- Paired-end Illumina sequencing data (FASTQ format)
- WGS: Minimum 30x coverage recommended
- WES: Minimum 100x coverage recommended
- Reference genome: GRCh37 or GRCh38

## Reference Genomes
- Human GRCh38 (hg38) - Recommended for new studies
- Human GRCh37 (hg19) - For compatibility with legacy data

## Tools and Algorithms

### Alignment
- BWA-mem2 (default)
- Sentieon DNAseq (optional, commercial license required)

### Variant Calling
- DeepVariant (default, AI-based)
- GATK HaplotypeCaller (standard)
- Sentieon DNAscope (optional, commercial)
- Manta (structural variants)
- GATK (CNVs)
- Tiddit (SVs and CNVs)
- ExpansionHunter (repeat expansions)
- RETROSEQ (mobile elements)

### Annotation
- VEP (Variant Effect Predictor)
- CADD (pathogenicity scoring)
- GENMOD (inheritance pattern annotation)

### Quality Control
- FastQC (read quality)
- Mosdepth (coverage analysis)
- Picard Metrics (alignment statistics)
- MultiQC (comprehensive QC report)

## Implementation Status

### Completed
- ✅ Pipeline research and use case identification
- ✅ Documentation structure created

### In Progress
- 🔄 App implementation for WGS analysis
- 🔄 Testing with nf-core test datasets

### Planned
- ⏳ WES-specific app implementation
- ⏳ Mitochondrial analysis app
- ⏳ Trio/Family analysis app
- ⏳ Validation with real patient data

## Use Case Priority

Based on research and clinical utility:

1. **Priority 1 (Implementing)**: WGS Rare Disease Analysis - Standard single sample or family analysis
2. **Priority 2**: WES Targeted Analysis - Exome-focused rare disease diagnosis
3. **Priority 3**: Mitochondrial Disease Analysis - Specialized mito variant detection
4. **Priority 4**: Trio Analysis - Parent-child inheritance pattern analysis

## Expected Outputs

### Variant Calls
- VCF files with SNVs, indels, SVs, and CNVs
- Annotated variants with gene names, functional predictions
- CADD scores for pathogenicity prediction

### Clinical Reports
- Ranked variant lists prioritized by clinical relevance
- Inheritance pattern annotations
- Coverage and quality metrics

### Quality Control
- MultiQC HTML report with comprehensive statistics
- BAM alignment files
- Per-sample metrics (coverage depth, mapping quality)

## Resources and Documentation

- **Official Documentation**: https://nf-co.re/raredisease/2.6.0/
- **GitHub Repository**: https://github.com/nf-core/raredisease
- **Publication**: Pettersson et al. (referenced in pipeline docs)
- **nf-core Framework**: Ewels et al., Nature Biotechnology 2020

## Notes

- This pipeline requires substantial computational resources (recommended: LARGE or XLARGE node sizes)
- Analysis time varies: WGS ~12-24 hours, WES ~4-8 hours per sample
- Family-based analysis may require additional time for joint calling and inheritance analysis
- Commercial Sentieon tools offer faster processing but require licensing

## Version History

- **v2.6.0** (Latest): Current stable release
- Pipeline is actively maintained by nf-core community
- Regular updates include new tools and improved algorithms

---

**Last Updated**: 2025-09-30
**Maintainer**: david40962
**Status**: Active Development