# Pipeline Status: nf-core/splicevariant

## CRITICAL FINDING

**There is NO nf-core/splicevariant pipeline.**

After extensive research of the nf-core pipeline collection (as of September 2025), there is no pipeline named "nf-core/splicevariant" in the official nf-core repository.

## Alternative: nf-core/rnasplice

The correct and actively maintained pipeline for splice variant analysis is:

**nf-core/rnasplice** - RNA-seq Alternative Splicing Analysis

### Pipeline Information
- **Pipeline Name**: nf-core/rnasplice
- **Latest Stable Version**: 1.0.4
- **Purpose**: Alternative splicing analysis of RNA sequencing data
- **Status**: Active and maintained
- **Repository**: https://github.com/nf-core/rnasplice
- **Documentation**: https://nf-co.re/rnasplice/

### Key Features
- Differential Exon Usage (DEU) with DEXSeq and edgeR
- Differential Transcript Usage (DTU) with DRIMSeq and DEXSeq
- Event-based Differential Splicing with rMATS and SUPPA2
- Multiple alignment options (STAR, Salmon)
- Comprehensive quality control with MultiQC

## Recommendation

**This implementation will use nf-core/rnasplice instead of the non-existent nf-core/splicevariant.**

The directory structure will remain as `/Users/david/git/prod_apps/nextflow/splicevariant/` as specified in the task requirements, but all documentation and implementation will correctly reference `nf-core/rnasplice`.

## Pipeline Verification Date
September 30, 2025

## Sources
- nf-core official pipeline list: https://nf-co.re/pipelines
- nf-core/rnasplice GitHub: https://github.com/nf-core/rnasplice
- nf-core/rnasplice documentation: https://nf-co.re/rnasplice/1.0.4/