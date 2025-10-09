# Use Cases: {pipeline-name}

## Research Summary

**Pipeline Purpose**: Brief description
**Typical Users**: Who uses this pipeline (e.g., cancer researchers, microbiologists)
**Data Types**: What sequencing/data types it processes

## Identified Use Cases

Each use case should be a distinct biological question or experimental scenario that represents a common way researchers use this pipeline.

---

### Use Case 1: {Descriptive Name}

**Biological Question**: What scientific question does this address?

**Target Audience**: Who would use this specific configuration?
- Example: Cancer researchers studying somatic mutations
- Example: Plant biologists studying RNA expression

**Typical Experimental Design**:
- Sample type: What kind of samples
- Data type: Sequencing platform and protocol
- Scale: Typical number of samples

**Key Parameters**:
- Hardcoded: Which parameters should be fixed for this use case
  - Parameter 1: Value (rationale)
  - Parameter 2: Value (rationale)

- Exposed: Which parameters user should control
  - Parameter 1: Why user needs to set this
  - Parameter 2: Why user needs to set this

**Tools/Algorithms**: Which specific tools from the pipeline to use
- Tool 1: Why chosen for this use case
- Tool 2: Alternative if needed

**Expected Outputs**: What results this analysis produces
- Output 1: Description
- Output 2: Description

**Resource Requirements**: Estimated compute needs
- Node size: SMALL | MEDIUM | LARGE | XLARGE
- Runtime: Typical duration
- Special needs: GPU, high memory, etc.

**Priority**: P0 | P1 | P2 | P3
- P0 = Most common, highest impact
- P1 = Common, important
- P2 = Specialized, useful
- P3 = Rare, nice-to-have

**References**:
- Scientific papers describing this approach
- Protocol papers
- Key resources

---

### Use Case 2: {Descriptive Name}

[Same structure as Use Case 1]

---

### Use Case 3: {Descriptive Name}

[Same structure as Use Case 1]

---

## Use Cases Considered But Excluded

Document use cases that were considered but not implemented, and why:

### {Excluded Use Case}
**Reason for Exclusion**:
- Too specialized (affects <1% of users)
- Platform limitation (requires feature X not available)
- Redundant with use case Y
- Insufficient test data

---

## Research Sources

Where did these use cases come from?

- [ ] nf-core pipeline documentation
- [ ] Scientific literature review
- [ ] nf-core Slack discussions
- [ ] GitHub issues and discussions
- [ ] Expert consultation
- [ ] Similar pipeline analysis

**Key Papers/Resources**:
1. Citation or link
2. Citation or link

---

## User Personas

Define typical users for this pipeline:

### Persona 1: {Name/Role}
**Background**: Research area and expertise
**Goals**: What they want to accomplish
**Technical Level**: Beginner | Intermediate | Advanced
**Most Likely Use Cases**: List of 2-3 use cases they'd use

### Persona 2: {Name/Role}
[Same structure]

---

## Implementation Priority

Suggested order for implementing use cases:

1. **{Use Case X}** - Start here because:
   - Most common use case
   - Good test data available
   - Clear documentation

2. **{Use Case Y}** - Second because:
   - Builds on first use case
   - Shares configuration patterns

3. **{Use Case Z}** - Third because:
   - Important but specialized

4-N. Remaining use cases in order of priority

---

## Success Criteria

How will we know if these use cases are well-chosen?

- [ ] Cover 80%+ of typical usage scenarios
- [ ] Each use case is distinct (no overlap)
- [ ] Clear biological motivation for each
- [ ] Test data available for each
- [ ] Positive feedback from target users (if possible)

---

## Questions to Resolve

Outstanding questions about use cases:

1. Question 1: Description and what needs to be researched
2. Question 2: ...

---

## Last Updated

**Date**: YYYY-MM-DD
**By**: Name/identifier
**Changes**: What was updated in this revision