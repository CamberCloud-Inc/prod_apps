# Pipeline: {pipeline-name}

**Latest Version**: X.Y.Z (check https://nf-co.re/{pipeline})
**Last Updated**: YYYY-MM-DD
**Overall Status**: 🔲 Not Started | 🔄 In Progress | ✅ Complete | ❌ Failed | ⚠️ Partial

## Pipeline Summary

Brief description of what this pipeline does and its biological applications.

**Official Documentation**: https://nf-co.re/{pipeline}
**GitHub Repository**: https://github.com/nf-core/{pipeline}

## Use Cases Identified

Total: X use cases

1. **{usecase-1}** - 🔲 Todo | 🔄 Testing | ✅ Working | ❌ Failed
   - Directory: `{usecase-1}/`
   - Description: Brief description

2. **{usecase-2}** - Status
   - Directory: `{usecase-2}/`
   - Description: Brief description

3. ...

## Implementation Progress

**Research Phase**:
- [ ] Pipeline documentation reviewed
- [ ] Use cases identified and documented in USE_CASES.md
- [ ] Test data located
- [ ] Common parameters identified

**Implementation Phase**:
- [ ] App 1: {usecase-1} - [Status with link to dir]
- [ ] App 2: {usecase-2} - [Status with link to dir]
- [ ] App 3: ...

**Testing Phase**:
- [ ] All apps have test data
- [ ] All apps tested at least once
- [ ] Working apps documented
- [ ] Failed apps marked with reasons

## Statistics

- **Apps Planned**: X
- **Apps Working**: Y (Y/X = Z%)
- **Apps Failed**: N
- **Total Test Attempts**: T
- **Average Attempts Per App**: T/X

## Common Issues Encountered

### Issue 1: {Issue Title}
**Frequency**: Occurred in X apps
**Description**: What went wrong
**Solution**: How it was resolved (or marked as unsolvable)
**Affected Apps**: List of apps

### Issue 2: ...

## Configuration Patterns That Work

Document successful patterns here:

**Resource Allocation**:
```groovy
// Example working config
process {
  withLabel:process_medium {
    cpus   = { 6     * task.attempt }
    memory = { 36.GB * task.attempt }
  }
}
```

**Key Parameters**:
- Parameter 1: Always set to X for this pipeline
- Parameter 2: Varies by use case (see individual apps)

## Lessons Learned

1. Key insight learned during implementation
2. What would we do differently next time
3. Patterns to avoid

## Next Steps

- [ ] Action item 1
- [ ] Action item 2

## Notes

Any additional notes, caveats, or important information about this pipeline.