# RNA Isoform Detection from Nanopore cDNA Sequencing

## Overview

This Camber app implements the nf-core/nanoseq pipeline for full-length RNA transcript isoform detection using Oxford Nanopore cDNA sequencing data. It uses the Bambu quantification method to identify alternative splicing patterns and quantify isoform expression.

## Biological Context

Oxford Nanopore long-read cDNA sequencing enables:
- **Full-length transcript sequencing**: Read entire transcripts from 5' to 3' end
- **Isoform resolution**: Directly observe which exons are spliced together
- **Alternative splicing detection**: Identify tissue-specific and condition-specific splice variants
- **Novel isoform discovery**: Detect previously unannotated transcript structures
- **Accurate quantification**: Count complete isoforms without computational assembly

## Target Users

- Researchers studying alternative splicing and RNA complexity
- Transcriptomics scientists investigating isoform diversity
- Cancer biologists examining fusion transcripts
- Developmental biologists studying tissue-specific isoforms
- Plant biologists analyzing complex transcriptomes

## Pipeline Configuration

### Hardcoded Parameters
- **Protocol**: cDNA (optimized for cDNA sequencing libraries)
- **Skip Demultiplexing**: true (assumes pre-demultiplexed FASTQ files)
- **Quantification Method**: Bambu (context-aware isoform discovery and quantification)
- **Pipeline Version**: 3.1.0 (nf-core/nanoseq)
- **Profile**: singularity (containerized execution)

### User-Configurable Parameters
- **Sample Sheet**: CSV file with sample metadata and file paths
- **Output Directory**: Location for analysis results

## Input Requirements

### Sample Sheet Format

CSV file with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| group | Sample group/condition identifier | WT, Control, Treated |
| replicate | Biological replicate number | 1, 2, 3 |
| barcode | Barcode number (leave empty for demultiplexed data) | |
| input_file | Path or URL to FASTQ.gz file | s3://bucket/sample1.fastq.gz |
| fasta | Reference genome FASTA file | genome.fa |
| gtf | Gene annotation GTF file | genes.gtf |

### Example Sample Sheet

```csv
group,replicate,barcode,input_file,fasta,gtf
WT,1,,sample1.fastq.gz,genome.fa,genes.gtf
WT,2,,sample2.fastq.gz,genome.fa,genes.gtf
Treated,1,,sample3.fastq.gz,genome.fa,genes.gtf
Treated,2,,sample4.fastq.gz,genome.fa,genes.gtf
```

## Output Structure

The pipeline produces comprehensive results including:

### Quantification Results
- **Isoform Expression Matrix**: Transcript-level read counts
- **Gene Expression Matrix**: Gene-level aggregated counts
- **Novel Isoforms**: GTF file with newly discovered transcripts
- **Extended Annotations**: Updated GTF with all detected isoforms

### Alignment Files
- **BAM Files**: Aligned reads for each sample
- **BAM Indices**: Index files for genome browsers

### Quality Control
- **NanoPlot Reports**: Read quality statistics and distributions
- **PycoQC Reports**: Comprehensive sequencing QC metrics
- **MultiQC Report**: Integrated QC summary across all samples

### Analysis Reports
- **Pipeline Report**: Nextflow execution summary
- **Timeline**: Process execution timeline
- **DAG**: Directed acyclic graph of workflow

## Resource Requirements

### System Sizes

- **Small** (1-4 samples): MEDIUM node (recommended for pilot studies)
- **Medium** (5-12 samples): LARGE node (recommended for typical experiments)
- **Large** (13+ samples): XLARGE node with 2 nodes (for large cohorts)

### Typical Runtime
- Small dataset (4 samples, 1M reads each): ~2-4 hours
- Medium dataset (10 samples, 5M reads each): ~6-12 hours
- Large dataset (20 samples, 10M reads each): ~12-24 hours

## Test Data

A test sample sheet (`samplesheet.csv`) is included in this directory using publicly available test data from nf-core/test-datasets.

## Scientific Applications

### Alternative Splicing Studies
- Identify tissue-specific splice variants
- Detect disease-associated isoform switching
- Map complete exon-intron structures

### Isoform Diversity Analysis
- Catalog all expressed isoforms per gene
- Quantify relative isoform abundances
- Compare isoform usage across conditions

### Transcript Structure Discovery
- Identify novel exons and splice junctions
- Detect retained introns
- Discover alternative TSS and polyA sites

## Pipeline Components

1. **Quality Control**: NanoPlot, PycoQC for read quality assessment
2. **Alignment**: Minimap2 for spliced long-read alignment
3. **Transcript Reconstruction**: Bambu for context-aware isoform assembly
4. **Quantification**: Bambu integrated read counting
5. **Reporting**: MultiQC aggregated quality metrics

## Citations

If using this pipeline, please cite:

- **nf-core/nanoseq**: Ewels PA et al. (2020). Nat Biotechnol. DOI: 10.1038/s41587-020-0439-x
- **Bambu**: Chen Y et al. (2023). Nat Methods. DOI: 10.1038/s41592-023-01835-0
- **Minimap2**: Li H. (2018). Bioinformatics. DOI: 10.1093/bioinformatics/bty191
- **Nextflow**: Di Tommaso P et al. (2017). Nat Biotechnol. DOI: 10.1038/nbt.3820

## Technical Details

- **Container System**: Singularity (ensures reproducibility)
- **Workflow Engine**: Nextflow (portable and scalable)
- **Pipeline Family**: nf-core (community-curated best practices)
- **Version**: 3.1.0 (stable release)

## Support

For pipeline-specific questions, see:
- nf-core/nanoseq documentation: https://nf-co.re/nanoseq/3.1.0
- nf-core Slack: https://nfcore.slack.com

For Camber platform support:
- Camber Documentation: https://docs.camber.cloud