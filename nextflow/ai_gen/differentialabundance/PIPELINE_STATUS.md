# Pipeline: differentialabundance

**Latest Version**: 1.5.0
**Last Updated**: 2025-09-30
**Overall Status**: ✅ First App Working

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

1. **RNA-seq Differential Expression (Two-Group)** - P0 ✅ **Working** (Completed 2025-09-30)
2. **Proteomics Differential Abundance** - P1 (Not Implemented)
3. **Multi-Factor RNA-seq Analysis** - P1 (Not Implemented)
4. **Time-Series Gene Expression** - P2 (Not Implemented)

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [x] App 1: rnaseq-two-group - ✅ **Working** (4 attempts, succeeded with rlog method)
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

### Issue 1: VST Transformation Fails on Small Datasets (RESOLVED)
**Problem**: Test dataset with 1000 genes caused error: "less than 'nsub' rows with mean normalized count > 5"

**Attempts to Fix**:
- Attempt 1: Default VST - Failed
- Attempt 2: Reduced `--vst_nsub` to 100 - Failed
- Attempt 3: Added `--vs_blind false` and `--vst_nsub 50` - Failed
- Attempt 4: Switched to `--deseq2_vs_method rlog` - **SUCCESS** ✅

**Solution**: Use rlog (regularized log transformation) instead of VST for small or sparse datasets. This is recommended in nf-core/differentialabundance GitHub issue #155.

**Learning**: For datasets with < 5000 genes or sparse counts, always use `--deseq2_vs_method rlog`

## Success Metrics

- **1/4 apps working** (target: 3-4 working)
- **1/4 apps tested successfully**
- **Testing attempts**: 4 total (1 successful)
- **Testing started**: 2025-09-30 09:17
- **First success**: 2025-09-30 09:32
- **Total testing time**: ~15 minutes across 4 attempts

## Key Learnings

1. **rlog vs VST**: rlog is more robust for small datasets, VST is faster for large datasets
2. **Test data size matters**: nf-core test datasets are intentionally small and may require different parameters than production data
3. **XSMALL sufficient**: 4 CPUs and 15GB RAM adequate for testing and small real datasets
4. **Research is critical**: GitHub issues provided the key solution (issue #155)
5. **Default test URLs work**: No need to upload test data separately