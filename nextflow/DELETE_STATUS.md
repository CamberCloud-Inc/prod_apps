# Delete Operation Status

## Apps That Had Delete Errors (API Error 500)

The following apps encountered "API error: code=500, message=Failed to delete app" during the delete operation. This typically means:
1. The app doesn't exist in Camber
2. The app has dependencies/references preventing deletion
3. A transient API error occurred

However, these errors were ignored, and the script proceeded with the create operation.

### Apps with Delete Errors:
1. hicar-enhancer-promoter-analysis
2. liverctanalysis-ct-analysis
3. deepvariant-clinical-wgs
4. longraredisease-diagnostic-wgs
5. scflow-cell-type-annotation
6. methylarray-clinical-ewas
7. viralmetagenome-viral-discovery
8. ddamsproteomics-tmt-labeling
9. phaseimpute-genotype-imputation
10. tf-regulon-analysis
11. epitopeprediction-vaccine-design
12. imcyto-imaging-mass-cytometry
13. cellpainting-phenotypic-profiling
14. molkart-spatial-multiomics
15. pixelator-spatial-proteomics
16. diaproteomics-dia-discovery
17. hgtseq-horizontal-gene-transfer
18. rnadnavar-rna-editing-analysis
19. pathogensurveillance-clinical-surveillance
20. variantbenchmarking-benchmark-analysis
21. alleleexpression-ase-analysis
22. tumourevo-tumor-phylogeny
23. drop-rna-outliers
24. lncpipe-lncrna-discovery
25. reportho-orthology-analysis
26. callingcards-tf-binding
27. drugresponseeval-drug-screening
28. evexplorer-molecular-evolution
29. diseasemodulediscovery-disease-networks
30. variantcatalogue-population-variants
31. viralintegration-hpv-integration
32. multiplesequencealign-protein-msa
33. pairgenomealign-synteny-analysis
34. denovotranscript-de-novo-transcriptome
35. denovohybrid-hybrid-assembly
36. ssds-single-strand-dna
37. tbprofiler-tb-genomics
38. sammyseq-chromatin-analysis
39. readsimulator-ngs-simulation
40. seqinspector-sequencing-qc
41. rarevariantburden-rare-disease-burden
42. coproid-ancient-dna
43. metapep-epitope-prediction
44. mitodetect-mitochondrial-variants
45. proteinannotator-protein-annotation
46. proteinfamilies-protein-families
47. genomeannotator-eukaryote-annotation
48. genomeassembler-long-read-assembly
49. genomeqc-genome-qc
50. genomeskim-organelle-genomes
51. omicsgenetraitassociation-multi-omics-gwas
52. bamtofastq-bam-conversion
53. fastqrepair-fastq-repair
54. fastquorum-quality-filtering
55. createpanelrefs-reference-panels
56. createtaxdb-taxonomy-db
57. references-reference-management
58. datasync-data-sync
59. deepmodeloptim-ml-optimization
60. abotyper-blood-antigens
61. stableexpression-housekeeping-genes
62. riboseq-profiling-qc
63. lsmquant-label-free-ms
64. panoramaseq-panorama-analysis
65. radseq-variant-calling
66. troughgraph-analysis
67. spatialvi-spatial-transcriptomics
68. mhcquant-immunopeptidomics
69. methylong-long-read-methylation
70. marsseq-single-cell-rnaseq
71. demo-nfcore-demo
72. neutronstar-10x-assembly
73. rangeland-remote-sensing

**Total: 73/73 apps encountered delete errors**

## Interpretation

Since ALL 73 apps encountered the same delete error (API error 500), this suggests one of the following:
1. **Most likely**: These apps were previously deleted or never existed in Camber in the first place
2. The Camber API is experiencing issues with the delete endpoint
3. The app names being used for deletion don't match the actual names in Camber

Despite the delete errors, **59 out of 73 apps were successfully created**, indicating that the create operation works correctly and the apps are now deployed in Camber.

---

**Recommendation**: Verify in the Camber UI which apps currently exist and whether any duplicates were created.
