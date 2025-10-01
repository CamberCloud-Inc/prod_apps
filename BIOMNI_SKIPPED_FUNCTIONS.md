# Biomni Apps - Skipped Functions Report

**Date:** 2025-09-30
**Total Functions:** 210
**Wrapped Functions:** 205
**Skipped Functions:** 5
**Coverage:** 97.6%

---

## Executive Summary

Out of 210 biomedical research tools in the Biomni repository, **205 were successfully wrapped** as Camber apps. Only **5 functions were skipped**, representing 97.6% coverage.

### Skipped Functions Breakdown

| Category | Function Name | Reason | Priority |
|----------|--------------|--------|----------|
| genomics | annotate_celltype_scRNA | Requires LLM integration | LOW |
| genomics | get_uce_embeddings_scRNA | Environment not ready (TODO in source) | LOW |
| genomics | map_to_ima_interpret_scRNA | Requires external data setup | LOW |
| genomics | get_gene_set_enrichment_analysis_supported_database_list | Utility function (returns list) | MEDIUM |
| immunology | analyze_immunohistochemistry_image | Unknown (likely oversight) | HIGH |

---

## Detailed Analysis

### 1. genomics.annotate_celltype_scRNA
**Reason:** Requires LLM integration
**Details:**
- Function signature includes `llm="claude-3-5-sonnet-20241022"` parameter
- Uses `get_llm()` function from Biomni's agent framework
- Performs cell type annotation using language model reasoning

**Recommendation:** LOW priority
- Would require integrating Biomni's LLM framework
- Complex dependency on AI agent capabilities
- Alternative tools exist (annotate_celltype_with_panhumanpy is already wrapped)

---

### 2. genomics.get_uce_embeddings_scRNA
**Reason:** Environment not ready
**Details:**
- Source code contains TODO comment: "the environment is not ready for this tool"
- Requires Universal Cell Embeddings (UCE) model setup
- Dependencies may not be publicly available yet

**Recommendation:** LOW priority
- Wait for Biomni team to complete UCE environment setup
- Monitor Biomni repository for updates

---

### 3. genomics.map_to_ima_interpret_scRNA
**Reason:** Requires external data/environment setup
**Details:**
- Maps single-cell data to IMA (Integrated Molecular Atlas)
- Requires specific reference data that may not be bundled
- Complex environment setup needed

**Recommendation:** LOW priority
- Depends on external reference datasets
- May require significant storage/compute resources

---

### 4. genomics.get_gene_set_enrichment_analysis_supported_database_list
**Reason:** Simple utility function
**Details:**
- Returns hardcoded list of supported GSEA databases
- Function signature: `def get_gene_set_enrichment_analysis_supported_database_list() -> str:`
- Returns: List of database names as string

**Recommendation:** MEDIUM priority
- Could be useful as a discovery tool for users
- Very simple to implement (no complex dependencies)
- Would complement the gene_set_enrichment_analysis app

**Action:** Consider adding simple wrapper that returns the database list

---

### 5. immunology.analyze_immunohistochemistry_image
**Reason:** Likely oversight during automated creation
**Details:**
- Standard image analysis function
- Similar to other histology analysis tools that WERE wrapped
- No obvious dependency or LLM requirements

**Recommendation:** HIGH priority - SHOULD BE ADDED
- No technical blockers
- Follows same pattern as other image analysis tools
- Likely missed due to automated agent not detecting it

**Action:** Create wrapper immediately

---

## Coverage by Category

| Category | Total Functions | Wrapped | Skipped | Coverage % |
|----------|----------------|---------|---------|------------|
| genomics | 17 | 13 | 4 | 76.5% |
| genetics | 9 | 9 | 0 | 100% |
| molecular_biology | 18 | 18 | 0 | 100% |
| biochemistry | 6 | 6 | 0 | 100% |
| biophysics | 3 | 3 | 0 | 100% |
| bioengineering | 7 | 7 | 0 | 100% |
| bioimaging | 10 | 10 | 0 | 100% |
| cancer_biology | 6 | 6 | 0 | 100% |
| cell_biology | 5 | 5 | 0 | 100% |
| immunology | 10 | 9 | 1 | 90% |
| pathology | 7 | 7 | 0 | 100% |
| literature | 8 | 8 | 0 | 100% |
| pharmacology | 23 | 23 | 0 | 100% |
| microbiology | 12 | 12 | 0 | 100% |
| physiology | 11 | 11 | 0 | 100% |
| systems_biology | 7 | 7 | 0 | 100% |
| synthetic_biology | 8 | 8 | 0 | 100% |
| glycoengineering | 3 | 3 | 0 | 100% |
| database | 35 | 35 | 0 | 100% |
| support_tools | 5 | 5 | 0 | 100% |
| **TOTAL** | **210** | **205** | **5** | **97.6%** |

---

## Immediate Action Items

### 1. Add Missing Wrapper (HIGH PRIORITY)
**Function:** `immunology.analyze_immunohistochemistry_image`
**Status:** Should be added immediately
**Effort:** Low (15 minutes)

### 2. Consider Adding Utility Wrapper (MEDIUM PRIORITY)
**Function:** `genomics.get_gene_set_enrichment_analysis_supported_database_list`
**Status:** Optional but useful
**Effort:** Very low (5 minutes)

### 3. Document LLM-Dependent Functions (LOW PRIORITY)
**Functions:**
- `genomics.annotate_celltype_scRNA`
- `genomics.get_uce_embeddings_scRNA`
- `genomics.map_to_ima_interpret_scRNA`

**Status:** Document as "Future Enhancements"
**Effort:** Documentation only

---

## Recommendations for Future Development

### Phase 1: Complete Core Coverage (Immediate)
1. ✅ Create wrapper for `analyze_immunohistochemistry_image`
2. ⏸️ Optionally add `get_gene_set_enrichment_analysis_supported_database_list`
3. ✅ Update totals to 206 or 207 wrapped functions

### Phase 2: LLM Integration Framework (Future)
1. Design Biomni LLM integration layer for Camber
2. Add support for functions requiring `get_llm()`
3. Implement `annotate_celltype_scRNA` with LLM backend

### Phase 3: Environment Setup (Future)
1. Monitor Biomni repository for UCE environment updates
2. Add `get_uce_embeddings_scRNA` when ready
3. Investigate IMA reference data availability for `map_to_ima_interpret_scRNA`

---

## Conclusion

The Biomni app creation achieved **97.6% coverage**, which is excellent for an automated wrapping process. The 5 skipped functions fall into clear categories:

- **1 function** should be added immediately (oversight)
- **1 function** could be added optionally (utility)
- **3 functions** have technical blockers (LLM/environment dependencies)

**Next Step:** Add the missing `analyze_immunohistochemistry_image` wrapper to achieve 98.1% coverage (206/210).

---

**Report Generated:** 2025-09-30
**Author:** Automated Biomni Wrapper Audit
**Status:** Complete
