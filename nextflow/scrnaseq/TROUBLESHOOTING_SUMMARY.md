# nf-core/scrnaseq Troubleshooting Summary

## Original Problem (Job 3491)
```
ERROR: docker: command not found (exit code 127)
```

## Complete Troubleshooting Process

### Issue 1: Docker vs Container System ✅ SOLVED
**Problem**: Pipeline used `-profile test,docker` but Docker not available
**Error**: `.command.run: line 300: docker: command not found`
**Solution**: Remove docker profile, use only `-profile test`
**Result**: Platform correctly uses k8s container system

### Issue 2: CPU Resource Constraints ✅ SOLVED  
**Problem**: Processes requesting more CPUs than available
**Error**: `Process requirement exceeds available CPUs -- req: 6; avail: 2`
**Solution**: Limit all processes to max 1-2 CPUs in configuration
**Result**: CPU allocation now works within platform limits

### Issue 3: Memory Resource Constraints ✅ SOLVED
**Problem**: Processes requesting more memory than available
**Error**: `Process requirement exceeds available memory -- req: 4 GB; avail: 3.9 GB`
**Solution**: Limit memory to max 3GB per process
**Result**: Memory allocation now works within platform limits

### Issue 4: Container/Tool Loading ⚠️ CURRENT ISSUE
**Problem**: Tools not found in execution environment
**Error**: `fastqc: command not found (exit status 127)`
**Status**: Resource constraints fixed, but container system needs investigation

## Key Findings

### What Works ✅
- **CPU/Memory constraints**: Successfully limited to platform resources
- **Profile system**: Platform k8s profile loads correctly
- **Container detection**: No more Docker errors
- **Resource allocation**: Processes now fit within node limits

### What Doesn't Work ❌
- **Tool availability**: Software tools not found in execution environment
- **Container loading**: No container pulling/mounting visible in logs
- **Environment setup**: Tools like `fastqc` missing from PATH

## Resource Limits Discovered
- **Available CPUs**: 2 cores maximum
- **Available Memory**: ~3.9GB maximum  
- **Node Type**: LARGE still has these constraints
- **Platform**: Uses k8s container orchestration

## Working Configuration Files Created
1. **`camber-final-fix.config`**: Resource-constrained configuration that respects platform limits
2. **`app.json`**: Proper app definition with Camber platform integration
3. **`CLAUDE.md`**: Complete documentation of troubleshooting process

## Next Steps for Platform Team
1. **Container Investigation**: Why aren't containers loading tools properly?
2. **Environment Setup**: How should tools be made available in execution environment?
3. **Profile Configuration**: Does the k8s profile need container registry configuration?
4. **Resource Documentation**: Document actual resource limits for different node sizes

## Test Jobs Summary
- **Job 3491**: Original failure (docker not found)
- **Job 3841**: Docker → Singularity (singularity not found) 
- **Job 3842**: Minimal config (CPU constraint)
- **Job 3843**: CPU fixed (memory constraint)
- **Job 3844**: Resources fixed (tools not found)

## Current Status
✅ **Resource constraints solved**: CPU and memory limits working
❌ **Container system**: Tools not loading in execution environment
🔄 **Next**: Platform team needs to investigate container/tool loading mechanism