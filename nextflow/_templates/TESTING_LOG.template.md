# Testing Log: {pipeline-name} - {usecase-name}

**App Name**: {app-name}
**Directory**: `/nextflow/{pipeline}/{usecase}/`
**Created**: YYYY-MM-DD

---

## Test Data Information

**Source**: Where test data came from
- nf-core test dataset: https://...
- Custom test data: Description

**Files**:
- `test_samplesheet.csv` - Description
- Additional files if needed

**Expected Behavior**: What should happen when this test succeeds
- Process completes without errors
- Output files: List expected outputs
- QC metrics: Expected quality thresholds

---

## Attempt 1

**Date/Time**: YYYY-MM-DD HH:MM:SS
**Tester**: Name/identifier

### Preparation
```bash
# Commands used to prepare
camber stash cp test_samplesheet.csv stash://username/test-{pipeline}/
camber stash cp {pipeline}-{usecase}-config.config stash://username/test-{pipeline}/
```

### Execution
```bash
# App creation/update
camber app delete {app-name}  # If updating
camber app create --file app.json

# Test run command
camber app run {app-name} \
  --input input="stash://username/test-{pipeline}/test_samplesheet.csv" \
  --input output="stash://username/test-{pipeline}/results-attempt-1" \
  --input genome="GRCh38"
```

**Job ID**: XXXX

### Monitoring
```bash
# Status checks
camber job get XXXX

# Logs retrieval
camber job logs XXXX > attempt-1-logs.txt
```

### Result
**Status**: PENDING | RUNNING | COMPLETED | FAILED
**Duration**: X hours Y minutes
**Final Job Status**: From `camber job get`

### Output Analysis
**If COMPLETED**:
- ✅ Output files generated: List files
- ✅ QC metrics look reasonable: Summary
- ✅ No errors in logs
- **Conclusion**: Success!

**If FAILED**:
- ❌ Error message: Copy key error from logs
- ❌ Failed at process: Which Nextflow process failed
- ❌ Error type: OutOfMemory | Timeout | File not found | Container issue | etc.

### Error Details
```
[Paste relevant error messages from logs here]
```

### Diagnosis
What we think went wrong and why:
- Analysis of error
- Probable cause
- Related to: config issue | parameter issue | resource issue | data issue | platform issue

### Resolution Attempted
What was changed to fix this:

**Config Changes**:
```groovy
// Before
process {
  withLabel:process_high {
    memory = { 72.GB * task.attempt }
  }
}

// After
process {
  withLabel:process_high {
    memory = { 120.GB * task.attempt }  // Increased for attempt 2
  }
}
```

**app.json Changes**:
- Changed parameter X from Y to Z
- Added missing parameter A

**Other Changes**:
- Modified test data
- Changed command structure
- Adjusted node size

### Files Changed
- [ ] app.json
- [ ] {pipeline}-{usecase}-config.config
- [ ] test_samplesheet.csv
- [ ] README.md

---

## Attempt 2

**Date/Time**: YYYY-MM-DD HH:MM:SS
**Tester**: Name/identifier

**Changes from Attempt 1**: Summary of what was fixed

### Execution
```bash
[Commands used for attempt 2]
```

**Job ID**: YYYY

### Result
**Status**: ...
**Duration**: ...

[Same structure as Attempt 1]

---

## Attempt 3

[Same structure as Attempt 2]

---

## Attempt 4

[Same structure as Attempt 2]

---

## Attempt 5

[Same structure as Attempt 2]

**Final Status**: ✅ Working | ❌ Failed after 5 attempts

---

## Final Outcome

### ✅ If Working

**Success Confirmed**: YYYY-MM-DD

**Final Configuration**:
- Node size: {size}
- Key parameters: List final parameter values
- Critical config settings: Highlight what made it work

**Output Validation**:
- Files generated: Complete list
- QC passed: Yes/No with metrics
- Results scientifically meaningful: Yes/No

**Performance Metrics**:
- Runtime: X hours
- CPU utilization: %
- Memory peak: X GB
- Cost estimate: $X (if available)

**Deployment**:
- [ ] Deployed to production
- [ ] Documentation updated
- [ ] STATUS.txt updated to ✅ Working

**Known Limitations**:
- Limitation 1: Description
- Limitation 2: Description

---

### ❌ If Failed After 5 Attempts

**Failure Confirmed**: YYYY-MM-DD

**Root Cause**:
Clear explanation of why this failed and couldn't be resolved

**Attempts Summary**:
1. Attempt 1: Error type - Resolution tried
2. Attempt 2: Error type - Resolution tried
3. Attempt 3: Error type - Resolution tried
4. Attempt 4: Error type - Resolution tried
5. Attempt 5: Error type - Resolution tried

**Blocking Issue**:
- Platform limitation: Description
- Resource constraint: Description
- Pipeline bug: Link to issue
- Container incompatibility: Description
- Other: Description

**Potential Future Solutions**:
- If platform adds feature X
- If pipeline fixes issue Y
- If different approach Z is tried

**Marked as Failed**:
- [ ] STATUS.txt updated to ❌ Failed
- [ ] PIPELINE_STATUS.md updated
- [ ] Reason documented

---

## Lessons Learned

### What Worked
- Approach 1: Description
- Configuration pattern X: Why it was effective
- Testing strategy Y: What helped debug

### What Didn't Work
- Approach A: Why it failed
- Configuration pattern B: Why it caused issues
- Common pitfall C: How to avoid

### Transferable Knowledge
Insights that could help with other apps:
1. Insight 1: Applicable to {other pipelines/use cases}
2. Insight 2: General principle learned
3. Insight 3: Platform-specific behavior discovered

### Recommendations for Similar Apps
If implementing similar use case in different pipeline:
- Do: Recommendation 1
- Don't: Recommendation 2
- Consider: Recommendation 3

---

## Resources Used

### Documentation Consulted
- nf-core docs: Links
- Tool documentation: Links
- Stack Overflow / Forums: Links

### People Consulted
- Person/role: What they helped with

### Time Spent
- Research: X hours
- Implementation: Y hours
- Testing: Z hours
- Debugging: W hours
- **Total**: Sum hours

---

## Appendix

### Configuration Files

**Final app.json** (if different from current):
```json
{
  // Paste final working app.json if it differs from version in directory
}
```

**Final config file** (if different from current):
```groovy
// Paste final working config if it differs from version in directory
```

### Log Files

Store full log files as separate files:
- `attempt-1-logs.txt`
- `attempt-2-logs.txt`
- etc.

### Test Data

Document test data used:
- Source: URL or description
- Size: File sizes
- Characteristics: Important features of test data

---

## Last Updated

**Date**: YYYY-MM-DD
**By**: Name/identifier
**Status**: Testing | Complete | Failed