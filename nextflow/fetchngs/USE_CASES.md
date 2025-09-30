# nf-core/fetchngs Use Cases

## Overview

The fetchngs pipeline is designed to download publicly available sequencing data from databases like SRA, ENA, DDBJ, and GEO. This document identifies specific biological use cases where researchers need to access public sequencing data.

---

## Use Case 1: Download RNA-seq Data for Reanalysis (PRIORITY: P0)

### Biological Question
How can researchers access published RNA-seq datasets to validate findings, perform meta-analyses, or apply new analysis methods?

### Target Audience
- Researchers validating published results
- Scientists performing meta-analyses across multiple studies
- Bioinformaticians developing or benchmarking new tools
- Students learning RNA-seq analysis with real data

### Typical Experimental Design
- Published RNA-seq studies from SRA/GEO
- Single or multiple samples from the same study
- Various organisms and experimental conditions
- Data quality varies by original study

### Key Parameters

**Hardcoded:**
- Download method: FTP (reliable and fast)
- nf_core_pipeline: rnaseq (generates rnaseq-compatible samplesheet)
- Force_samplesheet_check: false (handle diverse metadata)

**Exposed:**
- Input file: List of SRA/ENA/GEO accession IDs
- Output directory: Where to save downloaded files and samplesheets
- (Optional) Email for notifications on download completion

### Tools/Methods
- ENA API for metadata retrieval
- FTP download for FASTQ files
- MD5 checksum verification
- Samplesheet generation for nf-core/rnaseq

### Expected Outputs
- Raw FASTQ files
- ENA metadata (CSV)
- nf-core/rnaseq-compatible samplesheet
- MD5 checksums for verification
- Download quality report

### Priority
**P0** - This is the most common use case for fetchngs. RNA-seq is the most widely used sequencing technology, and there are thousands of published datasets that researchers regularly need to download and reanalyze.

### Implementation Notes
- Use nf-core test data (SRR IDs) for initial testing
- XSMALL node should be sufficient (downloads not compute-intensive)
- Runtime depends mainly on file sizes and network speed
- Should work out-of-the-box with default settings

---

## Use Case 2: Download Any Sequencing Data (Generic) (PRIORITY: P1)

### Biological Question
How can researchers download any type of sequencing data (ChIP-seq, ATAC-seq, whole genome, etc.) from public databases?

### Target Audience
- Researchers working with any sequencing modality
- Teams downloading data for diverse analysis types
- Labs accessing reference datasets

### Typical Experimental Design
- Any published sequencing study
- Multiple data types (ChIP-seq, ATAC-seq, WGS, etc.)
- Can be single samples or entire projects

### Key Parameters

**Hardcoded:**
- Download method: FTP
- Force_samplesheet_check: false

**Exposed:**
- Input file: List of accession IDs
- Output directory: Where to save files
- nf_core_pipeline: Optional selector (atacseq, chipseq, rnaseq, etc.)

### Expected Outputs
- Raw FASTQ files
- Generic samplesheet
- Metadata from ENA
- MD5 checksums

### Priority
**P1** - Important but less common than RNA-seq specific use case. Many users will know their data type upfront.

### Implementation Notes
- Very similar to Use Case 1 but without hardcoding pipeline type
- Allows flexibility for different downstream analyses
- Could serve as a template for pipeline-specific apps

---

## Use Case 3: Download Complete Study/Project (PRIORITY: P2)

### Biological Question
How can researchers download all samples from a published study in one operation?

### Target Audience
- Researchers performing comprehensive reanalysis
- Teams building reference databases
- Meta-analysis projects

### Typical Experimental Design
- Entire GEO study (GSE accession)
- Complete SRA project (SRP accession)
- Can include dozens or hundreds of samples

### Key Parameters

**Hardcoded:**
- Download method: FTP
- Auto-resolve study to individual runs

**Exposed:**
- Study/Project ID (GSE, SRP, etc.)
- Output directory

### Expected Outputs
- All FASTQ files from study
- Complete metadata
- Samplesheets for downstream analysis

### Priority
**P2** - Useful but can be achieved by providing all sample IDs from a study in Use Case 1 or 2. The pipeline automatically handles study IDs, so separate app may not be needed.

### Implementation Notes
- May require larger node sizes for projects with many samples
- Download times can be very long (hours to days)
- Consider implementing as enhancement to Use Case 2 rather than separate app

---

## Recommendations

### Implement First
**Use Case 1: RNA-seq Data Download**
- Clearest use case with specific output format
- Most common biological application
- Easy to test with nf-core test data
- Direct integration with nf-core/rnaseq pipeline

### Future Considerations
- **Use Case 2** could be implemented if Use Case 1 succeeds
- **Use Case 3** may not need separate app (functionality already in Use Case 1/2)

### Testing Strategy
1. Start with nf-core test data (small SRA IDs)
2. Test with 2-3 real RNA-seq samples
3. Verify samplesheet format compatibility with rnaseq pipeline
4. Check download integrity (MD5 sums)

---

## Research Sources

- nf-core/fetchngs documentation: https://nf-co.re/fetchngs/1.12.0/
- GitHub repository: https://github.com/nf-core/fetchngs
- Test datasets: https://github.com/nf-core/test-datasets (fetchngs branch)
- Common user queries on nf-core Slack

## Success Criteria

An app is successful if:
- Downloads complete without errors
- FASTQ files pass MD5 verification
- Generated samplesheet is valid for target nf-core pipeline
- Metadata is comprehensive and accurate
- Runtime is reasonable for test data (<30 minutes)
