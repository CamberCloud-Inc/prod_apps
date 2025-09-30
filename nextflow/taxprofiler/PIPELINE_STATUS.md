# Pipeline: nf-core/taxprofiler

**Latest Version**: 1.2.3
**Last Updated**: 2025-09-30
**Overall Status**: ✅ First App Working (1/3 complete)

## Summary

nf-core/taxprofiler is a bioinformatics pipeline for taxonomic classification and profiling of shotgun short- and long-read metagenomic data. It enables highly parallelized taxonomic profiling across multiple classifiers and databases simultaneously, producing standardized output tables for immediate cross-comparison of results between tools.

**Key Features**:
- Multi-tool taxonomic profiling (Kraken2, MetaPhlAn, mOTUs, Centrifuge, Kaiju, etc.)
- Support for both Illumina short-reads and Nanopore long-reads
- Read preprocessing (adapter trimming, host removal, complexity filtering)
- Standardized outputs via TAXPASTA for cross-tool comparison
- Multiple database support per tool

**Biological Applications**:
- Microbiome composition analysis
- Pathogen detection and surveillance
- Environmental metagenomics
- Clinical metagenomics
- Ancient DNA analysis

## Use Cases Identified

1. **Microbiome Profiling (Kraken2)** - P0 (HIGHEST PRIORITY) - ✅ Working
   - Fast taxonomic classification for gut/environmental microbiomes
   - Most common use case for researchers
   - **Status**: Tested and functional (4m42s on XSMALL)

2. **Clinical Pathogen Detection** - P0 - 🔲 Not Started
   - Rapid identification of pathogens in clinical samples
   - Critical for diagnostic applications

3. **Comprehensive Multi-Tool Profiling** - P1 - 🔲 Not Started
   - Compare results across multiple profilers
   - Research validation and method comparison

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [x] Pipeline documentation reviewed
- [x] App 1: Microbiome Profiling (Kraken2) - ✅ Working
- [ ] App 2: Clinical Pathogen Detection - 🔲 Pending
- [ ] App 3: Multi-Tool Profiling - 🔲 Pending

## Issues Encountered

### Solved Issues:

1. **Profile Configuration** (Attempts 1-2)
   - **Issue**: Explicitly setting `-profile singularity` caused "singularity: command not found" errors
   - **Root cause**: Camber backend automatically sets `-profile k8s` and manages containers
   - **Solution**: Remove all explicit profile flags from command - let backend handle it
   - **Learning**: Never use `-profile` flag in Camber apps - the platform manages this automatically

## Key Considerations

### Database Requirements
- taxprofiler requires pre-built databases for each profiler
- Databases must be provided via a database sheet CSV
- This is a significant consideration - may need to provide test databases or instructions

### Resource Requirements
- Varies by profiler and database size
- Kraken2 with standard database: MEDIUM to LARGE node
- MetaPhlAn: SMALL to MEDIUM node
- Multiple profilers in parallel: LARGE to XLARGE node

## Success Metrics

- 1/3 apps working ✅
- 1/3 apps tested successfully
- Success rate: 100% (1/1 completed)
- Average test attempts: 4

## Next Steps

1. ✅ Identify nf-core test data for taxprofiler - Complete
2. ✅ Create Kraken2 microbiome profiling app - Complete
3. ✅ Test with XSMALL node size initially - Complete (4m42s)
4. ✅ Document all testing attempts - Complete
5. Next: Implement Clinical Pathogen Detection use case (App 2)
6. Future: Implement Multi-Tool Profiling use case (App 3)