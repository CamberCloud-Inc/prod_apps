# Nextflow nf-core Pipeline Apps

Biologist-friendly Camber applications built from nf-core pipelines.

---

## 📚 Documentation Index

### Start Here

| Document | Description | Audience |
|----------|-------------|----------|
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | One-page cheat sheet | Everyone |
| **[_templates/QUICK_START.md](_templates/QUICK_START.md)** | Complete step-by-step guide | New contributors |
| **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** | Project overview and philosophy | Everyone |

### Planning & Strategy

| Document | Description | Audience |
|----------|-------------|----------|
| **[PIPELINE_IMPLEMENTATION_PLAN.md](PIPELINE_IMPLEMENTATION_PLAN.md)** | Master plan with all pipelines | Project managers, contributors |
| **[NEXTFLOW-DEVELOPMENT.md](../NEXTFLOW-DEVELOPMENT.md)** | Development patterns and best practices | Developers |
| **[_templates/README.md](_templates/README.md)** | Template usage guide | Contributors |

### Templates

All templates are in `_templates/` directory:
- `PIPELINE_STATUS.template.md` - Track pipeline progress
- `USE_CASES.template.md` - Document use cases
- `TESTING_LOG.template.md` - Record test attempts
- `README.template.md` - User documentation
- `QUICK_START.md` - Step-by-step implementation guide

---

## 🗂️ Pipeline Directory Structure

```
nextflow/
├── README.md                            ← You are here
├── QUICK_REFERENCE.md                   ← Cheat sheet
├── IMPLEMENTATION_SUMMARY.md            ← Project overview
├── PIPELINE_IMPLEMENTATION_PLAN.md      ← Master plan
├── NEXTFLOW-DEVELOPMENT.md              ← Development guide
│
├── _templates/                          ← Standardized templates
│   ├── README.md                        ← Template guide
│   ├── QUICK_START.md                   ← Step-by-step guide
│   ├── PIPELINE_STATUS.template.md
│   ├── USE_CASES.template.md
│   ├── TESTING_LOG.template.md
│   └── README.template.md
│
├── {pipeline}/                          ← Each nf-core pipeline
│   ├── PIPELINE_STATUS.md               ← Progress tracking
│   ├── USE_CASES.md                     ← Identified use cases
│   ├── IMPLEMENTATION_LOG.md            ← High-level notes
│   │
│   └── {usecase}/                       ← Each app (use case)
│       ├── app.json                     ← Camber config
│       ├── {pipeline}-{usecase}-config.config
│       ├── test_samplesheet.csv
│       ├── README.md                    ← User guide
│       ├── TESTING_LOG.md               ← Test history
│       ├── STATUS.txt                   ← Current status
│       └── attempt-N-logs.txt           ← Log files
│
└── ... (more pipelines)
```

---

## 📊 Current Status

### Existing Pipelines (Expand)

| Pipeline | Apps | Status | Next Steps |
|----------|------|--------|------------|
| **scrnaseq** | 1 comprehensive | ✅ Working | Add more 10x variants, other protocols |
| **sarek** | 1 general | ✅ Working | Split into germline, somatic, SV, CNV apps |
| **rnaseq** | 1 general | ✅ Working | Add small RNA, long-read, fusion variants |
| **atacseq** | 2 variants | ✅ Working | Add more chromatin accessibility use cases |
| **methylseq** | 2 variants | ✅ Working | Add bisulfite-specific use cases |
| **crisprseq** | 1 general | ✅ Exists | Expand with CRISPR screen variants |
| **mag** | 2 variants | ✅ Exists | Add more metagenomics use cases |

### High-Priority To Implement (Tier 1)

| Pipeline | Apps Planned | Priority | Biological Domain |
|----------|--------------|----------|-------------------|
| **chipseq** | 6 apps | P0 | Transcription factor binding, histone marks |
| **cutandrun** | 4 apps | P1 | Low-input chromatin profiling |
| **differentialabundance** | 4 apps | P1 | RNA-seq/proteomics downstream analysis |
| **ampliseq** | 3 apps | P1 | Microbial community profiling (16S/ITS) |
| **nanoseq** | 4 apps | P1 | Oxford Nanopore long-read sequencing |
| **viralrecon** | 3 apps | P1 | Viral genome reconstruction |
| **proteinfold** | 3 apps | P1 | AlphaFold protein structure prediction |
| **spatialvi** | 4 apps | P1 | Spatial transcriptomics |

See **[PIPELINE_IMPLEMENTATION_PLAN.md](PIPELINE_IMPLEMENTATION_PLAN.md)** for complete list of 60+ pipelines.

---

## 🎯 Philosophy

### One Pipeline → Multiple Focused Apps

Instead of creating one complex app with 50+ parameters, we create 10+ simple apps per pipeline, each optimized for a specific biological use case.

**Example: nf-core/sarek**

❌ **Old**: One "Sarek" app with all tools and parameters exposed

✅ **New**: 10 focused apps:
1. "Cancer Variant Detection: Tumor vs Normal"
2. "Inherited Genetic Variant Detection"
3. "Structural Variant Detection"
4. "Copy Number Variation Analysis"
5. "Trio Analysis: Family-Based Variant Detection"
6. ...and more

### Key Principles

1. **Biology-First Language** - Write for biologists, not bioinformaticians
2. **Complete Input Instructions** - Show exact CSV format with examples
3. **Hardcode Everything Possible** - Expose only 3-5 essential parameters
4. **Extensive Documentation** - Document every attempt, success, and failure
5. **Five-Attempt Protocol** - Test up to 5 times, then mark failed and move on

---

## 🚀 Getting Started

### For New Contributors

1. **Read**: [_templates/QUICK_START.md](_templates/QUICK_START.md) - Complete guide
2. **Read**: [NEXTFLOW-DEVELOPMENT.md](../NEXTFLOW-DEVELOPMENT.md) - Patterns
3. **Study**: Working examples in `scrnaseq/` or `sarek/` directories
4. **Choose**: Pick a Tier 1 pipeline from [PIPELINE_IMPLEMENTATION_PLAN.md](PIPELINE_IMPLEMENTATION_PLAN.md)
5. **Implement**: Follow step-by-step guide

### Quick Commands

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for one-page cheat sheet.

**Start new pipeline**:
```bash
cd nextflow
mkdir {pipeline}
cd {pipeline}
cp ../_templates/PIPELINE_STATUS.template.md ./PIPELINE_STATUS.md
cp ../_templates/USE_CASES.template.md ./USE_CASES.md
# Research and document use cases
```

**Implement use case**:
```bash
mkdir {usecase}
cd {usecase}
# Create app.json, config, test data, README.md, TESTING_LOG.md
# Test up to 5 times, document everything
```

---

## 📝 Documentation Requirements

Every app must have:

### User-Facing
- **README.md** - Complete user guide with:
  - What the analysis does (biological context)
  - When to use it
  - Input requirements with exact CSV format
  - Expected outputs
  - Testing instructions

### Developer-Facing
- **TESTING_LOG.md** - Complete test history:
  - All attempts (up to 5)
  - Error messages and logs
  - Fixes attempted
  - Final outcome (✅ or ❌)
  - Lessons learned

### Status Tracking
- **PIPELINE_STATUS.md** - Per pipeline progress
- **STATUS.txt** - Per app quick status (✅/❌/⚠️/🔄/🔲)

---

## ✅ Success Criteria

### App is Working
- ✅ Test job completes (status: COMPLETED)
- ✅ Expected outputs generated
- ✅ No errors in logs
- ✅ Results scientifically meaningful

### Documentation is Complete
- ✅ All test attempts in TESTING_LOG.md
- ✅ Complete README.md with samplesheet examples
- ✅ PIPELINE_STATUS.md updated
- ✅ Committed to git with clear message

### App is Failed
- ❌ 5 attempts exhausted without success
- ❌ Reason documented in TESTING_LOG.md
- ❌ Marked in STATUS.txt and PIPELINE_STATUS.md
- ❌ Committed to git, moved on to next use case

---

## 📈 Progress Tracking

### Overall Targets
- **Tier 1** (8 pipelines, ~65 apps): 90%+ success rate
- **Tier 2** (10 pipelines, ~30 apps): 75%+ success rate
- **Tier 3+** (40+ pipelines): 50%+ success rate

### Current Statistics
- **Pipelines with apps**: 7 existing
- **Total working apps**: ~12
- **Apps to implement**: ~300+ across all tiers
- **Next priority**: chipseq (Tier 1, P0)

---

## 🔧 Common Issues

| Issue | Quick Fix |
|-------|-----------|
| docker: command not found | `docker.enabled = false` in config |
| OutOfMemoryError | Increase memory or node size |
| File not found | Check samplesheet paths |
| Process timeout | Increase time limit in config |

See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for complete troubleshooting guide.

---

## 🤝 Contributing

### Workflow
1. Create branch: `git checkout -b pipeline/{pipeline-name}`
2. Implement use case following templates
3. Test thoroughly (up to 5 attempts)
4. Document everything
5. Commit frequently with clear messages
6. Merge to main when complete

### Commit Messages
```
pipeline/{pipeline}: {action} - {detail}

Examples:
pipeline/chipseq: Research complete - 6 use cases identified
pipeline/chipseq: Add transcription-factor-narrow app
pipeline/chipseq: Fix OOM error (attempt 3)
pipeline/chipseq: Mark failed after 5 attempts - platform limitation
```

---

## 🌟 Highlights

### What Makes This Different

1. **Biology-Focused** - Every app speaks the language of biologists, not bioinformaticians
2. **Pre-Configured** - Best practices hardcoded, only essential parameters exposed
3. **Complete Documentation** - Every file explains how to create input files, not just what they are
4. **Systematic Testing** - 5-attempt protocol with complete documentation of failures
5. **Knowledge Sharing** - Every attempt teaches future contributors

### Example: Biology-Focused Description

❌ **Technical**: "Sarek pipeline for somatic variant calling using GATK Mutect2"

✅ **Biology-Focused**: "Identify cancer-specific genetic mutations by comparing tumor tissue to matched normal tissue. Detects SNVs (single nucleotide variants) and small insertions/deletions that are present in cancer cells but not in healthy cells - essential for precision oncology, understanding tumor evolution, and identifying therapeutic targets."

---

## 📚 Additional Resources

### Documentation
- [NEXTFLOW-DEVELOPMENT.md](../NEXTFLOW-DEVELOPMENT.md) - Complete development patterns
- [PIPELINE_IMPLEMENTATION_PLAN.md](PIPELINE_IMPLEMENTATION_PLAN.md) - Detailed plan with use cases
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Project overview

### External Resources
- nf-core pipelines: https://nf-co.re/pipelines
- nf-core Slack: https://nfcore.slack.com
- nf-core GitHub: https://github.com/nf-core/
- Camber documentation: https://docs.camber.cloud

### Working Examples
- `scrnaseq/` - Comprehensive single-cell RNA-seq
- `sarek/` - Variant calling example
- `atacseq/` - Chromatin accessibility

---

## 🎓 Learning Path

1. **Week 1**: Read all documentation, study examples
2. **Week 2**: Implement first use case (follow QUICK_START.md)
3. **Week 3-4**: Implement more use cases, build speed
4. **Week 5+**: Contribute to Tier 1 pipelines

**Time to Productivity**: 1-2 weeks for first working app, then accelerating

---

## ❓ FAQ

**Q: How many parameters should I expose?**
A: 3-5 maximum. Hardcode everything else.

**Q: What if the app fails after 5 attempts?**
A: Document thoroughly, mark as ❌ Failed, commit, and move on. It's okay!

**Q: How detailed should my TESTING_LOG.md be?**
A: Very detailed. Include full commands, error messages, and your reasoning.

**Q: Should I write for biologists or bioinformaticians?**
A: Always biologists. Assume no bioinformatics background.

**Q: What if I find a better way to do something?**
A: Great! Update templates and document the improvement.

---

## 📞 Need Help?

1. Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for quick answers
2. Read [_templates/QUICK_START.md](_templates/QUICK_START.md) for detailed guide
3. Study working examples in existing pipeline directories
4. Consult nf-core documentation: https://nf-co.re/
5. Ask on nf-core Slack: https://nfcore.slack.com

---

## 📅 Last Updated

**Date**: 2025-09-30
**Status**: 📋 Planning Complete, Ready for Implementation
**Next Priority**: chipseq (Tier 1, P0 - no existing implementation)

---

**Ready to start?** Read [_templates/QUICK_START.md](_templates/QUICK_START.md) and begin implementing!