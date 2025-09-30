# Pipeline: proteinfold

**Latest Version**: 1.2.0
**Last Updated**: 2025-09-30
**Overall Status**: 🔄 In Progress

## Summary

The nf-core/proteinfold pipeline performs protein 3D structure prediction using deep learning models including AlphaFold2, ColabFold, and ESMFold. This pipeline revolutionizes structural biology by enabling accurate protein structure prediction from amino acid sequences alone, without requiring experimental structure determination through X-ray crystallography or cryo-EM.

**Biological Applications**:
- Predict 3D structures for proteins without experimental structures
- Understand protein function from structure
- Guide drug design and protein engineering
- Study protein-protein interactions and complexes
- Investigate evolutionary relationships through structure comparison

## Use Cases Identified

1. **Single Protein Structure Prediction (Monomer)** - P0 Priority - ✅ Implementing
2. **Protein Complex Prediction (Multimer)** - P1 Priority - 🔲 Not Started
3. **Batch Structure Prediction** - P2 Priority - 🔲 Not Started

## Implementation Progress

- [x] Research phase complete
- [x] Use cases defined
- [x] Test data identified (nf-core test-datasets)
- [ ] App 1: Single Protein Structure Prediction - 🔄 In Progress
- [ ] App 2: Protein Complex Prediction - 🔲 Not Started
- [ ] App 3: Batch Structure Prediction - 🔲 Not Started

## Key Technical Details

**Supported Methods**:
- AlphaFold2 (monomer and multimer modes)
- ColabFold (faster, uses MSA server)
- ESMFold (no MSA required, very fast)

**Input Format**:
- CSV samplesheet with protein IDs and FASTA file paths
- FASTA files contain amino acid sequences

**Resource Requirements**:
- GPU highly recommended (dramatically faster)
- Large memory requirements for database searches
- Storage for databases (AlphaFold2 requires ~2.2TB)

**Key Parameters**:
- `--mode`: alphafold2, colabfold, or esmfold
- `--alphafold2_model_preset`: monomer, monomer_casp14, monomer_ptm, multimer
- `--use_gpu`: Enable GPU acceleration
- `--full_dbs`: Use full databases vs reduced

## Issues Encountered

None yet - initial implementation in progress.

## Success Metrics

- 0/3 apps working
- 0/3 apps tested successfully
- Target: At least 1 working app (highest priority use case)

## Notes

- ESMFold is fastest but potentially less accurate
- ColabFold is good middle ground (fast, accurate)
- AlphaFold2 is most accurate but slowest and requires large databases
- GPU dramatically speeds up predictions (10-100x faster)
- Test data available in nf-core/test-datasets proteinfold branch