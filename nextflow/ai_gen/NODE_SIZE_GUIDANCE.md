# Node Size Guidance for nf-core Pipelines

**Last Updated**: 2025-09-30

## Default: XSMALL for Testing

**When implementing new apps, always start with XSMALL nodeSize for initial testing with nf-core test datasets.**

---

## Node Size Options

| Size | CPUs | RAM | When to Use |
|------|------|-----|-------------|
| **XXSMALL** | 2 | 8GB | Utility scripts only (not for nf-core pipelines) |
| **XSMALL** | 4 | 15GB | **Testing with nf-core test data** (Default) |
| **SMALL** | 8 | 30GB | Small real datasets (1-3 samples) |
| **MEDIUM** | 32 | 120GB | Standard datasets (5-20 samples) |
| **LARGE** | 64 | 360GB | Large datasets (20-50 samples) |
| **XLARGE** | 96 | 540GB | Very large cohorts (50+ samples) |

---

## Testing Strategy

### Phase 1: Initial Testing (XSMALL)

**Always start here for new app implementations:**

```json
{
  "jobConfig": [
    {
      "type": "Select",
      "label": "System Size",
      "name": "system_size",
      "hidden": true,
      "options": [
        {
          "label": "XSMALL - Testing/nf-core test data",
          "value": "xsmall",
          "mapValue": {"nodeSize": "XSMALL", "numNodes": 1, "withGpu": false}
        }
      ],
      "defaultValue": "xsmall"
    }
  ]
}
```

**Why XSMALL for testing:**
- ✅ Faster to provision (less queue time)
- ✅ Lower cost for repeated testing attempts
- ✅ Sufficient for nf-core test datasets (designed to be small)
- ✅ Quick failure feedback if issues exist
- ✅ Can run multiple tests in parallel without resource contention

### Phase 2: Production Sizing

**After successful XSMALL testing, add appropriate sizes for real data:**

```json
{
  "jobConfig": [
    {
      "options": [
        {"label": "XSMALL - Testing", "value": "xsmall", "mapValue": {"nodeSize": "XSMALL", "numNodes": 1, "withGpu": false}},
        {"label": "SMALL - 1-3 samples", "value": "small", "mapValue": {"nodeSize": "SMALL", "numNodes": 1, "withGpu": false}},
        {"label": "MEDIUM - 5-20 samples", "value": "medium", "mapValue": {"nodeSize": "MEDIUM", "numNodes": 1, "withGpu": false}},
        {"label": "LARGE - 20-50 samples", "value": "large", "mapValue": {"nodeSize": "LARGE", "numNodes": 1, "withGpu": false}}
      ],
      "defaultValue": "xsmall"
    }
  ]
}
```

**Keep XSMALL as default even in production** - users can scale up as needed for their data.

---

## Pipeline-Specific Guidance

### Lightweight Pipelines (XSMALL usually sufficient)

These pipelines often work well even on XSMALL for real data:

- **ampliseq** (16S/ITS) - Small amplicon data
- **taxprofiler** - Taxonomic classification
- **fetchngs** - Data download pipeline
- **bamtofastq** - Format conversion

**Recommendation**: XSMALL default, add SMALL/MEDIUM options

### Standard Pipelines (Start XSMALL, scale to MEDIUM)

Most genomics pipelines fit here:

- **chipseq** - ChIP sequencing
- **atacseq** - Chromatin accessibility
- **cutandrun** - Low-input ChIP alternative
- **methylseq** - DNA methylation
- **smrnaseq** - Small RNA sequencing

**Recommendation**: XSMALL for testing, SMALL/MEDIUM for production

### Memory-Intensive Pipelines (Start XSMALL, scale to LARGE)

These may need more resources for real data:

- **rnaseq** - RNA sequencing (especially many samples)
- **sarek** - Variant calling (WGS)
- **scrnaseq** - Single-cell RNA (many cells)
- **nanoseq** - Long-read sequencing
- **mag** - Metagenome assembly

**Recommendation**: XSMALL for testing, MEDIUM/LARGE for production

### Compute-Intensive Pipelines (May fail on XSMALL)

These might need SMALL even for testing:

- **proteinfold** - AlphaFold protein structure prediction
- **viralrecon** - Viral genome reconstruction (depends on coverage)
- **rnafusion** - Gene fusion detection
- **spatialvi** - Spatial transcriptomics

**Recommendation**: Try XSMALL first; if OOM, use SMALL for testing

---

## Troubleshooting Node Size Issues

### Issue: OutOfMemoryError on XSMALL

**Solution**:
1. For testing: Increase to SMALL
2. For production: Use MEDIUM or LARGE
3. Update jobConfig options to include larger sizes

### Issue: Process Timeout on XSMALL

**Solution**:
1. XSMALL may be too slow for some pipelines
2. Increase to SMALL or MEDIUM
3. Or add `--max_cpus` parameter to command to request more cores

### Issue: Test Data Works on XSMALL, Real Data Fails

**Expected behavior!** This is why we test on XSMALL:
1. Validates pipeline logic with fast/cheap testing
2. Then scale up for production workloads
3. Add appropriate size options in jobConfig

---

## Testing Protocol with XSMALL

### Attempt 1: XSMALL with nf-core test data

```bash
# In app.json, set defaultValue to "xsmall"
camber app create --file app.json

# Run test
camber app run {app-name} \
  --input input="stash://username/test-{pipeline}/test_samplesheet.csv" \
  --input outdir="stash://username/test-{pipeline}/results-attempt-1"

# Monitor
camber job get {job-id}
```

**Outcomes**:
- ✅ **COMPLETED**: Great! App works on minimal resources. Document and proceed.
- ❌ **FAILED (OutOfMemoryError)**: Expected for some pipelines. Try Attempt 2 with SMALL.
- ❌ **FAILED (Other error)**: Debug the error, fix app.json/command, retry on XSMALL.

### Attempt 2 (if OOM): SMALL

```bash
# Update app.json: Change defaultValue to "small"
# Or add --max_memory parameter to command

camber app delete {app-name}
camber app create --file app.json

# Retry
camber app run {app-name} ...
```

---

## App.json Template with XSMALL Default

**Standard template for all new apps**:

```json
{
  "name": "{pipeline}-{usecase}",
  "command": "nextflow run nf-core/{pipeline} --input ${input} --outdir ${outdir} --param1 value -r X.Y.Z -profile singularity",
  "engineType": "NEXTFLOW",
  "jobConfig": [
    {
      "type": "Select",
      "label": "System Size",
      "name": "system_size",
      "hidden": true,
      "description": "Select compute resources. Start with XSMALL for testing, scale up for production data.",
      "options": [
        {
          "label": "XSMALL (4 CPUs, 15GB RAM) - Testing/nf-core test data",
          "value": "xsmall",
          "mapValue": {"nodeSize": "XSMALL", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "SMALL (8 CPUs, 30GB RAM) - Small datasets (1-3 samples)",
          "value": "small",
          "mapValue": {"nodeSize": "SMALL", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "MEDIUM (32 CPUs, 120GB RAM) - Standard datasets (5-20 samples)",
          "value": "medium",
          "mapValue": {"nodeSize": "MEDIUM", "numNodes": 1, "withGpu": false}
        },
        {
          "label": "LARGE (64 CPUs, 360GB RAM) - Large datasets (20-50 samples)",
          "value": "large",
          "mapValue": {"nodeSize": "LARGE", "numNodes": 1, "withGpu": false}
        }
      ],
      "defaultValue": "xsmall"
    }
  ]
}
```

---

## Cost and Time Considerations

### XSMALL Benefits for Testing

| Metric | XSMALL | MEDIUM | LARGE |
|--------|--------|--------|-------|
| **Provision time** | ~30 sec | ~2 min | ~5 min |
| **Cost per hour** | $0.XX | $X.XX | $XX.XX |
| **Test iterations** | More attempts | Fewer attempts | Very few |
| **Parallel tests** | Many | Some | Limited |

**For 5 testing attempts**:
- XSMALL: Fast feedback, low cost, can run multiple apps in parallel
- MEDIUM: Slower feedback, higher cost, limits parallel testing
- LARGE: Very slow/expensive, should only use after validation

---

## Documentation Requirements

### In TESTING_LOG.md

Document why you chose each node size:

```markdown
## Attempt 1 - XSMALL (4 CPUs, 15GB RAM)

**Rationale**: Starting with XSMALL for initial testing with nf-core test dataset.

**Result**: FAILED - OutOfMemoryError in FASTQC process

## Attempt 2 - SMALL (8 CPUs, 30GB RAM)

**Rationale**: Increased from XSMALL due to OOM error in Attempt 1.

**Result**: COMPLETED - Test successful on SMALL node.

## Recommendation

- Testing: SMALL minimum
- Production (1-10 samples): MEDIUM
- Production (10+ samples): LARGE
```

### In README.md

Provide clear guidance on node size selection:

```markdown
## Resource Requirements

**Recommended Node Size**:

| Dataset Size | Node Size | Specs | Runtime Estimate |
|--------------|-----------|-------|------------------|
| nf-core test data | XSMALL | 4 CPU, 15GB RAM | 10-20 min |
| 1-3 samples | SMALL | 8 CPU, 30GB RAM | 1-2 hours |
| 5-20 samples | MEDIUM | 32 CPU, 120GB RAM | 2-6 hours |
| 20-50 samples | LARGE | 64 CPU, 360GB RAM | 6-24 hours |

**Note**: Always start with XSMALL for initial testing. Scale up based on your data size.
```

---

## Summary

1. **Always start with XSMALL** for initial app implementation and testing
2. **Use nf-core test datasets** which are designed to work on small resources
3. **Scale up as needed** based on actual resource usage
4. **Keep XSMALL as default** in production apps - users can select larger sizes
5. **Document node size decisions** in TESTING_LOG.md with rationale
6. **Test on XSMALL is cheap and fast** - enables rapid iteration and parallel testing

**Remember**: The goal is to validate the app works correctly, not to optimize performance. XSMALL achieves this faster and cheaper than larger nodes.