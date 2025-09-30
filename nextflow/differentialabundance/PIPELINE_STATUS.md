# Pipeline: differentialabundance

**Latest Version**: 1.5.0
**Last Updated**: 2025-09-30
**Overall Status**: 🔄 In Progress

## Summary

The nf-core/differentialabundance pipeline performs differential abundance analysis on feature/observation matrices from various platforms including RNA-seq, proteomics, and microarray data. It supports multiple statistical methods (DESeq2, edgeR, limma) and generates comprehensive reports with interactive visualizations.

**Key Features**:
- Differential expression analysis for RNA-seq data
- Proteomics differential abundance (MaxQuant output)
- Microarray analysis (Affymetrix CEL files)
- Gene set enrichment analysis
- Interactive HTML reports and optional Shiny apps
- Supports complex experimental designs with multiple factors

## Use Cases Identified

1. **RNA-seq Differential Expression (Two-Group)** - P0 ✅ Working
2. **Proteomics Differential Abundance** - P1 (Not Implemented)
3. **Multi-Factor RNA-seq Analysis** - P1 (Not Implemented)
4. **Time-Series Gene Expression** - P2 (Not Implemented)

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [x] App 1: rnaseq-two-group - 🔄 Testing
- [ ] App 2: proteomics-abundance (Not Started)
- [ ] App 3: multi-factor-rnaseq (Not Started)
- [ ] App 4: time-series-expression (Not Started)

## Test Data Availability

✅ **nf-core test data available**: https://github.com/nf-core/test-datasets (differentialabundance branch)

**Test Dataset**: Mouse RNA-seq data (SRP254919)
- Samplesheet: Available
- Gene counts matrix: Top 1000 genes
- Contrasts: Pre-defined comparisons
- GTF annotations: Ensembl GRCm38.81
- Gene sets: MSigDB for mouse

## Issues Encountered

None yet - initial implementation in progress.

## Success Metrics

- 0/4 apps working (target: 3-4 working)
- 0/4 apps tested successfully
- Testing started: 2025-09-30