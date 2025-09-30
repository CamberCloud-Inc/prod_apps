# Protein Structure Prediction: Single Protein (AlphaFold2)

## Overview

This app predicts 3D protein structures from amino acid sequences using AlphaFold2, the breakthrough deep learning model developed by DeepMind. It's optimized for single protein (monomer) predictions.

## Use Case

**Target Users**: Structural biologists, drug discovery scientists, protein engineers, biochemists

**Biological Questions**:
- What is the 3D structure of my protein?
- Where are the binding sites or active sites?
- How might mutations affect protein folding?
- What is the overall fold and domain architecture?

## Input Requirements

### 1. Sample Sheet (CSV)

Format:
```csv
id,fasta
protein1,protein1.fasta
protein2,protein2.fasta
```

- `id`: Unique protein identifier
- `fasta`: Path to FASTA file with amino acid sequence

### 2. FASTA Files

Each FASTA file should contain one protein sequence:

```
>my_protein_id Description
MKTAYIAKQRQISFVKSHFSRQLEERL...
```

- Use single-letter amino acid codes (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y)
- Works best for proteins 50-2000 amino acids
- Complete sequences preferred

## Expected Outputs

### Structure Files
- `ranked_0.pdb` through `ranked_4.pdb` - Five predicted models ranked by confidence
- `relaxed_model_*.pdb` - Energy-minimized structures
- `unrelaxed_model_*.pdb` - Raw predictions before refinement

### Confidence Scores
- `ranking_debug.json` - Ranking scores for all models
- `pae_plot_*.png` - Predicted Aligned Error visualizations
- Color-coded PDB files (blue=high confidence, red=low confidence)

### Analysis Files
- `features.pkl` - Multiple sequence alignment features
- `timings.json` - Runtime statistics
- `msas/` - Multiple sequence alignment files
- `multiqc_report.html` - Comprehensive summary report

## Confidence Interpretation

### pLDDT Scores (per residue, 0-100)
- **>90**: Very high confidence - structure very reliable
- **70-90**: High confidence - generally reliable
- **50-70**: Low confidence - may have errors
- **<50**: Very low confidence - often disordered regions

### Typical Patterns
- Structured domains: 70-100
- Loops/flexible regions: 50-70
- Disordered regions: <50 (naturally unstructured)

## Resource Requirements

| Protein Size | Recommended Node | Typical Runtime (GPU) |
|--------------|------------------|----------------------|
| 50-150 aa | XSMALL | 10-20 min |
| 150-400 aa | SMALL | 20-40 min |
| 400-800 aa | MEDIUM | 40-90 min |
| 800-2000 aa | LARGE | 1.5-3 hours |

**Note**: GPU dramatically speeds up predictions (10-100x faster than CPU)

## Algorithm Details

**Method**: AlphaFold2 with monomer_ptm preset

**Key Parameters** (hardcoded in command):
- `--mode alphafold2`: Use AlphaFold2 algorithm
- `--alphafold2_model_preset monomer_ptm`: Single protein with pTM score
- `--use_gpu true`: Enable GPU acceleration
- `--full_dbs false`: Use reduced databases (faster, still accurate)
- `--num_recycle 3`: Number of structure refinement iterations

**Pipeline Steps**:
1. Search sequence databases for evolutionary relatives
2. Build multiple sequence alignments (MSAs)
3. Extract evolutionary coupling information
4. Predict inter-residue distances and angles with neural networks
5. Optimize 3D structure to satisfy predicted constraints
6. Refine structure through recycling (3 iterations)
7. Energy minimize with Amber force field (relaxation)
8. Rank models by confidence scores

## Test Data

Test data is available from nf-core:
- Sample sheet: `https://raw.githubusercontent.com/nf-core/test-datasets/proteinfold/testdata/samplesheet/v1.2/samplesheet.csv`
- Test proteins: T1024 (408 residues), T1026 (small test protein)

The test data includes small proteins that run quickly for validation.

## Tips for Success

1. **Complete sequences**: Full-length sequences give best results
2. **Check confidence**: Always examine pLDDT scores; low scores indicate uncertain predictions
3. **Compare models**: Look at all 5 ranked models to assess consistency
4. **Domain boundaries**: Well-defined domains predict better than full-length proteins with long disordered regions
5. **Validation**: If possible, compare to known structures of homologs

## Limitations

- **No cofactors/ligands**: Predictions don't include metals, small molecules, or post-translational modifications
- **Single conformations**: Predicts one structure, but proteins may have multiple functional states
- **Membrane proteins**: More challenging, especially transmembrane helices
- **Intrinsically disordered**: Cannot predict structure for naturally disordered proteins (they have no stable structure)
- **Novel folds**: Works best for proteins with some similarity to training data

## Differences from Other Modes

### vs Multimer Mode
- Monomer: Single polypeptide chain
- Multimer: Multiple chains (protein complexes)

### vs ColabFold
- AlphaFold2: More accurate, uses full algorithm
- ColabFold: Faster, uses MSA server, good for screening

### vs ESMFold
- AlphaFold2: Highest accuracy, uses MSAs, slower
- ESMFold: Very fast, no MSAs, lower accuracy

## Troubleshooting

### Issue: Low confidence scores (<50) across entire protein
- **Cause**: Protein may be intrinsically disordered or sequence quality issue
- **Solution**: Check if protein is known to be disordered; verify sequence is correct

### Issue: High confidence in domains but low in linkers
- **Cause**: Normal - flexible linkers are naturally less structured
- **Solution**: This is expected; focus on high-confidence domain structures

### Issue: Very long runtime
- **Cause**: Large protein or insufficient GPU
- **Solution**: Use larger node size with GPU; consider splitting into domains

### Issue: Out of memory error
- **Cause**: Protein too large for allocated resources
- **Solution**: Increase node size to LARGE or split protein into domains

## References

- **AlphaFold2 Paper**: Jumper et al. (2021) Nature 596, 583-589
- **Pipeline**: https://nf-co.re/proteinfold
- **AlphaFold Database**: https://alphafold.ebi.ac.uk/

## Version Information

- **Pipeline**: nf-core/proteinfold v1.2.0
- **AlphaFold2**: Latest version from DeepMind
- **Database**: Reduced databases (for speed) - can be changed to full DBs if needed

## Testing Instructions

See TESTING_LOG.md for detailed testing attempts and results.