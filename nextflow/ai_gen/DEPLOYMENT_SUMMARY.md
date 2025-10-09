# Nextflow Apps Deployment Summary

**Date**: 2025-10-01
**Total Apps Processed**: 73 (Batches 14-21 + 3 already enhanced)

## Overall Results

- **Successfully Deployed**: 59/73 (80.8%)
- **Failed**: 14/73 (19.2%)

---

## Successfully Deployed Apps (59)

### Batch 14 (7/8 successful)
1. ✓ longraredisease/diagnostic-wgs → longraredisease-diagnostic-wgs
2. ✗ scflow/cell-type-annotation → scflow-cell-type-annotation (validation errors)
3. ✓ methylarray/clinical-ewas → methylarray-clinical-ewas
4. ✓ viralmetagenome/viral-discovery → viralmetagenome-viral-discovery
5. ✓ ddamsproteomics/tmt-labeling → ddamsproteomics-tmt-labeling
6. ✓ phaseimpute/genotype-imputation → phaseimpute-genotype-imputation
7. ✗ tfactivity/tf-regulon-analysis → tf-regulon-analysis (validation errors)
8. ✓ epitopeprediction/vaccine-design → epitopeprediction-vaccine-design

### Batch 15 (9/10 successful)
9. ✓ imcyto/imaging-mass-cytometry → imcyto-imaging-mass-cytometry
10. ✓ cellpainting/phenotypic-profiling → cellpainting-phenotypic-profiling
11. ✓ molkart/spatial-multiomics → molkart-spatial-multiomics
12. ✓ pixelator/spatial-proteomics → pixelator-spatial-proteomics
13. ✓ diaproteomics/dia-discovery → diaproteomics-dia-discovery
14. ✓ hgtseq/horizontal-gene-transfer → hgtseq-horizontal-gene-transfer
15. ✓ rnadnavar/rna-editing-analysis → rnadnavar-rna-editing-analysis
16. ✓ pathogensurveillance/clinical-surveillance → pathogensurveillance-clinical-surveillance
17. ✓ variantbenchmarking/benchmark-analysis → variantbenchmarking-benchmark-analysis
18. ✗ alleleexpression/ase-analysis → alleleexpression-ase-analysis (validation errors)

### Batch 16 (7/10 successful)
19. ✓ tumourevo/tumor-phylogeny → tumourevo-tumor-phylogeny
20. ✓ drop/rna-outliers → drop-rna-outliers
21. ✓ lncpipe/lncrna-discovery → lncpipe-lncrna-discovery
22. ✓ reportho/orthology-analysis → reportho-orthology-analysis
23. ✓ callingcards/tf-binding → callingcards-tf-binding
24. ✗ drugresponseeval/drug-screening → drugresponseeval-drug-screening (validation errors)
25. ✗ evexplorer/molecular-evolution → evexplorer-molecular-evolution (DefaultValue error)
26. ✓ diseasemodulediscovery/disease-networks → diseasemodulediscovery-disease-networks
27. ✓ variantcatalogue/population-variants → variantcatalogue-population-variants
28. ✓ viralintegration/hpv-integration → viralintegration-hpv-integration

### Batch 17 (10/10 successful)
29. ✓ multiplesequencealign/protein-msa → multiplesequencealign-protein-msa
30. ✓ pairgenomealign/synteny-analysis → pairgenomealign-synteny-analysis
31. ✓ denovotranscript/de-novo-transcriptome → denovotranscript-de-novo-transcriptome
32. ✓ denovohybrid/hybrid-assembly → denovohybrid-hybrid-assembly
33. ✓ ssds/single-strand-dna → ssds-single-strand-dna
34. ✓ tbanalyzer/tb-genomics → tbprofiler-tb-genomics
35. ✓ sammyseq/sammy-analysis → sammyseq-chromatin-analysis
36. ✓ readsimulator/ngs-simulation → readsimulator-ngs-simulation
37. ✓ seqinspector/sequencing-qc → seqinspector-sequencing-qc
38. ✓ rarevariantburden/rare-disease-burden → rarevariantburden-rare-disease-burden

### Batch 18 (10/10 successful)
39. ✓ coproid/ancient-dna → coproid-ancient-dna
40. ✓ metapep/metaproteomics → metapep-epitope-prediction
41. ✓ mitodetect/mitochondrial-variants → mitodetect-mitochondrial-variants
42. ✓ proteinannotator/protein-annotation → proteinannotator-protein-annotation
43. ✓ proteinfamilies/protein-families → proteinfamilies-protein-families
44. ✓ genomeannotator/eukaryote-annotation → genomeannotator-eukaryote-annotation
45. ✓ genomeassembler/short-read-assembly → genomeassembler-long-read-assembly
46. ✓ genomeqc/genome-qc → genomeqc-genome-qc
47. ✓ genomeskim/organelle-genomes → genomeskim-organelle-genomes
48. ✓ omicsgenetraitassociation/multi-omics-gwas → omicsgenetraitassociation-multi-omics-gwas

### Batch 19 (4/10 successful)
49. ✓ bamtofastq/bam-conversion → bamtofastq-bam-conversion
50. ✓ fastqrepair/fastq-repair → fastqrepair-fastq-repair
51. ✓ fastquorum/quality-filtering → fastquorum-quality-filtering
52. ✗ createpanelrefs/reference-panels → createpanelrefs-reference-panels (validation errors)
53. ✗ createtaxdb/taxonomy-db → createtaxdb-taxonomy-db (validation errors)
54. ✗ references/reference-management → references-reference-management (validation errors)
55. ✓ datasync/data-sync → datasync-data-sync
56. ✗ deepmodeloptim/ml-optimization → deepmodeloptim-ml-optimization (validation errors)
57. ✓ abotyper/blood-antigens → abotyper-blood-antigens
58. ✗ stableexpression/housekeeping-genes → stableexpression-housekeeping-genes (validation errors)

### Batch 20 (5/9 successful)
59. ✓ ribomsqc/ribo-profiling-qc → riboseq-profiling-qc
60. ✓ lsmquant/label-free-ms → lsmquant-label-free-ms
61. ✗ panoramaseq/panorama-analysis → panoramaseq-panorama-analysis (JSON parse error)
62. ✓ radseq/rad-seq → radseq-variant-calling
63. ✗ troughgraph/tumor-heterogeneity → troughgraph-analysis (JSON parse error)
64. ✗ spinningjenny/spatial-transcriptomics → spatialvi-spatial-transcriptomics (JSON parse error)
65. ✓ mhcquant/immunopeptidomics → mhcquant-immunopeptidomics
66. ✓ methylong/long-read-methylation → methylong-long-read-methylation
67. ✗ marsseq/mars-seq → marsseq-single-cell-rnaseq (JSON parse error)

### Batch 21 (3/3 successful)
68. ✓ demo/demo-pipeline → demo-nfcore-demo
69. ✓ neutronstar/neutron-star-analysis → neutronstar-10x-assembly
70. ✓ rangeland/remote-sensing → rangeland-remote-sensing

### Already Enhanced Apps (3/3 successful)
71. ✓ hicar/enhancer-promoter-loops → hicar-enhancer-promoter-analysis
72. ✓ liverctanalysis/ct-analysis → liverctanalysis-ct-analysis
73. ✓ deepvariant/clinical-wgs → deepvariant-clinical-wgs

---

## Failed Apps (14)

### Validation Errors - Invalid Type Field (10 apps)

**Issue**: Spec[].Type field validation failed on 'oneof' tag
- These apps have invalid type values in their spec array that don't match Camber's allowed types

1. **scflow/cell-type-annotation** → scflow-cell-type-annotation
   - Errors in Spec indices: 8, 10, 11, 12, 13, 14, 15

2. **tfactivity/tf-regulon-analysis** → tf-regulon-analysis
   - Errors in Spec indices: 4, 7

3. **alleleexpression/ase-analysis** → alleleexpression-ase-analysis
   - Errors in Spec indices: 2, 3

4. **drugresponseeval/drug-screening** → drugresponseeval-drug-screening
   - Errors in Spec indices: 0, 1

5. **createpanelrefs/reference-panels** → createpanelrefs-reference-panels
   - Errors in Spec index: 1

6. **createtaxdb/taxonomy-db** → createtaxdb-taxonomy-db
   - Errors in Spec index: 4

7. **references/reference-management** → references-reference-management
   - Errors in Spec index: 5

8. **deepmodeloptim/ml-optimization** → deepmodeloptim-ml-optimization
   - Errors in Spec index: 4

9. **stableexpression/housekeeping-genes** → stableexpression-housekeeping-genes
   - Errors in Spec indices: 0, 4, 5

### DefaultValue Error (1 app)

**Issue**: DefaultValue for type Stash File must be a string

10. **evexplorer/molecular-evolution** → evexplorer-molecular-evolution
    - Error in Spec[0]: DefaultValue type mismatch

### JSON Parse Errors (4 apps)

**Issue**: Invalid character '\n' in string literal
- These apps have malformed JSON, likely newlines embedded in string values

11. **panoramaseq/panorama-analysis** → panoramaseq-panorama-analysis
12. **troughgraph/tumor-heterogeneity** → troughgraph-analysis
13. **spinningjenny/spatial-transcriptomics** → spatialvi-spatial-transcriptomics
14. **marsseq/mars-seq** → marsseq-single-cell-rnaseq

---

## Actions Required

### For Validation Errors (10 apps)
The Spec array contains invalid Type values. Need to:
1. Review each app's spec array
2. Ensure Type values match Camber's allowed types (e.g., "String", "Integer", "Stash File", "Stash Folder", etc.)
3. Correct any typos or invalid type names

### For DefaultValue Error (1 app)
The evexplorer app has a DefaultValue that isn't a string for a Stash File type. Need to:
1. Convert DefaultValue to a string format
2. Ensure it matches expected Stash File path format

### For JSON Parse Errors (4 apps)
The JSON files contain unescaped newline characters in string fields. Need to:
1. Find string fields containing literal newlines
2. Either escape them as `\n` or remove them
3. Likely in the "content" or "description" fields

---

## Next Steps

1. **Fix JSON syntax errors** (4 apps) - Highest priority as these prevent parsing
2. **Fix validation errors** (10 apps) - Correct Type field values
3. **Fix DefaultValue error** (1 app) - Convert to proper format
4. **Re-run deployment** for the 14 failed apps
5. **Verify all 73 apps** are successfully deployed in Camber

---

**Last Updated**: 2025-10-01
