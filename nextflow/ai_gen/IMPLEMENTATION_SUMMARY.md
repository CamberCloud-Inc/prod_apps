# nf-core Pipeline Implementation: Summary & Status

**Created**: 2025-09-30
**Purpose**: Systematically implement biologist-friendly Camber apps for all nf-core pipelines

---

## What Was Created

### Core Documentation

1. **PIPELINE_IMPLEMENTATION_PLAN.md** - Master plan
   - Comprehensive list of ~60 nf-core pipelines sorted by priority
   - Detailed use cases for high-priority pipelines (chipseq, cutandrun, etc.)
   - Implementation workflow (Research → Implement → Test → Deploy)
   - 5-attempt testing protocol with failure criteria
   - Parallel work strategies for "swarming"
   - Risk management and success metrics

2. **/_templates/ Directory** - Standardized templates
   - `QUICK_START.md` - Step-by-step guide for new contributors
   - `PIPELINE_STATUS.template.md` - Track pipeline progress
   - `USE_CASES.template.md` - Document identified use cases
   - `TESTING_LOG.template.md` - Record all test attempts
   - `README.template.md` - User-facing documentation
   - `README.md` - Template usage guide

### Existing Documentation Updates

3. **NEXTFLOW-DEVELOPMENT.md** - Enhanced with biology-focused sections
   - Complete guide on writing for biologists (not bioinformaticians)
   - HTML content template for app descriptions
   - Detailed samplesheet instruction patterns
   - Parameter description guidelines
   - Real examples showing biology-focused transformations

4. **python/DEVELOPMENT.md** - Updated for Python apps
   - Added section on using `camber stash cp` and `ls`
   - Test data directory with sample files
   - Complete workflow documentation

5. **python/ML_LEARNING_PLATFORM_PLAN.md** - Created
   - Self-improving ML learning platform concept
   - Progressive learning tracks
   - Meta-learning architecture

---

## Philosophy: One Pipeline → Multiple Focused Apps

**Core Strategy**: Instead of creating one complex app with 50+ parameters, create 10+ simple apps per pipeline, each optimized for a specific biological use case.

### Example: nf-core/sarek

**❌ Old Approach**: One "Sarek" app
- Exposes all tools (GATK, Mutect2, Freebayes, etc.)
- Exposes all parameters (50+ options)
- Users must understand bioinformatics deeply
- Overwhelming and error-prone

**✅ New Approach**: 10 focused apps
1. "Cancer Variant Detection: Tumor vs Normal"
2. "Inherited Genetic Variant Detection"
3. "Structural Variant Detection"
4. "Copy Number Variation Analysis"
5. "Trio Analysis: Family-Based Variant Detection"
6. ...and more

Each app:
- Clear biological purpose
- 3-5 parameters only
- Pre-configured best practices
- Biology-focused documentation
- Complete samplesheet instructions

---

## Key Principles

### 1. Biology-First Language

**Bad (Technical)**:
```
Title: "Sarek: Somatic Variant Calling Pipeline"
Description: "Uses GATK Mutect2 for somatic variant detection with BAM preprocessing"
Input: "Samplesheet following nf-core schema"
```

**Good (Biology-Focused)**:
```
Title: "Cancer Variant Detection: Tumor vs Normal Comparison"
Description: "Identify cancer-specific genetic mutations by comparing tumor tissue to matched normal tissue. Detects SNVs and small indels present in cancer cells but not in healthy cells."
Input: "CSV file listing tumor and normal samples. Required columns: patient, sample, status (0=normal, 1=tumor), lane, fastq_1, fastq_2. Each patient must have one normal and one tumor sample."
```

### 2. Complete Input Instructions

Every app must include:
- Exact CSV format with example data
- Explanation of every column
- Where to find information (e.g., "lane number is in your FASTQ filename")
- Valid values and constraints
- Common mistakes to avoid

### 3. Hardcode Everything Possible

**Always Hardcode**:
- Pipeline version
- Tool selection (use best practice tool)
- Quality thresholds
- Algorithm parameters
- File formats
- Technical settings

**Expose to Users** (only 3-5 parameters):
- Input data (samplesheet)
- Output directory
- Reference genome
- Key biological parameters (e.g., expected cell count)

### 4. Extensive Documentation

Every app must have:
- **README.md** - User-facing guide with complete instructions
- **TESTING_LOG.md** - Developer reference with all attempts
- **PIPELINE_STATUS.md** - Overall pipeline progress
- **STATUS.txt** - Quick status indicator

### 5. Five-Attempt Protocol

- Test each app up to 5 times
- Document every attempt in TESTING_LOG.md
- If working within 5 attempts: Mark ✅ Working
- If still failing after 5 attempts: Mark ❌ Failed with clear reason
- Move on - don't get stuck

---

## Pipeline Priority Tiers

### Tier 1: High-Priority Genomics (Start Here)

| Pipeline | Status | Apps Planned | Priority |
|----------|--------|--------------|----------|
| rnaseq | ✅ Exists | 8 apps | P0 |
| sarek | ✅ Exists | 10 apps | P0 |
| scrnaseq | ✅ Exists | 10 apps | P0 |
| chipseq | 🔲 Todo | 6 apps | P0 |
| atacseq | ✅ Exists | 5 apps | P0 |
| methylseq | ✅ Exists | 4 apps | P1 |
| cutandrun | 🔲 Todo | 4 apps | P1 |
| differentialabundance | 🔲 Todo | 4 apps | P1 |

**Target**: 90%+ success rate

### Tier 2: Specialized Genomics

| Pipeline | Apps Planned |
|----------|--------------|
| ampliseq | 3 apps |
| nanoseq | 4 apps |
| crisprseq | 3 apps |
| mag | 3 apps |
| viralrecon | 3 apps |
| taxprofiler | 3 apps |
| rnafusion | 3 apps |
| smrnaseq | 3 apps |

**Target**: 75%+ success rate

### Tier 3-7: Specialized & Emerging

30+ additional pipelines across:
- Structural & Long-Read genomics
- Proteomics & Metabolomics
- Spatial & Imaging
- Specialized applications
- Other scientific fields

**Target**: 50%+ success rate (more experimental)

---

## Implementation Workflow

### Phase 1: Research (Per Pipeline)

1. Clone pipeline: `git clone https://github.com/nf-core/{pipeline}.git`
2. Review documentation: README, usage docs, parameter schema
3. Create directory: `mkdir nextflow/{pipeline}`
4. Copy templates: `PIPELINE_STATUS.md`, `USE_CASES.md`
5. Research use cases (literature, Slack, GitHub issues)
6. Document 5-15 use cases with biological context
7. Prioritize use cases

**Output**: Complete `USE_CASES.md` with prioritized use cases

### Phase 2: Implementation (Per Use Case)

1. Create directory: `{pipeline}/{usecase}/`
2. Create config file based on working examples
3. Find/create test data (prefer nf-core test datasets)
4. Create `app.json` with biology-focused content
5. Create `README.md` from template
6. Initialize `TESTING_LOG.md`

**Output**: Complete app directory ready for testing

### Phase 3: Testing (Up to 5 Attempts)

```bash
# Attempt 1
camber stash cp test_samplesheet.csv stash://username/test-{pipeline}/
camber app create --file app.json
camber app run {app-name} --input input="..." --input output="..."
# Monitor: camber job get {job-id}
# Get logs: camber job logs {job-id}
# Document in TESTING_LOG.md

# If failed: diagnose, fix, try again (Attempt 2)
# Repeat up to 5 times

# After 5 attempts:
# - If working: Mark ✅, deploy, commit
# - If failed: Mark ❌, document reason, commit, move on
```

**Output**: Working app or documented failure

### Phase 4: Documentation & Deployment

1. Complete all documentation
2. Update `PIPELINE_STATUS.md`
3. Deploy to production (if working)
4. Commit to git with descriptive message
5. Move to next use case

---

## File Organization

```
nextflow/
├── NEXTFLOW-DEVELOPMENT.md              # Development patterns
├── PIPELINE_IMPLEMENTATION_PLAN.md      # This master plan
├── IMPLEMENTATION_SUMMARY.md            # This file
│
├── _templates/                          # Standardized templates
│   ├── README.md                        # Template usage guide
│   ├── QUICK_START.md                   # Step-by-step guide
│   ├── PIPELINE_STATUS.template.md
│   ├── USE_CASES.template.md
│   ├── TESTING_LOG.template.md
│   └── README.template.md
│
├── {pipeline}/                          # Each nf-core pipeline
│   ├── PIPELINE_STATUS.md               # Overall progress
│   ├── USE_CASES.md                     # Identified use cases
│   ├── IMPLEMENTATION_LOG.md            # High-level notes
│   │
│   └── {usecase}/                       # Each use case = one app
│       ├── app.json                     # Camber app config
│       ├── {pipeline}-{usecase}-config.config  # Nextflow config
│       ├── test_samplesheet.csv         # Test data
│       ├── README.md                    # User guide
│       ├── TESTING_LOG.md               # Test attempts
│       ├── STATUS.txt                   # Quick status
│       └── attempt-N-logs.txt           # Log files
│
├── sarek/                               # Example: existing pipeline
│   ├── germline-haplotypecaller/
│   ├── somatic-mutect2/
│   └── ...
│
├── scrnaseq/                            # Example: existing pipeline
│   ├── 10x-v3-standard/
│   ├── dropseq/
│   └── ...
│
└── chipseq/                             # Example: to be implemented
    ├── PIPELINE_STATUS.md               # Create first
    ├── USE_CASES.md                     # Create second
    ├── transcription-factor-narrow/     # Implement first
    ├── histone-marks-broad/             # Implement second
    └── ...
```

---

## Git Workflow

### Branch Strategy

```bash
# Work on a pipeline
git checkout -b pipeline/{pipeline-name}

# Implement use cases, commit frequently
git add nextflow/{pipeline}/{usecase}/
git commit -m "pipeline/{pipeline}: Add {usecase} app - Attempt N"

# When complete
git checkout main
git merge pipeline/{pipeline-name}
git push origin main
```

### Commit Message Convention

```
pipeline/{pipeline}: {action} - {detail}

Examples:
pipeline/chipseq: Research complete - 6 use cases identified
pipeline/chipseq: Add transcription-factor-narrow app
pipeline/chipseq: Fix OOM error in histone-marks-broad (attempt 3)
pipeline/chipseq: Mark differential-binding as failed after 5 attempts
pipeline/chipseq: All apps tested - 5/6 working
```

---

## Parallel Work Strategy ("Swarming")

### Recommended Approach for Teams

**Week 1-2**: Research Phase (Tier 1 Pipelines)
- Create `USE_CASES.md` for all 8 Tier 1 pipelines
- Can be done in parallel (1 person per pipeline)

**Week 3-6**: Implementation & Testing (Tier 1)
- Divide 8 pipelines among team
- Each person implements all use cases for their pipelines
- Test in parallel, share learnings

**Week 7-8**: Tier 2 Pipelines
- Apply lessons learned
- Faster implementation with established patterns

**Week 9-12**: Tier 3-4 Pipelines
- More specialized, lower priority
- Opportunistic implementation

### For Solo Work

1. Start with one use case, complete fully (research → test)
2. Learn from experience
3. Apply to next use case with improved speed
4. Build momentum through successes

---

## Success Metrics

### Per Pipeline
- Number of use cases identified
- Number of apps working / total
- Number of apps failed (with reasons)
- Common issues and resolutions

### Overall Project
- Total pipelines with ≥1 working app
- Total working apps across all pipelines
- Tier 1 completion percentage
- Documentation completeness

### Targets
- **Tier 1**: 90%+ success rate
- **Tier 2**: 75%+ success rate
- **Tier 3+**: 50%+ success rate

---

## Common Issues & Solutions

### Technical Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| docker: command not found | Using Docker on platform without it | Set `docker.enabled = false`, `singularity.enabled = true` |
| OutOfMemoryError | Insufficient memory allocation | Increase process memory or node size |
| File not found | Incorrect samplesheet paths | Verify stash paths, use relative paths |
| Process timeout | Time limit too short | Increase time in config |
| Parameter validation failed | Wrong parameter names | Check against pipeline schema |

### Implementation Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Too complex | Exposed too many parameters | Hardcode more, expose only 3-5 essential params |
| No test data | Pipeline lacks public test data | Create minimal synthetic test data |
| Unclear use case | Not biologically motivated | Research actual use cases in literature |
| Documentation unclear | Written for bioinformaticians | Rewrite for biologists using plain language |

---

## Resources

### Documentation
- `/NEXTFLOW-DEVELOPMENT.md` - Complete development guide
- `/nextflow/PIPELINE_IMPLEMENTATION_PLAN.md` - Detailed plan with use cases
- `/nextflow/_templates/QUICK_START.md` - Step-by-step implementation guide
- `/nextflow/_templates/README.md` - Template usage guide

### Examples
- `/nextflow/scrnaseq/` - Well-documented multi-app pipeline
- `/nextflow/sarek/` - Variant calling examples
- `/nextflow/atacseq/` - ATAC-seq examples

### External Resources
- nf-core pipelines: https://nf-co.re/pipelines
- nf-core Slack: https://nfcore.slack.com
- nf-core GitHub: https://github.com/nf-core/
- Pipeline-specific docs: https://nf-co.re/{pipeline}

---

## Estimated Timeline

### Tier 1 (8 pipelines, ~65 apps)
- Research: 2-4 hours per pipeline = 16-32 hours
- Implementation: 2-4 hours per app = 130-260 hours
- Testing: 1-8 hours per app = 65-520 hours
- **Total**: 211-812 hours

**With team of 4**: 6-12 weeks
**Solo**: 6-12 months (opportunistic)

### Tier 2 (10 pipelines, ~30 apps)
- **Total**: 90-390 hours
- **With team of 4**: 3-6 weeks
- **Solo**: 3-6 months

### All Tiers (60+ pipelines)
- **With team**: 6-12 months for comprehensive coverage
- **Solo**: 2-3 years (but not recommended)

---

## Getting Started

### Immediate Next Steps

1. **Choose Your Starting Point**
   - New to this? Start with chipseq (high-priority, no existing implementation)
   - Want to expand? Pick existing pipeline (sarek, scrnaseq, rnaseq)

2. **Read Documentation**
   - Read: `_templates/QUICK_START.md` (comprehensive guide)
   - Read: `NEXTFLOW-DEVELOPMENT.md` (patterns and best practices)
   - Study: Working examples in `scrnaseq/` or `sarek/`

3. **Begin Research Phase**
   - Create pipeline directory
   - Copy templates
   - Research and document use cases
   - Prioritize

4. **Implement First Use Case**
   - Follow QUICK_START.md step-by-step
   - Document everything
   - Test thoroughly
   - Learn from experience

5. **Share Learnings**
   - Update templates if you find improvements
   - Document common issues
   - Share successful patterns

---

## Questions to Address

**Before starting**:
- [ ] Do I understand the biological use case?
- [ ] Do I have test data?
- [ ] Have I studied working examples?
- [ ] Do I understand the five-attempt protocol?

**During implementation**:
- [ ] Am I documenting every attempt?
- [ ] Is my app.json biology-focused?
- [ ] Are samplesheet instructions complete?
- [ ] Am I hardcoding enough parameters?

**After testing**:
- [ ] Are all documentation files complete?
- [ ] Did I update PIPELINE_STATUS.md?
- [ ] Did I commit to git with clear message?
- [ ] Did I mark status correctly (✅/❌)?

---

## Philosophy Reminder

**Our Goals**:
1. **Accessibility**: Biologists can use these apps without bioinformatics expertise
2. **Completeness**: Every attempt, success, and failure is documented
3. **Reproducibility**: Anyone can reproduce our work from documentation
4. **Learning**: Knowledge is shared and built upon
5. **Progress**: Done is better than perfect; 85% success rate is excellent

**Remember**:
- ✅ Complete documentation > perfect code
- ✅ Biology-focused language > technical accuracy
- ✅ Simple apps for specific use cases > complex apps with all options
- ✅ Progress with learning > perfection with frustration
- ✅ 5 attempts then move on > infinite debugging

---

## Status: Ready to Begin

**Created**: 2025-09-30
**Status**: 📋 Planning Complete, Ready for Implementation
**Next Action**: Begin with Tier 1 pipeline (recommended: chipseq)

**Contributors**: Follow `_templates/QUICK_START.md` to begin!

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2025-09-30 | 1.0 | Initial comprehensive plan created with all templates |