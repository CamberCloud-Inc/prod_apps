# SARS-CoV-2 Surveillance Pipeline

A Camber Cloud application implementing the nf-core/viralrecon pipeline for SARS-CoV-2 genomic surveillance in public health laboratories.

## Overview

This application reconstructs SARS-CoV-2 genomes from Illumina amplicon sequencing data, identifies viral variants, and classifies lineages for epidemiological tracking. It is specifically configured for public health surveillance workflows using ARTIC primer schemes.

## Use Case

**Target Users:** Public health laboratories, epidemiologists, genomic surveillance teams

**Applications:**
- Identify SARS-CoV-2 variants of concern (VOCs) and variants of interest (VOIs)
- Track viral transmission chains and outbreak clusters
- Monitor viral evolution in populations
- Generate consensus sequences for GISAID/GenBank submission
- Support contact tracing with genomic data

## Pipeline Features

### Hardcoded Settings (Optimized for Surveillance)

- **Reference Genome:** SARS-CoV-2 MN908947.3 (Wuhan-Hu-1)
- **Platform:** Illumina sequencing
- **Protocol:** Amplicon-based (ARTIC primers)
- **Primer Scheme:** ARTIC nCoV-2019
- **Consensus Caller:** iVar
- **Variant Caller:** iVar with BCFtools

### Configurable Parameters

1. **Samplesheet Location** (Required)
   - CSV file with columns: `sample,fastq_1,fastq_2`
   - Supports local paths or remote URLs
   - Example provided using nf-core test data

2. **ARTIC Primer Version** (Required)
   - V1: Original scheme
   - V2: Updated scheme
   - V3: Most commonly used (default)
   - V4/4.1: Improved for Delta/Omicron variants
   - V5.3.2: Latest scheme for current Omicron sublineages

3. **Output Directory** (Optional)
   - Default: Job outputs directory
   - Results include consensus sequences, variants, lineages, and QC reports

### Variant Calling Parameters

- **Minimum variant frequency:** 25% (intra-host variants)
- **Minimum coverage depth:** 10x
- **Minimum variant quality:** Q20
- **Primer trimming:** Enabled to remove primer artifacts
- **Minimum read length:** 20bp after trimming
- **Minimum mapped reads:** 1,000 for consensus calling

## Input Requirements

### Samplesheet Format

CSV file with the following structure:

```csv
sample,fastq_1,fastq_2
SAMPLE01,/path/to/sample01_R1.fastq.gz,/path/to/sample01_R2.fastq.gz
SAMPLE02,/path/to/sample02_R1.fastq.gz,/path/to/sample02_R2.fastq.gz
```

- **sample:** Unique sample identifier
- **fastq_1:** Path or URL to forward reads (R1)
- **fastq_2:** Path or URL to reverse reads (R2)

### Sequencing Requirements

- **Platform:** Illumina (MiSeq, NextSeq, NovaSeq)
- **Library Prep:** ARTIC PCR amplicon
- **Read Type:** Paired-end
- **Read Length:** 75-300bp
- **Coverage:** Recommended ≥100x mean depth
- **Quality:** Q30 ≥ 80%

## Pipeline Workflow

1. **Quality Control** (FastQC)
   - Assess raw read quality
   - Identify sequencing issues

2. **Read Trimming** (fastp)
   - Remove adapter sequences
   - Quality filtering
   - Length filtering

3. **Read Alignment** (Bowtie2)
   - Map reads to MN908947.3 reference
   - Generate BAM files

4. **Primer Trimming** (iVar)
   - Remove ARTIC primer sequences
   - Soft-clip primer regions

5. **Variant Calling** (iVar)
   - Identify SNVs and indels
   - Calculate variant frequencies
   - Generate VCF files

6. **Consensus Generation** (iVar)
   - Create consensus sequences
   - Mask low-coverage regions
   - Output FASTA files

7. **Lineage Analysis**
   - **Pangolin:** Assign Pango lineages (e.g., BA.5.2.1)
   - **Nextclade:** Classify clades and identify mutations

8. **Quality Reporting** (MultiQC)
   - Aggregate all QC metrics
   - Coverage statistics
   - Lineage summary

## Output Files

```
results/
├── fastqc/                      # Raw read QC reports
├── fastp/                       # Trimmed read QC
├── variants/
│   ├── ivar/
│   │   ├── *.vcf.gz            # Variant calls per sample
│   │   └── *.tsv               # Variant annotations
│   └── bowtie2/
│       └── *.sorted.bam        # Aligned and sorted reads
├── consensus/
│   └── *.consensus.fa          # Consensus sequences (FASTA)
├── pangolin/
│   └── *.pangolin.csv          # Lineage assignments
├── nextclade/
│   ├── *.nextclade.json        # Detailed clade information
│   └── *.nextclade.tsv         # Clade assignments table
└── multiqc/
    └── multiqc_report.html     # Comprehensive QC report
```

### Key Output Files

- **Consensus Sequences:** `consensus/*.consensus.fa` - Ready for GISAID/GenBank submission
- **Variant Calls:** `variants/ivar/*.vcf.gz` - All detected variants with frequencies
- **Lineage Assignments:** `pangolin/*.pangolin.csv` - Pango lineage classifications
- **Clade Classifications:** `nextclade/*.nextclade.tsv` - Nextclade clade assignments
- **QC Report:** `multiqc/multiqc_report.html` - Interactive quality control dashboard

## Running the Pipeline

### Quick Start

1. Prepare your samplesheet CSV file with sample information
2. Upload samplesheet to Camber Stash
3. Launch the application from Camber Cloud interface
4. Select ARTIC primer version (V3 recommended for most samples)
5. Specify output directory (optional)
6. Submit job

### Example Command (Manual Execution)

```bash
nextflow run nf-core/viralrecon \
  -r 2.6.0 \
  --input samplesheet.csv \
  --outdir results \
  --platform illumina \
  --protocol amplicon \
  --genome 'MN908947.3' \
  --primer_set artic \
  --primer_set_version 3 \
  --skip_assembly \
  --ivar_trim_noprimer \
  --consensus_caller ivar \
  --max_memory 128.GB \
  --max_cpus 16 \
  -profile docker
```

## Test Data

The application includes test data from the nf-core/test-datasets repository:

- **Sample 1:** ARTIC amplicon test data (SAMPLE01_PE)
- **Sample 2:** ARTIC amplicon test data (SAMPLE02_PE)
- **Reference:** SARS-CoV-2 MN908947.3
- **Primers:** ARTIC V3

Test data URL: https://github.com/nf-core/test-datasets/tree/viralrecon

## Resource Requirements

- **Node Size:** LARGE (default)
- **CPUs:** 16 cores
- **Memory:** 128 GB
- **Storage:** ~50 GB per batch (depends on sample count)
- **Runtime:** 1-4 hours (typical batch of 96 samples)

## Interpreting Results

### Consensus Quality Metrics

- **Coverage Depth:** Average ≥100x for high-quality consensus
- **Genome Completeness:** Aim for ≥95% coverage
- **N-content:** Lower is better (<5% recommended for database submission)

### Variant Interpretation

- **High-confidence variants:** Frequency ≥75%, depth ≥20x
- **Intra-host variants:** Frequency 25-75% (mixed infections or within-host evolution)
- **Low-frequency variants:** <25% (may represent sequencing errors or minor populations)

### Lineage Assignment

- **Pango lineages:** Most detailed nomenclature (e.g., BA.5.2.1)
- **Nextclade clades:** Broader classifications (e.g., 22B Omicron)
- **VOC/VOI status:** Check WHO classifications for public health significance

## Troubleshooting

### Low Coverage

**Symptoms:** High N-content in consensus, gaps in genome
**Solutions:**
- Check input FASTQ quality (Q30 score)
- Verify PCR amplification success
- Ensure correct primer version matches lab protocol
- Increase sequencing depth

### Failed Lineage Assignment

**Symptoms:** "Unassigned" or "None" lineage
**Solutions:**
- Check consensus quality (needs ≥50% genome coverage)
- Verify reference genome (must be MN908947.3)
- Update Pangolin/Nextclade datasets (done automatically)

### Primer Mismatch Warnings

**Symptoms:** Low primer trimming rates, high primer sequences in reads
**Solutions:**
- Verify primer version selection matches lab protocol
- Check for primer scheme updates from ARTIC Network
- Consider using newer primer version for recent variants

## References

### Pipeline Documentation

- **nf-core/viralrecon:** https://nf-co.re/viralrecon
- **Pipeline GitHub:** https://github.com/nf-core/viralrecon
- **nf-core:** https://nf-co.re/

### ARTIC Network

- **ARTIC Network:** https://artic.network/
- **Primer Schemes:** https://github.com/artic-network/primer-schemes
- **SARS-CoV-2 Primers:** https://artic.network/ncov-2019

### Lineage Classification

- **Pangolin:** https://cov-lineages.org/
- **Nextclade:** https://clades.nextstrain.org/
- **GISAID:** https://www.gisaid.org/

### Publications

- Quick J, et al. (2017) "Multiplex PCR method for MinION and Illumina sequencing of Zika and other viral genomes directly from clinical samples." *Nature Protocols* 12:1261-1276.
- Ewels PA, et al. (2020) "The nf-core framework for community-curated bioinformatics pipelines." *Nature Biotechnology* 38:276-278.

## Support

For pipeline issues or questions:
- nf-core Slack: https://nf-co.re/join
- GitHub Issues: https://github.com/nf-core/viralrecon/issues
- Camber Cloud Support: support@cambercloud.com

## Version Information

- **Pipeline:** nf-core/viralrecon v2.6.0
- **Reference Genome:** SARS-CoV-2 MN908947.3
- **Default Primer Scheme:** ARTIC V3
- **Consensus Caller:** iVar
- **Lineage Tools:** Pangolin + Nextclade

## License

This application uses nf-core/viralrecon which is released under the MIT License.