# RNA-seq Two-Group Differential Expression Analysis

## Use Case Description

This app performs statistical comparison of gene expression between two experimental conditions using the DESeq2 method. It's designed for the most common differential expression scenario: comparing a treatment group vs control, disease vs healthy, knockout vs wild-type, or any two-group comparison.

**Target Users**: Molecular biologists, cancer researchers, drug discovery scientists, immunologists, developmental biologists.

**Typical Experiment**: 3-6 biological replicates per group, comparing gene expression between two conditions.

## Input Requirements

### 1. Sample Information Sheet (CSV)

**Required columns**:
- `sample`: Sample identifiers matching count matrix column names
- `condition`: Your two experimental groups (e.g., "control", "treated")

**Optional columns**:
- `replicate`: Biological replicate number
- `batch`: Batch information for technical variation correction

**Example**:
```csv
sample,condition,replicate,batch
ctrl_rep1,control,1,batch1
ctrl_rep2,control,2,batch1
ctrl_rep3,control,3,batch2
treat_rep1,treated,1,batch1
treat_rep2,treated,2,batch1
treat_rep3,treated,3,batch2
```

### 2. Contrasts File (CSV)

Defines which groups to compare.

**Required columns**:
- `id`: Name for this comparison (used in output files)
- `variable`: Column from samplesheet (usually "condition")
- `reference`: Control/baseline group
- `target`: Treatment/experimental group
- `blocking`: Optional blocking variable (e.g., "batch")

**Example**:
```csv
id,variable,reference,target,blocking
treated_vs_control,condition,control,treated,
```

**Interpretation**: Positive fold changes = genes higher in target (treated) vs reference (control).

### 3. Gene Count Matrix (TSV)

Tab-separated file with:
- **Rows**: Genes (with gene_id as first column)
- **Columns**: Samples (matching samplesheet sample names)
- **Values**: Raw or normalized read counts

**Example**:
```
gene_id\tsample1\tsample2\tsample3\tsample4
ENSMUSG00000000001\t100\t95\t450\t425
ENSMUSG00000000028\t5\t3\t2\t4
ENSMUSG00000000037\t2500\t2300\t2600\t2450
```

**Source**: Typically from nf-core/rnaseq pipeline output (`gene_counts.tsv` or `salmon.merged.gene_counts.tsv`).

### 4. Output Directory (Stash Path)

Where results will be saved.

## Expected Outputs

### Differential Expression Results
```
results/
├── differential/
│   ├── deseq2/
│   │   ├── treated_vs_control_results.tsv          # Full results table
│   │   ├── treated_vs_control_significant.tsv      # Only FDR < 0.05
│   │   ├── treated_vs_control_upregulated.tsv      # Up in treatment
│   │   └── treated_vs_control_downregulated.tsv    # Down in treatment
│   ├── volcano_plot.pdf                             # Fold change vs p-value
│   ├── ma_plot.pdf                                  # Expression vs fold change
│   └── heatmap_top_genes.pdf                        # Clustered expression
├── exploratory/
│   ├── pca_plot.pdf                                 # Sample relationships
│   ├── sample_correlation_heatmap.pdf               # Replicate similarity
│   └── dispersion_plot.pdf                          # DESeq2 model fit
├── qc/
│   └── multiqc_report.html                          # Comprehensive QC
└── report.html                                      # Interactive HTML report
```

### Key Result Columns

In differential expression tables:
- `log2FoldChange`: Log2(treatment/control). Positive = up in treatment
- `pvalue`: Raw p-value from statistical test
- `padj`: FDR-adjusted p-value (significance threshold typically 0.05)
- `baseMean`: Average normalized expression across all samples
- `gene_name`: Gene symbol (if annotations provided)
- `gene_biotype`: Gene type (protein_coding, lncRNA, etc.)

## Resource Requirements

| Dataset Size | Node Size | CPUs | RAM | Estimated Runtime |
|--------------|-----------|------|-----|-------------------|
| Test data (1000 genes, 6 samples) | XSMALL | 4 | 15GB | 10-15 min |
| Small (20K genes, 6-10 samples) | SMALL | 8 | 30GB | 20-30 min |
| Standard (20K genes, 10-30 samples) | SMALL-MEDIUM | 8-32 | 30-120GB | 30-60 min |

**Recommendation**: Start with XSMALL for testing, scale up for production data.

## Testing Instructions

### Test with nf-core Data (Mouse RNA-seq)

The app comes pre-configured with test data URLs. Simply run the app with default values to test functionality.

**Test Dataset**: Mouse RNA-seq experiment (SRP254919)
- 6 samples across 2 conditions
- Top 1000 genes (subset for fast testing)
- Pre-defined contrasts

**Steps**:
1. Create app: `camber app create --file app.json`
2. Run with defaults: `camber app run differentialabundance-rnaseq-twogroup`
3. Monitor: `camber job get <job-id>`

### Test with Your Own Data

1. Prepare your three input files (samplesheet, contrasts, matrix)
2. Upload to stash: `camber stash cp file.csv stash://username/myproject/`
3. Run app with custom inputs:
   ```bash
   camber app run differentialabundance-rnaseq-twogroup \
     --input input="stash://username/myproject/samplesheet.csv" \
     --input contrasts="stash://username/myproject/contrasts.csv" \
     --input matrix="stash://username/myproject/gene_counts.tsv" \
     --input outdir="stash://username/myproject/results"
   ```

## Biological Interpretation

### Significant Genes (padj < 0.05)

**Upregulated in treatment** (positive log2FC):
- These genes increase in expression in your experimental condition
- May be activated pathways, stress responses, or treatment effects
- Good candidates for pathway enrichment analysis

**Downregulated in treatment** (negative log2FC):
- These genes decrease in expression
- May represent repressed pathways or lost functions
- Important for understanding treatment mechanisms

### Typical Thresholds

Biologists commonly use:
- **Significance**: padj < 0.05 (sometimes 0.01 for stringent)
- **Fold change**: |log2FC| > 1 (i.e., >2-fold change)
- **Expression filter**: baseMean > 10 (avoid low-count genes)

### Next Steps

1. **Pathway Analysis**: Submit gene lists to:
   - DAVID (https://david.ncifcrf.gov/)
   - Enrichr (https://maayanlab.cloud/Enrichr/)
   - g:Profiler (https://biit.cs.ut.ee/gprofiler/)

2. **Gene Ontology**: Understand biological processes affected

3. **Literature Review**: Research top candidates in PubMed

4. **Validation**: Plan qPCR or Western blots for key findings

5. **Multi-omics Integration**: Combine with proteomics, ChIP-seq, ATAC-seq

## Common Questions

**Q: What fold change is biologically meaningful?**
A: Typically >1.5-2 fold (log2FC > 0.58-1.0), but depends on system. Even small changes in key regulators can be important.

**Q: How many replicates do I need?**
A: Minimum 3 per group for statistical power. 4-6 replicates recommended for reliable detection.

**Q: Should I filter low-count genes?**
A: DESeq2 handles this automatically with independent filtering. Results tables exclude genes with insufficient evidence.

**Q: How do I handle batch effects?**
A: Include `batch` column in samplesheet and specify in contrasts file `blocking` column. DESeq2 will model batch effects.

**Q: Can I compare more than two groups?**
A: This app is optimized for two-group comparisons. For multi-group or complex designs, use the multi-factor use case (coming soon).

## Technical Details

### Pre-configured Parameters

This app uses optimized settings for standard two-group RNA-seq:

- `--features_type gene`: Analyze at gene level (not transcript)
- `--deseq2_test Wald`: Optimal test for two-group comparison
- `--exploratory_clustering_method ward.D2`: Hierarchical clustering
- `--exploratory_cor_method spearman`: Robust correlation
- `--features_id_col gene_id`: Standard gene ID column name
- `--features_name_col gene_name`: Standard gene name column

### Statistical Method: DESeq2

DESeq2 is the field standard for RNA-seq differential expression:
- **Negative binomial model**: Proper handling of count data overdispersion
- **Size factor normalization**: Accounts for library size differences
- **Empirical Bayes shrinkage**: Improves fold change estimates for low-count genes
- **Wald test**: Optimal for two-group comparisons
- **Benjamini-Hochberg FDR**: Controls false discovery rate

### Citations

If you use this analysis, please cite:

1. **nf-core/differentialabundance**: Ewels et al. (2020). Nature Biotechnology.
2. **DESeq2**: Love, Huber & Anders (2014). Genome Biology.
3. **Nextflow**: Di Tommaso et al. (2017). Nature Biotechnology.

## Troubleshooting

### Error: "Sample names don't match"
- Check that `sample` column in samplesheet exactly matches column headers in matrix
- Case-sensitive matching required

### Error: "Not enough replicates"
- DESeq2 requires at least 2 samples per group
- 3+ replicates strongly recommended for reliable results

### Error: "Contrasts not found"
- Verify `reference` and `target` values exist in your condition column
- Check for typos or extra spaces

### Empty results
- Check that your matrix has sufficient counts (not all zeros)
- Verify proper TSV format (tab-separated, not comma)
- Ensure gene_id is first column name

## Version Information

- **Pipeline**: nf-core/differentialabundance v1.5.0
- **Statistical Method**: DESeq2
- **Container System**: Singularity
- **Nextflow**: DSL2

## Support

For issues specific to:
- **This app**: Check TESTING_LOG.md in this directory
- **Pipeline**: https://github.com/nf-core/differentialabundance/issues
- **DESeq2**: https://support.bioconductor.org/

Last updated: 2025-09-30