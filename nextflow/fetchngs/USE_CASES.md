# nf-core/fetchngs Use Cases

**Pipeline**: fetchngs v1.12.0
**Last Updated**: 2025-09-30

## Overview

The nf-core/fetchngs pipeline downloads sequencing data and metadata from public databases (SRA, ENA, DDBJ, GEO) and prepares it for downstream analysis with other nf-core pipelines. This is a utility pipeline focused on data retrieval rather than analysis.

---

## Use Case 1: SRA Download for RNA-seq Analysis

**Priority**: P0 (Highest)

**Biological Question**: How do I download publicly available RNA-seq data from NCBI SRA or GEO for reanalysis?

**Target Audience**:
- Researchers reproducing published RNA-seq studies
- Scientists performing meta-analyses across multiple datasets
- Biologists validating methods on reference datasets

**Typical Experimental Design**:
- Input: List of SRA/GEO accession IDs (e.g., SRR11605097, GSM4432381)
- Scale: 2-100 samples from published studies
- Output: Downloaded FastQ files + samplesheet ready for nf-core/rnaseq

**Key Parameters**:
- **Hardcoded**:
  - Download method: FTP (reliable and widely available)
  - nf-core pipeline format: rnaseq
  - Force sra-tools: false (prefer FTP)
  - Skip FastQ download: false (we want the files)
- **Exposed**:
  - Input file (list of accession IDs)
  - Output directory
  - nf-core pipeline type (rnaseq, atacseq, etc.)

**Tools**:
- ENA API for metadata retrieval
- FTP download for FastQ files
- MD5 checksum verification

**Expected Outputs**:
- Downloaded FastQ files (paired-end or single-end)
- `samplesheet.csv` formatted for nf-core/rnaseq
- `id_mappings.csv` with metadata
- `multiqc_config.yml` for downstream QC

**Resource Requirements**: XSMALL (minimal computation, mainly network I/O)

**Example Input File** (`ids.csv`):
```csv
SRR11605097
SRR11605098
GSM4432381
```

**Priority Justification**: Most common use case - researchers regularly need to download published data for validation, reanalysis, or meta-analysis studies.

---

## Use Case 2: ENA Bulk Data Download

**Priority**: P1

**Biological Question**: How do I efficiently download large cohorts of sequencing data from the European Nucleotide Archive?

**Target Audience**:
- Researchers conducting large-scale meta-analyses
- Bioinformaticians building reference datasets
- Data scientists training machine learning models on public data

**Typical Experimental Design**:
- Input: Large list of ENA accession IDs (50-500 samples)
- Scale: Cohort-level downloads (e.g., entire studies)
- Output: Downloaded FastQ files organized by study/sample

**Key Parameters**:
- **Hardcoded**:
  - Download method: Aspera (faster for bulk downloads)
  - Force FTP fallback: true (in case Aspera fails)
  - Parallel downloads: enabled
- **Exposed**:
  - Input file (ENA accession list)
  - Output directory
  - Download method (FTP vs Aspera)

**Tools**:
- ENA API for metadata
- Aspera for high-speed downloads
- FTP fallback for reliability

**Expected Outputs**:
- Downloaded FastQ files
- Study-level organization
- Comprehensive metadata file

**Resource Requirements**: XSMALL to SMALL (network-bound, but may need more memory for large cohorts)

**Priority Justification**: Secondary use case for researchers working with larger datasets requiring optimized download strategies.

---

## Use Case Prioritization

| Use Case | Priority | Complexity | Test Data | Implementation Order |
|----------|----------|------------|-----------|---------------------|
| SRA Download for RNA-seq | P0 | Low | ✅ Available | 1 |
| ENA Bulk Data Download | P1 | Medium | ✅ Available | 2 |

---

## Implementation Notes

### Use Case 1 (SRA Download)
- **Test Data**: Use nf-core/test-datasets fetchngs branch
- **Expected Runtime**: 5-10 minutes for test data (small files)
- **Challenges**:
  - Network reliability (handle download failures gracefully)
  - Stash integration (ensure files are properly written to output)
  - FTP vs Aspera selection

### Use Case 2 (ENA Bulk)
- **Test Data**: Same as Use Case 1 but with Aspera download method
- **Expected Runtime**: Similar to Use Case 1 for test data
- **Challenges**:
  - Aspera installation and configuration
  - Parallel download limits
  - Large file handling

---

## Common Parameters Across Use Cases

### Always Hardcoded
- `--md5sum`: true (verify downloads)
- `--skip_fastq_download`: false (we want the files)

### Always Exposed
- `--input`: Path to ID list file
- `--outdir`: Output directory for results
- `--nf_core_pipeline`: Which nf-core pipeline to format samplesheet for

### Download Method Selection
- **FTP**: Reliable, works everywhere, moderate speed
- **Aspera**: Very fast, requires Aspera Connect, may need configuration
- **SRA Tools**: For dbGaP or restricted access data

---

## Biological Research Applications

**Perfect for Research in**:
- Reproducibility studies (validating published findings)
- Meta-analyses (combining data from multiple studies)
- Method development (testing on reference datasets)
- Comparative genomics (downloading samples across species)
- Time-series analyses (downloading historical datasets)
- Reanalysis with updated methods (applying new algorithms to old data)

**Typical Research Workflows**:
1. **Literature Review → Data Download**: Find relevant studies, extract SRA IDs, download data
2. **Meta-Analysis Pipeline**: Download multiple studies → Combine → Unified analysis
3. **Method Validation**: Download benchmark datasets → Test new tools → Compare results
4. **Reanalysis Studies**: Download original data → Apply updated pipelines → New insights

---

## Success Criteria

**App is working when**:
- ✅ Successfully downloads FastQ files from test accessions
- ✅ Generates valid samplesheet for downstream pipeline
- ✅ MD5 checksums verified
- ✅ Output files properly written to stash
- ✅ Job completes with COMPLETED status

**Common Failure Modes to Test**:
- Network timeouts during download
- Invalid accession IDs
- Mixed single-end and paired-end data
- Large file handling
- Stash write permissions

---

## Pipeline-Specific Considerations

### Lightweight Nature
- No heavy computation (just downloads)
- Network-bound rather than CPU/memory-bound
- XSMALL nodes should be sufficient

### Integration Points
- Output must work with nf-core/rnaseq, atacseq, etc.
- Samplesheet format must match downstream pipeline requirements
- Metadata preservation for sample tracking

### Testing Strategy
- Start with small test accessions (fast iteration)
- Verify samplesheet format compatibility
- Test with both SRA and GEO accession types
- Ensure proper error handling for failed downloads