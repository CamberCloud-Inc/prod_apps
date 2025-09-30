# Quick Reference: nf-core Pipeline Implementation

One-page reference for implementing nf-core pipeline apps.

---

## Essential Documents

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `_templates/QUICK_START.md` | Complete step-by-step guide | **START HERE** if new |
| `NEXTFLOW-DEVELOPMENT.md` | Patterns and best practices | Before implementing |
| `PIPELINE_IMPLEMENTATION_PLAN.md` | Pipeline list and use cases | Choose pipeline |
| `IMPLEMENTATION_SUMMARY.md` | Overview and philosophy | Understand strategy |

---

## Quick Commands

### Start New Pipeline
```bash
cd /Users/david/git/prod_apps/nextflow
mkdir -p {pipeline}
cd {pipeline}
cp ../_templates/PIPELINE_STATUS.template.md ./PIPELINE_STATUS.md
cp ../_templates/USE_CASES.template.md ./USE_CASES.md
# Edit templates, research use cases
```

### Start New Use Case
```bash
cd /Users/david/git/prod_apps/nextflow/{pipeline}
mkdir -p {usecase}
cd {usecase}
cp ../../_templates/TESTING_LOG.template.md ./TESTING_LOG.md
cp ../../_templates/README.template.md ./README.md
# Create app.json, config.config, test_samplesheet.csv
```

### Test App
```bash
# Upload
camber stash cp test_samplesheet.csv stash://username/test-{pipeline}/
camber stash cp {pipeline}-{usecase}-config.config stash://username/test-{pipeline}/

# Create/Update
camber app create --file app.json
# OR
camber app delete {app-name} && camber app create --file app.json

# Run
camber app run {app-name} \
  --input input="stash://username/test-{pipeline}/test_samplesheet.csv" \
  --input output="stash://username/test-{pipeline}/results-attempt-N" \
  --input genome="GRCh38"

# Monitor (note Job ID from above)
camber job get {job-id}

# Get logs
camber job logs {job-id} > attempt-N-logs.txt
```

### Git Workflow
```bash
# Start
git checkout -b pipeline/{pipeline-name}

# Commit after each attempt
git add .
git commit -m "pipeline/{pipeline}: {action} - {detail}"

# When done
git checkout main
git merge pipeline/{pipeline-name}
git push
```

---

## File Checklist

### Per Pipeline
- [ ] `PIPELINE_STATUS.md` - Overall progress
- [ ] `USE_CASES.md` - Identified use cases
- [ ] `IMPLEMENTATION_LOG.md` - High-level notes
- [ ] `{usecase}/` directories for each app

### Per Use Case (App)
- [ ] `app.json` - Camber app config
- [ ] `{pipeline}-{usecase}-config.config` - Nextflow config
- [ ] `test_samplesheet.csv` - Test data
- [ ] `README.md` - User documentation
- [ ] `TESTING_LOG.md` - All test attempts
- [ ] `STATUS.txt` - Current status (✅/❌/⚠️/🔄/🔲)
- [ ] `attempt-N-logs.txt` - Log files (at least 1)

---

## Status Indicators

| Symbol | Meaning | Use In |
|--------|---------|--------|
| 🔲 | Not Started | PIPELINE_STATUS.md, STATUS.txt |
| 🔄 | In Progress | PIPELINE_STATUS.md, STATUS.txt |
| ⚠️ | Working with Issues | PIPELINE_STATUS.md, STATUS.txt |
| ✅ | Working | PIPELINE_STATUS.md, STATUS.txt |
| ❌ | Failed (5 attempts) | PIPELINE_STATUS.md, STATUS.txt |

---

## app.json Template (Minimal)

```json
{
  "name": "{pipeline}-{usecase}",
  "title": "{Biology-Focused Title}",
  "description": "{Plain language description for biologists}",
  "content": "<h1>...</h1><h2>What This Analysis Does</h2><p>...</p>...",
  "imageUrl": "https://raw.githubusercontent.com/nf-core/{pipeline}/master/docs/images/{pipeline}_logo.png",
  "command": "nextflow run nf-core/{pipeline} --input ${input} --outdir ${output} --genome ${genome} --param value -r X.Y.Z -c /etc/mpi/nextflow.camber.config -c {pipeline}-{usecase}-config.config",
  "engineType": "NEXTFLOW",
  "jobConfig": [{
    "type": "Select",
    "label": "System Size",
    "name": "system_size",
    "hidden": true,
    "options": [
      {"label": "Small", "value": "small", "mapValue": {"nodeSize": "SMALL", "numNodes": 1, "withGpu": false}},
      {"label": "Large (Recommended)", "value": "large", "mapValue": {"nodeSize": "LARGE", "numNodes": 1, "withGpu": false}}
    ],
    "defaultValue": "large"
  }],
  "spec": [
    {"type": "Stash File", "label": "Sample Information Sheet", "name": "input", "description": "CSV with columns: ...", "required": true},
    {"type": "Stash File", "label": "Output Directory", "name": "output", "defaultValue": "./results", "required": true},
    {"type": "Select", "label": "Reference Genome", "name": "genome", "defaultValue": "GRCh38", "options": [...]}
  ]
}
```

---

## config.config Template (Minimal)

```groovy
// Process Resources
process {
  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
    time   = { 8.h   * task.attempt }
  }

  // Process-specific overrides
  withName:'.*:PROCESS_NAME.*' {
    memory = { 48.GB * task.attempt }
  }
}

// Container Configuration (CRITICAL)
singularity {
  enabled = true
  autoMounts = true
}

docker {
  enabled = false  // Must be false on Camber
}

// Use-Case Parameters (hardcode everything)
params {
  parameter1 = 'value1'
  skip_tools = 'tool1,tool2'
}
```

---

## Common Errors & Fixes

| Error | Fix |
|-------|-----|
| docker: command not found | `docker.enabled = false` + `singularity.enabled = true` in config |
| OutOfMemoryError | Increase `memory` in config or use larger node size |
| File not found | Check samplesheet paths, verify stash upload |
| Process timeout | Increase `time` in config |
| Parameter validation failed | Check parameter names match pipeline schema |

---

## Testing Protocol

1. **Attempt 1**: Run with test data
2. **If Failed**: Diagnose error, fix ONE thing
3. **Attempt 2**: Run again
4. **If Failed**: Diagnose, fix ONE thing
5. **Attempt 3-5**: Continue pattern
6. **After 5 Attempts**:
   - ✅ If working: Complete docs, deploy, commit
   - ❌ If failed: Document reason, mark failed, commit, move on

**Key**: Document EVERY attempt in TESTING_LOG.md

---

## Biology-Focused Writing

### Titles
- ✅ "Cancer Variant Detection: Tumor vs Normal"
- ❌ "Sarek: Somatic Variant Calling Pipeline"

### Descriptions
- ✅ "Identify cancer-specific mutations by comparing tumor to normal tissue"
- ❌ "Uses GATK Mutect2 for somatic variant detection"

### Parameters
- ✅ "Sample Information Sheet - CSV listing tumor and normal samples"
- ❌ "Input - Samplesheet following nf-core schema"

### Samplesheet Instructions
- ✅ Show exact CSV format with examples
- ✅ Explain every column in detail
- ✅ Include valid values and constraints
- ❌ Just say "follow nf-core format"

---

## Priority Order

### Start Here (Tier 1)
1. **chipseq** - No existing implementation, high priority
2. **cutandrun** - Low-input ChIP alternative
3. **differentialabundance** - RNA-seq downstream
4. **ampliseq** - Microbial community profiling

### Expand These (Already Exist)
5. **sarek** - Add more variant calling use cases
6. **scrnaseq** - Add more single-cell protocols
7. **rnaseq** - Add more RNA-seq variants
8. **atacseq** - Add more accessibility use cases

---

## Time Estimates

| Activity | Solo | Team of 4 |
|----------|------|-----------|
| Research (1 pipeline) | 2-4 hours | 2-4 hours |
| Implement (1 app) | 2-4 hours | 2-4 hours |
| Test (1 app, working) | 1-2 hours | 1-2 hours |
| Test (1 app, debugging) | 4-8 hours | 4-8 hours |
| **Per App Total** | 5-18 hours | 5-18 hours |
| **Tier 1 (65 apps)** | 6-12 months | 6-12 weeks |

---

## Success Criteria

### App is Working When:
- ✅ Test job status = COMPLETED
- ✅ Expected outputs generated
- ✅ No errors in logs
- ✅ Results scientifically meaningful

### App is Failed When:
- ❌ 5 attempts exhausted
- ❌ Reason documented in TESTING_LOG.md
- ❌ STATUS.txt = "❌ Failed"

### Documentation is Complete When:
- ✅ All attempts documented in TESTING_LOG.md
- ✅ README.md has complete user instructions
- ✅ PIPELINE_STATUS.md updated
- ✅ Committed to git

---

## Need Help?

1. **Implementation patterns**: See `NEXTFLOW-DEVELOPMENT.md`
2. **Step-by-step guide**: See `_templates/QUICK_START.md`
3. **Working examples**: See `scrnaseq/`, `sarek/` directories
4. **Pipeline details**: https://nf-co.re/{pipeline}
5. **Community support**: https://nfcore.slack.com

---

## Remember

- **Biology-first**: Write for biologists, not bioinformaticians
- **Hardcode**: Expose only 3-5 parameters
- **Document**: Every attempt, every error, every fix
- **5 attempts max**: Then mark failed and move on
- **Done > Perfect**: 85% success rate is excellent

---

## Quick Decision Tree

```
Starting new pipeline?
  → Read QUICK_START.md
  → Create PIPELINE_STATUS.md and USE_CASES.md
  → Research use cases

Implementing new use case?
  → Copy templates to {usecase}/ directory
  → Create app.json, config, test data
  → Test (up to 5 attempts)

Test failed?
  → Check common errors table above
  → Fix ONE thing
  → Document in TESTING_LOG.md
  → Try again (if <5 attempts)

Test succeeded?
  → Complete all documentation
  → Update PIPELINE_STATUS.md
  → Deploy to production
  → Commit to git
  → Move to next use case

5 attempts exhausted?
  → Document reason in TESTING_LOG.md
  → Mark ❌ Failed in STATUS.txt
  → Update PIPELINE_STATUS.md
  → Commit to git
  → Move to next use case
```

---

**Last Updated**: 2025-09-30
**Status**: Ready for Implementation
**Next**: Begin with chipseq (Tier 1, P0)