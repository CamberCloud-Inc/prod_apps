# fetchngs: SRA Download for RNA-seq

## Use Case Description

Download raw sequencing data from public repositories (SRA, ENA, DDBJ, GEO) and prepare it for downstream analysis. This app automatically fetches FastQ files and generates samplesheets compatible with nf-core pipelines.

## Target Audience

- Researchers reproducing published RNA-seq studies
- Scientists performing meta-analyses across multiple datasets
- Biologists validating methods on reference datasets
- Anyone needing to download public sequencing data

## Input Requirements

### Accession ID List (`input`)

A simple CSV file with one accession ID per line. No header required.

**Supported ID Types**:
- SRA: `SRR11605097`
- ENA: `ERR4007730`
- DDBJ: `DRR171822`
- GEO: `GSM4432381` or `GSE214215`

**Example File** (`test_ids.csv`):
```csv
SRR11605097
SRR11605098
GSM4432381
```

### Output Directory (`output`)

Stash path where results will be saved (e.g., `stash://username/fetchngs-results/`).

### Pipeline Format (`pipeline_format`)

Format the output samplesheet for a specific nf-core pipeline:
- `rnaseq` - RNA sequencing (most common)
- `atacseq` - ATAC-seq chromatin accessibility
- `taxprofiler` - Metagenomic profiling
- `viralrecon` - Viral genome reconstruction
- `none` - Generic download without pipeline formatting

## Expected Outputs

### Downloaded Data
- `fastq/` - Directory containing downloaded FastQ files
  - Single-end: `{sample}_R1.fastq.gz`
  - Paired-end: `{sample}_R1.fastq.gz`, `{sample}_R2.fastq.gz`
- `md5/` - MD5 checksum files for verification

### Analysis-Ready Files
- `samplesheet/samplesheet.csv` - Formatted for downstream pipeline
- `metadata/id_mappings.csv` - Accession IDs mapped to metadata
- `multiqc_config.yml` - Configuration for MultiQC reports

### Metadata
- Sample information (organism, tissue, library prep)
- Sequencing details (platform, read length, layout)
- Study information (title, publication, accession)

## Resource Requirements

| Dataset Size | Node Size | Specs | Est. Runtime |
|--------------|-----------|-------|--------------|
| Test data (2 accessions) | XSMALL | 4 CPU, 15GB RAM | 5-10 min |
| Small (1-10 accessions) | XSMALL | 4 CPU, 15GB RAM | 10-30 min |
| Medium (10-50 accessions) | XSMALL | 4 CPU, 15GB RAM | 30-120 min |
| Large (50+ accessions) | SMALL | 8 CPU, 30GB RAM | 2-6 hours |

**Note**: Runtime depends primarily on network speed and file sizes, not compute resources.

## Testing Instructions

### Test with nf-core Test Data

```bash
# Navigate to app directory
cd /Users/david/git/prod_apps/nextflow/fetchngs/sra-download-rnaseq

# Upload test file to stash
camber stash cp test_ids.csv stash://username/fetchngs-test/

# Create the app
camber app create --file app.json

# Run test
camber app run fetchngs-sra-download \
  --input input="stash://username/fetchngs-test/test_ids.csv" \
  --input output="stash://username/fetchngs-test/results-attempt-1" \
  --input pipeline_format="rnaseq"

# Monitor job (save job ID from above)
camber job get <job_id>

# Get logs when complete
camber job logs <job_id> > attempt-1-logs.txt
```

### Verify Results

Check that the following files exist in output directory:
1. `fastq/` directory with downloaded FastQ files
2. `samplesheet/samplesheet.csv` with correct format for rnaseq
3. `metadata/id_mappings.csv` with sample metadata
4. MD5 checksums match for all downloaded files

## Known Limitations

- Download speed depends on network connection and server availability
- Very large files (>50GB) may require extended timeouts
- GEO accessions are resolved to underlying SRA accessions
- Some restricted-access data cannot be downloaded without credentials

## Downstream Analysis

The generated `samplesheet.csv` can be directly used with:

```bash
# RNA-seq analysis
camber app run rnaseq-standard \
  --input input="stash://username/fetchngs-test/results/samplesheet/samplesheet.csv" \
  --input genome="GRCh38"

# Or other nf-core pipelines
```

## Troubleshooting

### Issue: "Failed to download file"
- **Cause**: Network timeout or server unavailable
- **Solution**: Retry the job; FTP servers occasionally have temporary issues

### Issue: "Invalid accession ID"
- **Cause**: Typo in ID or accession doesn't exist
- **Solution**: Verify IDs on NCBI SRA or ENA website

### Issue: "Mixed single-end and paired-end"
- **Cause**: Accessions have different sequencing layouts
- **Solution**: This is expected; pipeline handles both types automatically

## Test Data Information

Test IDs from nf-core/test-datasets:
- `SRR9984183` - Small bacterial RNA-seq sample
- `SRR13191702` - Small viral RNA-seq sample

These are minimal test datasets designed for fast testing (~5-10 minutes).

## Version Information

- **Pipeline**: nf-core/fetchngs v1.12.0
- **Test Profile**: Uses nf-core test configuration
- **Last Updated**: 2025-09-30