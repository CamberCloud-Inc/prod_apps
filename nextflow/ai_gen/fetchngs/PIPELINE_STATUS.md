# Pipeline: nf-core/fetchngs

**Latest Version**: 1.12.0
**Last Updated**: 2025-09-30
**Overall Status**: 🔄 In Progress

## Summary

nf-core/fetchngs is a bioinformatics pipeline designed to automatically download raw sequencing data and metadata from public databases. It supports multiple public repositories including SRA (Sequence Read Archive), ENA (European Nucleotide Archive), DDBJ (DNA Data Bank of Japan), and GEO (Gene Expression Omnibus). This pipeline is essential for researchers who need to reanalyze published data, validate findings, or integrate public datasets into their own analyses.

## Key Features

- Downloads raw FASTQ files from multiple public databases (SRA/ENA/DDBJ/GEO)
- Resolves various accession formats (run, experiment, study, project IDs)
- Multiple download methods (FTP, Aspera, sra-tools)
- Automatically generates samplesheets compatible with other nf-core pipelines
- Fetches comprehensive metadata from ENA database
- Handles multiple runs from the same experiment

## Use Cases Identified

1. **Public Data Download for RNA-seq** - ✅ Selected for implementation
   - Download published RNA-seq data for reanalysis or meta-analysis
   - Priority: P0 (most common use case)

2. **Public Data Download for Any Sequencing Type** - 🔲 Not Started
   - Generic downloader for any sequencing modality
   - Priority: P1

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [x] App 1: public-data-rnaseq - ✅ Working (Tested successfully)
- [ ] App 2: public-data-generic - 🔲 Not Started (Optional)

## Biological Applications

fetchngs enables researchers to:
- **Reproduce Published Results**: Download data from publications to verify findings
- **Meta-Analysis**: Combine data from multiple studies for larger-scale analysis
- **Method Validation**: Test new analysis methods on published benchmark datasets
- **Data Reuse**: Leverage existing public data for new biological questions
- **Training/Education**: Access real-world datasets for learning bioinformatics

## Technical Notes

- Pipeline is very lightweight - primarily performs downloads and metadata operations
- No heavy computational requirements
- Runtime depends on file sizes and download speeds
- XSMALL node size is sufficient for most use cases
- **Tested and confirmed working**: Job 4394 completed in 57 seconds on XSMALL node

## Success Metrics

- 1/1 apps working (public-data-rnaseq)
- 1/1 apps tested successfully
- Test runtime: 57 seconds
- Test dataset: 2 SRA accessions successfully downloaded

## Issues Encountered

### Issue 1: Output Path Format (Resolved)
- **Problem**: Using full stash paths (e.g., `stash://user/path/output`) caused immediate failure
- **Solution**: Use simple relative paths (e.g., `results-output`) instead
- **Status**: ✅ Resolved in Attempt 2
