# Pipeline: fetchngs

**Latest Version**: 1.12.0
**Last Updated**: 2025-09-30
**Overall Status**: 🔄 In Progress

## Summary

nf-core/fetchngs is a bioinformatics pipeline designed to fetch metadata and raw FastQ files from public sequencing databases. It supports multiple database identifiers (SRA, ENA, DDBJ, GEO) and can automatically generate samplesheets compatible with other nf-core pipelines.

**Key Features**:
- Download sequencing data from public repositories (SRA/ENA/DDBJ/GEO)
- Automatic metadata retrieval via ENA API
- Multiple download methods (FTP, Aspera, SRA tools)
- MD5 checksum verification
- Generate samplesheets for downstream nf-core pipelines

**Biological Applications**:
- Access publicly available sequencing datasets
- Reproduce published analyses
- Meta-analysis across multiple studies
- Download reference datasets for method validation
- Retrieve data for reanalysis or secondary analysis

## Use Cases Identified

1. **SRA Download for RNA-seq** - ✅ Priority 1 (IMPLEMENTED)
   - Download RNA-seq data from SRA/GEO accessions
   - Generate samplesheet for nf-core/rnaseq
   - Target: Researchers reanalyzing published RNA-seq studies

2. **ENA Bulk Data Download** - 🔲 Priority 2 (TODO)
   - Download large cohorts from ENA
   - Optimized for bulk downloads
   - Target: Meta-analysis researchers

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [x] App 1: sra-download-rnaseq - 🔄 In Progress
- [ ] App 2: ena-bulk-download - Not Started

## Issues Encountered

None yet - initial implementation in progress.

## Success Metrics

- 0/2 apps working
- 0/2 apps tested successfully
- Testing attempts: 0/5 for sra-download-rnaseq

## Notes

- fetchngs is lightweight and should work well on XSMALL nodes
- No heavy computation, mainly network I/O for downloads
- Key challenge will be ensuring proper integration with Camber stash system
- Test data available from nf-core/test-datasets