# Pipeline: nf-core/smrnaseq

**Latest Version**: 2.4.0
**Last Updated**: 2025-09-30
**Overall Status**: 🔄 In Progress

## Summary

The nf-core/smrnaseq pipeline is a bioinformatics best-practice analysis pipeline for Small RNA-Seq data. It analyzes small RNA sequencing data to quantify miRNA expression, discover novel miRNAs, and perform comprehensive quality control. Small RNAs, particularly microRNAs (miRNAs), are crucial regulators of gene expression and play important roles in development, disease, and cellular function.

**Biological Significance**: The 2024 Nobel Prize in Physiology or Medicine was awarded for the discovery of miRNAs and their role in post-transcriptional gene regulation, highlighting the critical importance of this field.

## Key Features

- Quality control and adapter trimming of small RNA reads
- UMI deduplication (optional)
- miRNA quantification using multiple methods (EdgeR, Mirtop)
- Contamination filtering
- Novel miRNA discovery
- Comprehensive quality reporting with MultiQC
- Support for multiple library preparation protocols (Illumina, QIAseq, NextTFlex, CATS)

## Use Cases Identified

1. **miRNA Expression Profiling** - [Status: 📝 Planned]
   - Focus: Standard miRNA expression quantification
   - Target: Cancer research, developmental biology

2. **Biomarker Discovery** - [Status: 📝 Planned]
   - Focus: Circulating miRNAs in liquid biopsies
   - Target: Clinical diagnostics, disease monitoring

3. **Novel miRNA Discovery** - [Status: 📝 Planned]
   - Focus: Identify previously unknown miRNAs
   - Target: Non-model organisms, disease-specific miRNAs

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [ ] App 1: miRNA Expression Profiling - [Status: 📝 Planned]
- [ ] App 2: Biomarker Discovery (Circulating miRNA) - [Status: 📝 Planned]
- [ ] App 3: Novel miRNA Discovery - [Status: 📝 Planned]

## Technical Details

**Input Requirements**:
- Single-end FASTQ files (small RNA-seq is typically single-end)
- Samplesheet CSV format: `sample,fastq_1`

**Key Parameters**:
- `--genome`: Reference genome (e.g., GRCh38, GRCm39)
- `--mirtrace_species`: Species code for miRTrace QC (e.g., 'hsa' for human, 'mmu' for mouse)
- `--protocol`: Library preparation protocol (auto-detected or specified)

**Supported Library Protocols**:
- Illumina (default)
- QIAseq
- NextTFlex
- CATS
- Custom (manual configuration)

**Resource Requirements**:
- SMALL to MEDIUM nodes recommended
- Test data runs in ~10-20 minutes on XSMALL

## Test Data

nf-core provides test data:
- **Samplesheet**: https://github.com/nf-core/test-datasets/raw/smrnaseq/samplesheet/v2.0/samplesheet.csv
- **Species**: Human (hsa)
- **Samples**: 8 samples (3 clones + controls with replicates)
- **Data size**: Small test dataset optimized for quick validation

## Issues Encountered

None yet - pipeline research phase complete.

## Success Metrics

- Target: 3/3 apps working
- Current: 0/3 apps implemented

## Next Steps

1. Implement miRNA Expression Profiling app (most common use case)
2. Test with nf-core test data
3. Implement Biomarker Discovery app with protocol-specific configurations
4. Implement Novel miRNA Discovery app

## Notes

- Small RNA-seq is typically single-end (not paired-end)
- miRTrace QC requires species code - important to expose this parameter
- Protocol detection is automatic but can be manually specified
- Multiple quantification tools available (will hardcode best practices)
