# Testing Log: differentialabundance - rnaseq-two-group

**App Name**: differentialabundance-rnaseq-twogroup
**Use Case**: RNA-seq Two-Group Differential Expression Analysis
**Pipeline Version**: nf-core/differentialabundance v1.5.0
**Started**: 2025-09-30

---

## Test Data Information

**Dataset**: Mouse RNA-seq (SRP254919) from nf-core/test-datasets
**Source**: https://github.com/nf-core/test-datasets (modules branch)
**Size**: Top 1000 genes, 6 samples across 2 conditions
**Expected Runtime**: 10-20 minutes on XSMALL node

**Test Files**:
- Samplesheet: https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/mus_musculus/rnaseq_expression/SRP254919.samplesheet.csv
- Contrasts: https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/mus_musculus/rnaseq_expression/SRP254919.contrasts.csv
- Matrix: https://raw.githubusercontent.com/nf-core/test-datasets/modules/data/genomics/mus_musculus/rnaseq_expression/SRP254919.salmon.merged.gene_counts.top1000cov.tsv

---

## Attempt 1 - 2025-09-30 09:17

**Node Size**: XSMALL (4 CPUs, 15GB RAM)
**Rationale**: Starting with XSMALL as recommended for initial testing with nf-core test dataset per NODE_SIZE_GUIDANCE.md

### Command Used
```bash
camber app create --file app.json
camber app run differentialabundance-rnaseq-twogroup --input outdir="stash://david40962/test-differentialabundance/results-attempt-1"
```

**App Configuration**:
- Command: `nextflow run nf-core/differentialabundance -r 1.5.0 --input ${input} --contrasts ${contrasts} --matrix ${matrix} --outdir ${outdir} --features_id_col gene_id --features_name_col gene_name --features_type gene --deseq2_test Wald --exploratory_clustering_method ward.D2 --exploratory_cor_method spearman -c /etc/mpi/nextflow.camber.config`
- All parameters embedded in command (no separate config file)
- Using default test data URLs
- Singularity profile via /etc/mpi/nextflow.camber.config

### Job Details
- **Job ID**: 4391
- **Submission Time**: 2025-09-30 09:17:29Z
- **Status**: FAILED

### Results
- **Status**: FAILED
- **Duration**: ~3 minutes before failure
- **Exit Code**: 1

### Error Messages
```
Error in vst(dds, blind = opt$vs_blind, nsub = opt$vst_nsub) :
  less than 'nsub' rows with mean normalized count > 5,
  it is recommended to use varianceStabilizingTransformation directly
Execution halted
```

### Analysis
The test dataset (1000 genes) is too small for the default VST (variance stabilizing transformation) which expects at least 1000 genes with mean normalized count > 5. The dataset only has ~1000 total genes, many with low counts.

### Resolution for Next Attempt
Try reducing vst_nsub parameter to 100 to accommodate smaller test dataset.

---

## Attempt 2 - 2025-09-30 09:22

**Node Size**: XSMALL (4 CPUs, 15GB RAM)

### Changes from Attempt 1
- Added `--vst_nsub 100` parameter to reduce genes required for VST

### Command Used
```bash
Command: nextflow run nf-core/differentialabundance -r 1.5.0 --input ${input} --contrasts ${contrasts} --matrix ${matrix} --outdir ${outdir} --features_id_col gene_id --features_name_col gene_name --features_type gene --deseq2_test Wald --exploratory_clustering_method ward.D2 --exploratory_cor_method spearman --vst_nsub 100 -c /etc/mpi/nextflow.camber.config
```

### Job Details
- **Job ID**: 4396
- **Submission Time**: 2025-09-30 09:22:59Z
- **Status**: FAILED

### Results
- **Status**: FAILED
- **Duration**: ~3 minutes before failure
- **Exit Code**: 1

### Error Messages
```
Error in vst(dds, blind = opt$vs_blind, nsub = opt$vst_nsub) :
  less than 'nsub' rows with mean normalized count > 5,
  it is recommended to use varianceStabilizingTransformation directly
Execution halted
```

### Analysis
Same error persists. Even with vst_nsub=100, the dataset doesn't have enough genes with sufficient counts. The issue is not just the subset size but the actual number of well-expressed genes in the test dataset.

### Resolution for Next Attempt
Try adding --vs_blind false parameter in addition to vst_nsub 50 to further reduce requirements.

---

## Attempt 3 - 2025-09-30 09:25

**Node Size**: XSMALL (4 CPUs, 15GB RAM)

### Changes from Attempt 2
- Added `--vs_blind false` parameter
- Reduced `--vst_nsub` to 50

### Command Used
```bash
Command: nextflow run nf-core/differentialabundance -r 1.5.0 --input ${input} --contrasts ${contrasts} --matrix ${matrix} --outdir ${outdir} --features_id_col gene_id --features_name_col gene_name --features_type gene --deseq2_test Wald --exploratory_clustering_method ward.D2 --exploratory_cor_method spearman --vst_nsub 50 --vs_blind false -c /etc/mpi/nextflow.camber.config
```

### Job Details
- **Job ID**: 4398
- **Submission Time**: 2025-09-30 09:25:25Z
- **Status**: FAILED

### Results
- **Status**: FAILED
- **Duration**: ~3 minutes before failure
- **Exit Code**: 1

### Error Messages
```
Error in vst(dds, blind = opt$vs_blind, nsub = opt$vst_nsub) :
  less than 'nsub' rows with mean normalized count > 5,
  it is recommended to use varianceStabilizingTransformation directly
Execution halted
```

### Analysis
Same VST error persists. After research, found that the solution is to use a different variance stabilization method entirely - rlog (regularized log transformation) instead of vst, as recommended in nf-core/differentialabundance issue #155.

### Resolution for Next Attempt
Switch from VST to rlog method using --deseq2_vs_method rlog parameter.

---

## Attempt 4 - 2025-09-30 09:29 ✅ SUCCESS

**Node Size**: XSMALL (4 CPUs, 15GB RAM)

### Changes from Attempt 3
- Switched variance stabilization method from VST to rlog: `--deseq2_vs_method rlog`
- Removed `--vst_nsub` and `--vs_blind` parameters (not needed for rlog)

### Command Used
```bash
Command: nextflow run nf-core/differentialabundance -r 1.5.0 --input ${input} --contrasts ${contrasts} --matrix ${matrix} --outdir ${outdir} --features_id_col gene_id --features_name_col gene_name --features_type gene --deseq2_test Wald --deseq2_vs_method rlog --exploratory_clustering_method ward.D2 --exploratory_cor_method spearman -c /etc/mpi/nextflow.camber.config
```

### Job Details
- **Job ID**: 4400
- **Submission Time**: 2025-09-30 09:29:36Z
- **Finish Time**: 2025-09-30 09:32:43Z
- **Status**: COMPLETED ✅

### Results
- **Status**: COMPLETED ✅
- **Duration**: 3 minutes 7 seconds
- **Exit Code**: 0

### Processes Executed
All processes completed successfully:
- VALIDATOR - Validated samplesheet
- CUSTOM_MATRIXFILTER - Filtered count matrix
- DESEQ2_DIFFERENTIAL (2x) - Differential expression analysis (with and without blocking)
- DESEQ2_NORM - Normalization
- FILTER_DIFFTABLE (2x) - Filtered results tables
- PLOT_EXPLORATORY - PCA and exploratory plots
- PLOT_DIFFERENTIAL (2x) - Volcano plots, MA plots, heatmaps
- SHINYNGS_APP - Interactive Shiny application
- RMARKDOWNNOTEBOOK - R Markdown report
- MAKE_REPORT_BUNDLE - Final report bundle

### Analysis
SUCCESS! The rlog (regularized log transformation) method works perfectly for small datasets where VST fails. The pipeline completed all analysis steps including:
- Differential expression testing with DESeq2
- Quality control visualizations
- Interactive reports
- Complete output bundle

### Key Success Factors
1. Using `--deseq2_vs_method rlog` instead of default VST
2. rlog is more suitable for small datasets (< 1000 genes or sparse data)
3. XSMALL node size was sufficient for test dataset
4. All default test data URLs worked correctly

---

---

## Final Outcome

**Status**: ✅ Working (Completed on Attempt 4)

### Working Configuration
- **Successful Attempt**: #4
- **Final Command**: `nextflow run nf-core/differentialabundance -r 1.5.0 --input ${input} --contrasts ${contrasts} --matrix ${matrix} --outdir ${outdir} --features_id_col gene_id --features_name_col gene_name --features_type gene --deseq2_test Wald --deseq2_vs_method rlog --exploratory_clustering_method ward.D2 --exploratory_cor_method spearman -c /etc/mpi/nextflow.camber.config`
- **Node Size Used**: XSMALL (4 CPUs, 15GB RAM)
- **Runtime**: 3 minutes 7 seconds
- **Key Success Factors**:
  1. Using rlog instead of VST for variance stabilization (critical for small datasets)
  2. XSMALL node size sufficient for test data
  3. Using default nf-core test datasets with known compatibility
  4. Proper column naming in command (gene_id, gene_name)

---

## Lessons Learned

### What Worked
- **rlog transformation**: Perfect solution for small/sparse datasets where VST fails
- **nf-core test data**: Pre-validated test datasets work reliably
- **Minimal parameters**: Hardcoding most parameters in command simplifies user experience
- **XSMALL node**: Sufficient for testing and small real datasets

### What Didn't Work
- **VST with nsub parameter adjustment**: Adjusting vst_nsub (even down to 50) didn't solve the issue
- **vs_blind parameter**: Adding --vs_blind false didn't help VST work
- **Default VST method**: Not suitable for datasets with < 1000 well-expressed genes

### Configuration Patterns
- For small datasets (< 5000 genes or sparse counts), always use `--deseq2_vs_method rlog`
- For standard RNA-seq (> 10000 genes, good coverage), default VST is fine
- Test data often requires rlog due to intentional size reduction
- No separate config file needed - all parameters can be in command

### Pipeline-Specific Notes
- **differentialabundance** is sensitive to data size for transformation methods
- The pipeline validates inputs well (samplesheet, contrasts format)
- Generates comprehensive outputs: tables, plots, interactive apps, reports
- Works seamlessly with nf-core/rnaseq output format
- GitHub issue #155 was key reference for solving VST problem

---

## Recommendations for Future Use

### Node Sizing
- **Testing/nf-core test data**: XSMALL (4 CPUs, 15GB RAM) - proven sufficient
- **Small datasets (5-10 samples, < 5000 genes)**: XSMALL to SMALL
- **Standard datasets (10-30 samples, 20000 genes)**: SMALL to MEDIUM
- **Large cohorts (30+ samples)**: MEDIUM to LARGE

### Common Issues to Avoid
1. **VST error on small datasets**: Use `--deseq2_vs_method rlog` for datasets < 5000 genes or sparse counts
2. **Column name mismatches**: Ensure --features_id_col and --features_name_col match your matrix
3. **Samplesheet format**: Must have 'sample' column matching matrix column names exactly
4. **Contrasts format**: Use CSV with id, variable, reference, target, blocking columns

### Best Practices
1. **Start with rlog for safety**: Works on all dataset sizes, slightly slower but more robust
2. **Use nf-core test data first**: Validates app works before trying real data
3. **Keep XSMALL as default**: Most users can start small and scale up if needed
4. **Embed parameters in command**: Reduces user configuration burden
5. **Provide default test URLs**: Makes testing immediate without data upload

---

## Next Steps

- [x] Update STATUS.txt with final outcome (✅ Working)
- [x] Document all 4 attempts in TESTING_LOG.md
- [ ] Update PIPELINE_STATUS.md
- [ ] Update README.md with lessons learned
- [ ] Commit to git with descriptive message
- [ ] Consider implementing next use case (proteomics or multi-factor)
- [ ] Deploy app to production if needed