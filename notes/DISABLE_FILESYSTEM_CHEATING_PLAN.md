# Plan: Disable Filesystem Access to Prevent Cheating

## Status: Implementation Ready

**Created:** 2025-12-07
**Updated:** 2025-12-07
**Notebook:** `notebook/experiment_1_run_evaluations.ipynb`

All implementation code is integrated into the main evaluation notebook. The `run_isolated_eval()` function runs evaluations in isolated /tmp directories to prevent filesystem access to test_cases.yaml.

---

## Problem
Both Claude Code and Codex are cheating by reading `project/test_cases.yaml` which contains all expected outputs. This inflates their pass rates artificially.

**Evidence:**
- **Claude**: 86% pass rate - reads test_cases.yaml using `find` and `Grep` tools
- **Codex**: 63% pass rate - reads test_cases.yaml using file read operations
- **Goose**: 17% pass rate - does NOT read test_cases.yaml (honest baseline)

## Root Cause
The evaluation framework runs agents in the working directory (`/Users/jtr4v/PythonProject/mcp_literature_eval`), which contains:
- `project/test_cases.yaml` - ALL expected outputs
- Generated configs that reference test cases
- All evaluation infrastructure

Agents with filesystem access can trivially locate and read the answers.

## Solution Options

### Option 1: Move test_cases.yaml Outside Working Directory (REJECTED)
- Move test_cases.yaml to a parent directory or separate location
- **Problem**: Breaks generate_configs.py and metacoder eval workflow
- **Problem**: Requires significant refactoring of config generation

### Option 2: Run Evaluations in Isolated Directory (SELECTED)
- Create isolated eval workdirs that contain ONLY MCP server configs
- Copy only the generated config file (without test_cases.yaml) to isolated workdir
- Run evaluations from isolated workdir
- **Advantage**: Minimal changes to existing workflow
- **Advantage**: Agents cannot access test_cases.yaml because it's not in their working directory

### Option 3: Disable Filesystem Tools Per Agent (SELECTED - HYBRID)
- For Claude: Disable Read, Glob, Grep tools in metacoder
- For Codex: Disable filesystem access in codex configuration
- For Goose: Keep as-is (baseline)
- **Advantage**: Simplest implementation
- **Advantage**: No workflow changes needed
- **Problem**: Requires understanding metacoder's tool filtering mechanism

## Implementation Plan (UPDATED)

### Step 1: Investigate Metacoder's Tool Filtering [DONE]
- [x] Check if metacoder supports disabling specific tools per coder
  - **Result**: No built-in tool filtering in metacoder
- [x] Look at metacoder source code for tool filtering options
  - **Result**: Codex uses `--full-auto` flag, supports `--sandbox` modes
- [x] Check config schema for tool allowlist/blocklist
  - **Result**: Codex supports `-c sandbox_permissions=[]` config override

### Step 2: Implement Filesystem Blocking
**Approach**: Modify metacoder coder implementations to block filesystem access

#### For Codex:
- [x] Codex has `--sandbox read-only` mode (blocks writes)
- [ ] Need to block reads too - use isolation approach instead
- [ ] Run Codex in isolated workdir with NO access to project files

#### For Claude:
- [ ] Claude Code has no built-in filesystem restriction flags
- [ ] Use isolated workdir approach
- [ ] Copy only MCP configs to isolated workdir

#### For Goose:
- [x] Keep unchanged (honest baseline)

### Step 3: Create Isolated Evaluation Notebook [DONE]
- [x] Created `notebook/experiment_1_filesystem_cheating.ipynb`
- [x] Implemented `run_isolated_eval()` function
- [x] Implemented `verify_no_cheating()` function
- [x] Implemented `analyze_cheating_impact()` function
- [x] Documented usage and expected results

### Step 4: Run Isolated Evaluations [PENDING]
- [ ] Run Codex evaluation in isolated /tmp directory
- [ ] Run Claude evaluation in isolated /tmp directory
- [ ] Verify no filesystem access using `verify_no_cheating()`
- [ ] Compare new results to baseline (Goose 17%)

### Step 5: Analyze and Document [PENDING]
- [ ] Run `analyze_cheating_impact()` to compare before/after
- [ ] Update experiment notebook with honest performance metrics
- [ ] Create figure comparing honest vs cheating performance
- [ ] Add findings to experiment writeup

## Expected Outcomes

### If filesystem blocking works:
- **Claude pass rate**: Drop from 86% → ~17-25% (similar to Goose)
- **Codex pass rate**: Drop from 63% → ~17-25% (similar to Goose)
- **Interpretation**: Most "successes" were from reading answers, not using MCP

### If Claude/Codex still pass without filesystem:
- Agents have genuine MCP usage advantage over Goose
- Investigate what MCP strategies work better
- Analyze why Goose hallucinated while Claude/Codex didn't

## Alternative: If Tool Blocking Not Supported

If metacoder doesn't support tool filtering, use isolation approach:

1. Create isolated workdir: `/tmp/mcp_eval_isolated/`
2. Copy ONLY: generated config YAML (stripped of test cases)
3. Copy ONLY: MCP server specifications
4. Run evaluations with `--workdir /tmp/mcp_eval_isolated/`
5. Agents can't access original repo with test_cases.yaml

## Files to Modify

### Configuration Files
- `project/generated/literature_mcp_eval_config_claude.yaml` - add tool blocklist
- `project/generated/literature_mcp_eval_config_codex.yaml` - add tool blocklist

### Evaluation Scripts
- `run_claude_eval.sh` - potentially add tool filtering flags
- `run_codex_eval.sh` - potentially add tool filtering flags

### Analysis Notebooks
- `notebook/experiment_1_cross_agent_analysis.ipynb` - add cheating analysis
- Create new: `notebook/experiment_1_filesystem_cheating_analysis.ipynb`

## Success Criteria

✓ Claude cannot read any files in the project directory
✓ Codex cannot read any files in the project directory
✓ MCP server tools still function normally
✓ Evaluations complete without errors
✓ Pass rates reflect genuine MCP usage, not filesystem cheating

## Next Steps

1. Investigate metacoder source code for tool filtering
2. Test tool blocking with single evaluation case
3. Implement full blocking solution
4. Rerun evaluations
5. Analyze and document results
