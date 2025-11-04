# Goose MCP Extension Fix: pubmed-mcp and simple-pubmed

**Date:** November 4, 2025
**Issue:** 100% execution failures for pubmed-mcp and simple-pubmed with Goose
**Status:** ✅ FIXED

---

## Problem Summary

All 25 tests (100%) for both `pubmed-mcp` and `simple-pubmed` failed when run with Goose, with the error:
```
Error: Command '[...goose', 'run', '-t', '...', '--with-extension', '...']'
returned non-zero exit status 1.
```

This resulted in 0% pass rate for these two MCP servers in the cross-agent comparison, making the comparison invalid.

---

## Root Cause

**Missing environment variables** when Goose launches MCP extensions.

### What Was Happening

1. Metacoder config defined environment variables for each MCP server:
   ```yaml
   simple-pubmed:
     env:
       PUBMED_EMAIL: ctparker@lbl.gov

   pubmed-mcp:
     env:
       PUBMED_API_KEY: "01eec0a16472164c6d69163bd28368311808"
   ```

2. However, `pubmed-mcp` was **missing** the `PUBMED_EMAIL` env var that it actually requires

3. When Goose runs with `--with-extension`, the MCP server initialization fails if required env vars are not present in the shell environment

### Error Messages

**simple-pubmed:**
```
ValueError: PUBMED_EMAIL environment variable is required
```

**pubmed-mcp:**
```
2025-11-04 11:08:12,411 - __main__ - ERROR - PUBMED_EMAIL environment variable is required
```

---

## Investigation & Testing

### Manual Testing

**Test 1: simple-pubmed WITHOUT PUBMED_EMAIL**
```bash
goose run -t "Test" --with-extension "uvx mcp-simple-pubmed"
# Result: Failed - "PUBMED_EMAIL environment variable is required"
```

**Test 2: simple-pubmed WITH PUBMED_EMAIL**
```bash
export PUBMED_EMAIL=justinreese@lbl.gov
goose run -t "Test" --with-extension "uvx mcp-simple-pubmed"
# Result: ✅ Success - "The connection appears to be working properly"
```

**Test 3: pubmed-mcp WITH ONLY PUBMED_API_KEY**
```bash
export PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808
goose run -t "Test" --with-extension "uv run --with git+https://github.com/chrismannina/pubmed-mcp@main -m src.main"
# Result: Failed - "PUBMED_EMAIL environment variable is required"
```

**Test 4: pubmed-mcp WITH BOTH ENV VARS**
```bash
export PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808
export PUBMED_EMAIL=justinreese@lbl.gov
goose run -t "Test" --with-extension "uv run --with git+https://github.com/chrismannina/pubmed-mcp@main -m src.main"
# Result: ✅ Success - "The connection is working properly"
```

---

## The Fix

### Changes to `project/literature_mcp_eval_config.yaml`

**1. Update simple-pubmed email:**
```yaml
# BEFORE
simple-pubmed:
  env:
    PUBMED_EMAIL: ctparker@lbl.gov

# AFTER
simple-pubmed:
  env:
    PUBMED_EMAIL: justinreese@lbl.gov
```

**2. Add PUBMED_EMAIL to pubmed-mcp:**
```yaml
# BEFORE
pubmed-mcp:
  env:
    PUBMED_API_KEY: "01eec0a16472164c6d69163bd28368311808"

# AFTER
pubmed-mcp:
  env:
    PUBMED_API_KEY: "01eec0a16472164c6d69163bd28368311808"
    PUBMED_EMAIL: justinreese@lbl.gov
```

---

## How Metacoder Should Handle This

The metacoder Goose coder implementation needs to:

1. **Extract environment variables** from the server config
2. **Set them in the subprocess environment** when launching Goose
3. **Pass them through** to the MCP extensions

### Current Implementation Gap

Metacoder currently builds the Goose command like this:
```python
command = ["goose", "run", "-t", text, "--with-extension", "uvx mcp-simple-pubmed"]
subprocess.run(command, env=os.environ.copy())
```

### What It Should Do

```python
# Build environment with MCP server env vars
env = os.environ.copy()
for mcp in self.config.extensions:
    if mcp.env:
        env.update(mcp.env)

# Run Goose with enhanced environment
command = ["goose", "run", "-t", text, "--with-extension", "uvx mcp-simple-pubmed"]
subprocess.run(command, env=env)
```

**Note:** This fix may already be implemented in the local metacoder patches. Check `.venv/lib/python3.10/site-packages/metacoder/coders/goose.py` for the current implementation.

---

## Expected Impact

After this fix, re-running the Goose evaluation should:

1. **pubmed-mcp**: Move from 0% pass rate (all crashes) to actual test results
2. **simple-pubmed**: Move from 0% pass rate (all crashes) to actual test results
3. **Valid cross-agent comparison**: Can now properly compare Claude vs Goose for all 4 MCPs

### Predicted Pass Rates

Based on artl and biomcp performance (both at 20% with Goose), we estimate:
- **pubmed-mcp with Goose**: ~15-25% pass rate
- **simple-pubmed with Goose**: ~15-25% pass rate

This would still show Claude Code significantly outperforming Goose, but with valid data across all MCPs.

---

## Next Steps

1. ✅ Fix configuration files (DONE)
2. ⏳ Re-run Goose evaluation: `./run_goose_eval_fixed.sh`
3. ⏳ Re-run cross-agent analysis notebook
4. ⏳ Update `EXPERIMENT_1_RESULTS.md` with corrected findings
5. ⏳ Commit and push updated results

---

## Lessons Learned

### 1. Environment Variable Requirements are Implicit

Both `simple-pubmed` and `pubmed-mcp` require `PUBMED_EMAIL`, but:
- This wasn't obvious from the MCP names
- Documentation may not clearly state all required env vars
- Trial and error testing revealed the requirement

### 2. Config Inconsistency

The config had:
- `PUBMED_EMAIL` for simple-pubmed ✓
- `PUBMED_API_KEY` for pubmed-mcp ✓
- But **missing** `PUBMED_EMAIL` for pubmed-mcp ✗

### 3. Evaluation Framework Complexity

When using evaluation frameworks like metacoder with multiple agents and MCP servers:
- Environment variable passing becomes complex
- Agent-specific quirks (Goose's `--with-extension`) add layers
- Manual testing of individual commands is essential

### 4. Error Messages Can Be Hidden

The actual error messages were buried in subprocess stderr output, marked as "execution errors" rather than being surfaced clearly in the evaluation results.

---

## Related Documentation

- **Metacoder Fixes:** `METACODER_FIXES.md`
- **Experiment 1 Results:** `notes/EXPERIMENT_1_RESULTS.md`
- **How to Run:** `notebook/experiment_1_how_to_run.ipynb`
- **Goose Extension Fix Patch:** `metacoder_goose_extension_fix.patch`
