# nf-core Pipeline Implementation Templates

This directory contains standardized templates for implementing Camber apps from nf-core pipelines.

## Purpose

These templates ensure:
- **Consistency** across all pipeline implementations
- **Complete documentation** of every attempt, success, and failure
- **Knowledge sharing** through detailed logs
- **Reproducibility** of the implementation process
- **Easy onboarding** for new contributors

## Available Templates

### Core Templates

| Template | Purpose | When to Use |
|----------|---------|-------------|
| **QUICK_START.md** | Step-by-step guide for implementing an app | Read this first! Complete workflow from research to testing |
| **PIPELINE_STATUS.template.md** | Track overall pipeline progress | Create once per pipeline at start of research phase |
| **USE_CASES.template.md** | Document identified use cases | Create once per pipeline during research phase |
| **TESTING_LOG.template.md** | Track all test attempts for an app | Create once per use case at start of implementation |
| **README.template.md** | User-facing documentation for an app | Create once per use case during implementation |

### Supporting Templates (To Be Added)

| Template | Purpose | Status |
|----------|---------|--------|
| app.template.json | Skeleton app.json with all required fields | 🔲 Todo |
| config.template.config | Skeleton Nextflow config | 🔲 Todo |

## Template Usage Workflow

```
Start New Pipeline
  ↓
Copy PIPELINE_STATUS.template.md → {pipeline}/PIPELINE_STATUS.md
Copy USE_CASES.template.md → {pipeline}/USE_CASES.md
Research & Document Use Cases
  ↓
For Each Use Case:
  ↓
  Create {usecase}/ directory
  Copy TESTING_LOG.template.md → {usecase}/TESTING_LOG.md
  Copy README.template.md → {usecase}/README.md
  Create app.json (no template yet, see examples)
  Create config.config (no template yet, see examples)
  ↓
  Test (up to 5 attempts, documenting in TESTING_LOG.md)
  ↓
  ✅ Success → Update all docs, commit
  or
  ❌ Failed → Document reason, mark as failed, commit
```

## Quick Start

**New to implementing nf-core apps?**

1. **Read**: `QUICK_START.md` (comprehensive guide)
2. **Read**: `/NEXTFLOW-DEVELOPMENT.md` (patterns and best practices)
3. **Read**: `/nextflow/PIPELINE_IMPLEMENTATION_PLAN.md` (overall strategy)
4. **Study**: Working examples in `/nextflow/scrnaseq/` or `/nextflow/sarek/`
5. **Start**: Choose a Tier 1 pipeline from PIPELINE_IMPLEMENTATION_PLAN.md
6. **Follow**: QUICK_START.md step-by-step

## Template Customization

### How to Use Templates

1. **Copy** the template to appropriate location
2. **Search and replace** all `{placeholders}` with actual values:
   - `{pipeline-name}` → actual pipeline name (e.g., `chipseq`)
   - `{usecase-name}` → actual use case (e.g., `transcription-factor-narrow`)
   - `{app-name}` → actual app name (e.g., `chipseq-tf-narrow`)
   - `YYYY-MM-DD` → actual date
   - etc.
3. **Fill in** all sections marked with instructions or examples
4. **Delete** any sections not applicable (e.g., optional parameters if none exist)

### Placeholder Convention

Templates use this convention:
- `{placeholder}` - Replace with actual value
- `{placeholder1|placeholder2}` - Choose one option
- `[description]` - Replace with specific description
- `YYYY-MM-DD` - Replace with actual date
- `X`, `Y`, `Z` - Replace with actual numbers

## File Organization

### Per Pipeline

```
nextflow/{pipeline}/
├── PIPELINE_STATUS.md        ← From PIPELINE_STATUS.template.md
├── USE_CASES.md               ← From USE_CASES.template.md
├── IMPLEMENTATION_LOG.md      ← High-level notes (no template)
│
└── {usecase}/
    ├── app.json
    ├── {pipeline}-{usecase}-config.config
    ├── test_samplesheet.csv
    ├── README.md              ← From README.template.md
    ├── TESTING_LOG.md         ← From TESTING_LOG.template.md
    ├── STATUS.txt             ← Simple status indicator
    └── attempt-N-logs.txt     ← Log files from test runs
```

## Documentation Standards

### Required Documentation

Every app implementation MUST have:

1. **Complete README.md** - User-facing guide
   - Clear input requirements
   - Samplesheet format with examples
   - Expected outputs
   - Testing instructions

2. **Complete TESTING_LOG.md** - Developer reference
   - All attempts documented
   - Error messages captured
   - Resolutions tried
   - Final outcome with rationale

3. **Updated PIPELINE_STATUS.md** - Overall tracking
   - Progress on all use cases
   - Common issues
   - Statistics

### Documentation Quality Criteria

**Good documentation**:
- ✅ Can someone reproduce your work from your logs?
- ✅ Are errors and solutions clearly explained?
- ✅ Is the target audience (biologists) clearly addressed?
- ✅ Are biological motivations explained?
- ✅ Are all files tracked in git?

**Poor documentation**:
- ❌ Missing error messages or logs
- ❌ Vague descriptions ("it didn't work")
- ❌ No rationale for decisions
- ❌ Technical jargon without explanations
- ❌ Incomplete testing logs

## Status Indicators

Use these consistent status indicators across all files:

### App Status (STATUS.txt and PIPELINE_STATUS.md)

| Indicator | Meaning | Description |
|-----------|---------|-------------|
| 🔲 | Not Started | Use case identified but not yet implemented |
| 🔄 | In Progress | Implementation started, testing ongoing |
| ⚠️ | Issues | Working but with known limitations or warnings |
| ✅ | Working | Tested successfully, deployed or ready to deploy |
| ❌ | Failed | 5 attempts exhausted, marked as failed with reason |

### Testing Status (in TESTING_LOG.md)

| Status | Meaning |
|--------|---------|
| PENDING | Job created, waiting to start |
| RUNNING | Job executing |
| COMPLETED | Job finished successfully |
| FAILED | Job finished with errors |

## Common Pitfalls

### Documentation Pitfalls

1. **Incomplete error logs** - Always save full logs, not just snippets
2. **Missing attempt details** - Document every attempt, even "quick fixes"
3. **Vague resolutions** - Be specific about what was changed and why
4. **Inconsistent updates** - Update STATUS files after each major change
5. **No lessons learned** - Capture insights for future use

### Implementation Pitfalls

1. **Skipping research phase** - Don't implement without clear use case
2. **Too many changes at once** - Change one thing per test attempt
3. **Ignoring working examples** - Start from scrnaseq/sarek patterns
4. **Exposing too many parameters** - Remember: 3-5 parameters max
5. **Technical descriptions** - Write for biologists, not bioinformaticians

## Examples

### Good Examples to Study

**Well-documented implementations**:
- `/nextflow/scrnaseq/` - Comprehensive example with multiple apps
- `/nextflow/sarek/` - Variant calling with different use cases

**What makes them good**:
- Clear biological motivation
- Complete samplesheet documentation
- Biology-focused language
- Working test data
- Reasonable resource allocations

### Template Usage Examples

See `QUICK_START.md` for complete examples of:
- Creating PIPELINE_STATUS.md from template
- Documenting use cases in USE_CASES.md
- Filling out TESTING_LOG.md through multiple attempts
- Writing user-friendly README.md

## Continuous Improvement

### Updating Templates

Templates should be updated when:
- Common patterns emerge across multiple implementations
- Better practices are discovered
- Feedback from users suggests improvements
- New requirements are identified

### Suggesting Changes

If you find these templates could be improved:
1. Document your suggestion
2. Show example of improvement
3. Discuss with team
4. Update template
5. Consider updating existing docs to match

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-09-30 | 1.0 | Initial template set created |

## Related Documentation

- `/NEXTFLOW-DEVELOPMENT.md` - Comprehensive development guide
- `/nextflow/PIPELINE_IMPLEMENTATION_PLAN.md` - Overall strategy and pipeline list
- `/python/DEVELOPMENT.md` - Python app development (different pattern)

## Questions & Support

**For questions about**:
- **Template usage**: See QUICK_START.md
- **Implementation patterns**: See NEXTFLOW-DEVELOPMENT.md
- **Specific pipelines**: Check existing implementations
- **Biological use cases**: Consult domain experts or literature

---

## Quick Reference Card

### New Pipeline Checklist

- [ ] Create `{pipeline}/` directory
- [ ] Copy PIPELINE_STATUS.template.md → PIPELINE_STATUS.md
- [ ] Copy USE_CASES.template.md → USE_CASES.md
- [ ] Research pipeline and identify 5-15 use cases
- [ ] Prioritize use cases (P0-P3)
- [ ] Update PIPELINE_STATUS.md with use case list

### New Use Case Checklist

- [ ] Create `{pipeline}/{usecase}/` directory
- [ ] Copy TESTING_LOG.template.md → TESTING_LOG.md
- [ ] Copy README.template.md → README.md
- [ ] Create app.json with biology-focused content
- [ ] Create config.config based on working examples
- [ ] Create test_samplesheet.csv
- [ ] Test (up to 5 attempts)
- [ ] Update all documentation
- [ ] Update PIPELINE_STATUS.md
- [ ] Commit to git

### Testing Checklist (Per Attempt)

- [ ] Upload test files to stash
- [ ] Create/update app on Camber
- [ ] Run test and note Job ID
- [ ] Monitor job status
- [ ] Get logs when complete
- [ ] Save logs to attempt-N-logs.txt
- [ ] Document in TESTING_LOG.md
- [ ] If failed: diagnose, plan fix, try again
- [ ] If succeeded: complete docs, deploy
- [ ] Update STATUS.txt and PIPELINE_STATUS.md
- [ ] Commit changes

---

Remember: **Complete documentation is more valuable than perfect code**. Someone can fix broken code, but they can't reproduce or learn from undocumented attempts.