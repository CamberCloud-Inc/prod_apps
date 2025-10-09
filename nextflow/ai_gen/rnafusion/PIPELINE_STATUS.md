# Pipeline: nf-core/rnafusion

**Latest Version**: 4.0.0
**Last Updated**: 2025-09-30
**Overall Status**: 🔄 In Progress

## Summary

nf-core/rnafusion is a bioinformatics best-practice analysis pipeline for RNA sequencing designed for detecting and visualizing gene fusions. Gene fusions occur when two previously separate genes become joined, creating a hybrid gene that can drive cancer development or indicate chromosomal translocations. This pipeline integrates multiple fusion detection tools (STAR-Fusion, arriba, FusionCatcher) to provide robust, reproducible fusion gene detection with comprehensive visualization and reporting.

**Key Features**:
- Multiple fusion detection algorithms for consensus calling
- Quality control and visualization in interactive reports
- Transcript assembly and splicing aberration detection
- VCF, HTML, TSV, and PDF output formats
- Designed specifically for cancer genomics research

**Technical Requirements**:
- Only supports GRCh38 reference genome (human)
- Paired-end RNA-seq data required
- Must use Singularity or Docker (Conda not supported)
- Minimum read length: 130bp for FusionCatcher

## Use Cases Identified

1. **Cancer Fusion Detection** - Priority: P0 [🔄 In Progress]
   - Detect oncogenic fusion genes in tumor RNA-seq
   - Directory: `cancer-fusion-detection/`

2. **Translocation Validation** - Priority: P1 [🔲 Not Started]
   - Validate known translocations at RNA level
   - Directory: `translocation-validation/`

3. **Leukemia Fusion Profiling** - Priority: P1 [🔲 Not Started]
   - Identify fusion genes in hematologic malignancies
   - Directory: `leukemia-fusion-profiling/`

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [x] Pipeline documentation reviewed
- [x] App 1: cancer-fusion-detection - [⚠️ Ready for Manual Testing]
- [ ] App 2: translocation-validation - [Not Started]
- [ ] App 3: leukemia-fusion-profiling - [Not Started]

## Technical Notes

**Reference Genome**:
- Only GRCh38 is supported - pipeline is human-specific
- Custom references not recommended by nf-core team

**Data Requirements**:
- Paired-end RNA-seq strongly recommended
- Single-end reads only work with STAR-Fusion and arriba (not FusionCatcher)
- Minimum 50M reads per sample for robust detection

**Fusion Callers Available**:
- STAR-Fusion: Fast, accurate, splice-aware
- arriba: High sensitivity, good visualization
- FusionCatcher: Comprehensive, established tool
- Consensus approach: Multiple callers increase confidence

## Issues Encountered

**Implementation Phase**:
- Successfully identified 3 biological use cases
- Created comprehensive documentation (USE_CASES.md)
- Implemented highest priority app (cancer-fusion-detection)
- Verified test data availability in nf-core/test-datasets

**Testing Phase** (2025-09-30):
- Manual testing required due to platform CLI constraints
- All files prepared and ready for testing:
  - app.json with complete configuration
  - test_samplesheet.csv with verified nf-core test data URLs
  - Comprehensive README.md and TESTING_LOG.md
  - STATUS.txt indicating ready state

**Platform Considerations**:
- rnafusion only supports GRCh38/hg38 (human genome) - no other organisms
- Pipeline requires paired-end RNA-seq data
- Uses three fusion callers: STAR-Fusion, arriba, FusionCatcher
- Reference genome via iGenomes: s3://ngi-igenomes/igenomes/Homo_sapiens/NCBI/GRCh38/

## Success Metrics

- 0/3 apps working (1 ready for testing, awaiting manual validation)
- 1/3 apps implemented and documented
- Target: At least 1 working app for cancer fusion detection

**App 1 Status** (cancer-fusion-detection):
- Implementation: ✅ Complete
- Documentation: ✅ Complete
- Test data: ✅ Verified and ready
- Manual testing: ⚠️ Required (documented in TESTING_LOG.md)
- Expected outcome: High probability of success (using official nf-core test data)