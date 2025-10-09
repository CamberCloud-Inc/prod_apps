# nf-core/proteinfold Use Cases

This document identifies the biological use cases for the proteinfold pipeline, prioritized by frequency of use and biological impact.

---

## Use Case 1: Single Protein Structure Prediction (Monomer) 🌟 HIGHEST PRIORITY

**Biological Question**: What is the 3D structure of my protein of interest?

**Target Audience**:
- Structural biologists studying individual proteins
- Drug discovery scientists needing target structures
- Protein engineers designing mutations
- Biochemists investigating protein function

**Typical Experimental Context**:
- You have identified a protein gene/sequence from genomics data
- You want to understand the protein's function through its structure
- You need a structure for drug docking or binding site analysis
- You want to predict effects of mutations on protein folding

**Typical Scale**:
- 1-10 individual proteins
- Sequence length: 50-2000 amino acids (typical proteins)
- Single polypeptide chains

**Key Parameters**:

*Hardcoded (hidden from users)*:
- Mode: `alphafold2` (most accurate and well-established)
- Model preset: `monomer_ptm` (predicts structure with confidence scores)
- Database: Use available pre-computed databases
- Recycles: 3 (standard for good predictions)
- Use GPU: true (dramatically faster)

*Exposed to users*:
- Input samplesheet (CSV with protein IDs and FASTA files)
- Output directory
- (Optional) Number of models to generate (1-5, default 5)

**Input Format**:
```csv
id,fasta
my_protein,my_protein.fasta
another_protein,another_protein.fasta
```

Where each FASTA file contains:
```
>my_protein_id Description
MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQTLGQHDFSAGEGLYTHMKALRPDEDRLSPLHSVYVDQWDWERVMGDGERQFSTLKSTVEAIWAGIKATEAAVSEEFGLAPFLPDQIHFVHSQELLSRYPDLDAKGRERAIAKDLGAVFLVGIGGKLSDGHRHDVRAPDYDDWSTPSELGHAGLNGDILVWNPVLEDAFELSSMGIRVDADTLKHQLALTGDEDRLELEWHQALLRGEMPQTIGGGIGQSRLTMLLLQLPHIGQVQAGVWPAAVRESVPSLL
```

**Expected Outputs**:
- PDB structure files (3D coordinates)
- Confidence scores (pLDDT per residue)
- PAE (Predicted Aligned Error) plots
- Relaxed structures (energy minimized)
- Multiple model predictions for ensemble analysis

**Tools Used**: AlphaFold2 with monomer_ptm model preset

**Resource Requirements**:
- XSMALL for testing (small proteins, <200 residues)
- SMALL to MEDIUM for typical proteins (200-500 residues)
- LARGE for large proteins (500-2000 residues) or multiple predictions

**Expected Runtime**:
- Test data (2 small proteins): 10-30 minutes on XSMALL with GPU
- Single typical protein: 30-60 minutes on SMALL with GPU
- Large protein: 2-4 hours on MEDIUM with GPU

**Priority**: **P0** - Most common use case, foundational for all structure prediction

**Biological Impact**: HIGH
- Enables functional annotation of proteins
- Guides experimental design
- Accelerates drug discovery
- Predicts mutation effects

**Implementation Notes**:
- Start with ColabFold mode for faster testing (doesn't require full database)
- If successful, provide AlphaFold2 as more accurate option
- ESMFold as ultra-fast screening option (separate app)

---

## Use Case 2: Protein Complex Prediction (Multimer)

**Biological Question**: How do two or more proteins interact to form a complex?

**Target Audience**:
- Researchers studying protein-protein interactions
- Drug developers targeting protein interfaces
- Systems biologists analyzing cellular machinery
- Structural biologists studying multi-protein assemblies

**Typical Experimental Context**:
- You have identified interacting proteins (e.g., from pull-down experiments)
- You want to understand the binding interface
- You need to predict complex structure for drug design
- You want to understand stoichiometry of a complex

**Typical Scale**:
- 2-4 protein chains in complex
- Total size: 100-1000 residues across all chains
- Can include multiple copies of same protein

**Key Parameters**:

*Hardcoded*:
- Mode: `alphafold2`
- Model preset: `multimer` (specifically for protein complexes)
- Database: Full databases for accurate interaction predictions
- Use GPU: true

*Exposed*:
- Input samplesheet (FASTA with multiple sequences per complex)
- Output directory
- Number of models (default 5)

**Input Format**:
```csv
id,fasta
protein_complex,complex.fasta
```

Where FASTA contains multiple sequences:
```
>subunit_A
MKTAYIAKQRQISFVKSHFSRQ...
>subunit_B
AGVWPAAVRESVPSLLQKR...
```

**Expected Outputs**:
- PDB structure of the complex
- Interface confidence scores
- ipTM scores (interface predicted TM-score)
- PAE plots showing inter-chain contacts
- Binding interface analysis

**Tools Used**: AlphaFold2 multimer mode

**Resource Requirements**:
- MEDIUM minimum (complexes require more memory)
- LARGE for large complexes or multiple predictions

**Expected Runtime**:
- Small complex (2 proteins, <300 residues total): 1-2 hours
- Medium complex (3 proteins): 3-6 hours
- Large complex: 6-12 hours

**Priority**: **P1** - Important for protein interaction studies

**Biological Impact**: HIGH
- Reveals protein interaction mechanisms
- Identifies drug-targetable interfaces
- Predicts complex assembly
- Guides mutation studies of interactions

---

## Use Case 3: Batch Protein Structure Prediction (Proteome-scale)

**Biological Question**: What are the structures of all proteins in my organism/pathway of interest?

**Target Audience**:
- Computational biologists analyzing proteomes
- Evolutionary biologists studying protein families
- Systems biologists mapping pathway structures
- Annotators characterizing newly sequenced genomes

**Typical Experimental Context**:
- You have sequenced a new organism's genome
- You want structural annotations for all predicted proteins
- You're studying structural evolution across species
- You need to prioritize experimental structure determination

**Typical Scale**:
- 10-1000+ proteins
- Automated processing
- High-throughput screening

**Key Parameters**:

*Hardcoded*:
- Mode: `esmfold` (fastest for large-scale predictions)
- OR `colabfold` (good accuracy/speed tradeoff)
- Use GPU: true
- Minimal models: 1 (for speed)

*Exposed*:
- Input samplesheet (many proteins)
- Output directory
- Batch size for parallel processing

**Input Format**:
```csv
id,fasta
protein_001,protein_001.fasta
protein_002,protein_002.fasta
protein_003,protein_003.fasta
...
protein_100,protein_100.fasta
```

**Expected Outputs**:
- PDB structures for all proteins
- Summary statistics (confidence, fold types)
- Batch quality control reports
- Structural similarity clustering

**Tools Used**: ESMFold or ColabFold (faster than AlphaFold2)

**Resource Requirements**:
- LARGE or XLARGE for batch processing
- Parallel execution across many proteins

**Expected Runtime**:
- 10 proteins with ESMFold: 30-60 minutes
- 100 proteins with ESMFold: 3-6 hours
- 1000 proteins: Run as multiple batches

**Priority**: **P2** - Specialized use case for computational projects

**Biological Impact**: MEDIUM-HIGH
- Enables proteome-wide structural analysis
- Accelerates functional annotation
- Identifies structural novelty
- Guides experimental priorities

**Implementation Notes**:
- ESMFold is best for batch (no MSA required, very fast)
- Consider implementing as separate queue/scheduling system
- May need to chunk large proteomes into sub-batches

---

## Additional Potential Use Cases (Lower Priority)

### Use Case 4: Mutation Effect Prediction
- Predict structural impact of point mutations
- Compare wild-type vs mutant structures
- Requires: Multiple runs with sequence variants

### Use Case 5: Protein Design Validation
- Validate designed sequences will fold correctly
- Iterate on designs based on predictions
- Requires: Rapid re-prediction workflow

### Use Case 6: Domain Structure Prediction
- Predict structures of isolated domains
- Map domain boundaries
- Requires: Sequence parsing and domain definition

---

## Implementation Priority

**Phase 1 (Current)**:
✅ Use Case 1: Single Protein (Monomer) - **IMPLEMENTING NOW**

**Phase 2 (Future)**:
- Use Case 2: Protein Complex (Multimer)

**Phase 3 (Future)**:
- Use Case 3: Batch Prediction

**Later**:
- Additional specialized use cases based on user demand

---

## Technical Considerations

**Database Requirements**:
- AlphaFold2: ~2.2TB for full databases (reduced: ~500GB)
- ColabFold: Uses remote MSA server (no local database) OR local databases
- ESMFold: No external database required (model only)

**GPU Benefits**:
- 10-100x faster than CPU
- Essential for practical use
- Recommend GPU-enabled nodes

**Quality Metrics**:
- pLDDT >90: Very high confidence
- pLDDT 70-90: High confidence
- pLDDT 50-70: Low confidence
- pLDDT <50: Very low confidence (disordered regions)

**Test Data Available**:
- nf-core/test-datasets proteinfold branch
- Small test proteins for validation
- Both monomer and multimer examples