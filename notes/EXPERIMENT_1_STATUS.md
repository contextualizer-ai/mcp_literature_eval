# Experiment 1: Cross-Agent Comparison - Status

## Current Status: Ready to Run (with known issue)

**Date:** 2025-10-31
**Branch:** `compare-across-agents`

## Setup Complete ✅

1. **Branch created:** `compare-across-agents`
2. **Configuration files created:**
   - `project/literature_mcp_eval_config_claude.yaml` - Claude-code agent config
   - `project/literature_mcp_eval_config.yaml` - Goose agent config (baseline)
3. **Analysis notebook created:** `notebook/experiment_1_cross_agent_analysis.ipynb`
4. **Documentation complete:**
   - `notes/experiment_1_cross_agent_comparison.md` - Detailed experimental plan
   - `README.md` - Updated with experiment instructions
   - `project/README.md` - Config directory guide
5. **Directory structure:**
   - `results/raw/` - For raw YAML outputs
   - `results/figures/` - For generated plots
   - `.gitignore` updated to exclude `results/raw/`

## Known Issue: Evaluation Metric API Key

### Problem
MetaCoder/DeepEval defaults to using OpenAI for the CorrectnessMetric evaluation, requiring `OPENAI_API_KEY`. However:
- We want to use Claude (Anthropic) for evaluation
- `ANTHROPIC_BASE_URL` is set but `ANTHROPIC_API_KEY` may not be
- The evaluation step fails even though the agent successfully retrieves content

### Evidence
Test run on 2025-10-31 showed:
```
✅ Claude-code successfully ran (30 seconds)
✅ Retrieved PMID:28027860 using artl MCP
✅ Output saved to eval_workdir/
❌ Evaluation failed: DeepEval trying to use OpenAI
```

Error:
```
openai.OpenAIError: The api_key client option must be set either by passing
api_key to the client or by setting the OPENAI_API_KEY environment variable
```

### Solutions

**Option 1: Set OpenAI API Key (temporary workaround)**
```bash
export OPENAI_API_KEY="your_key_here"
```
- Pro: Quick fix, evaluations will run
- Con: Using OpenAI for evaluation instead of Claude

**Option 2: Fix metacoder to use Anthropic for evaluation**
- Modify metacoder's `get_default_metrics()` in `evals/runner.py`
- Configure DeepEval to use Anthropic model
- Requires metacoder code changes

**Option 3: Manual evaluation**
- Run agents without evaluation
- Extract outputs from `eval_workdir/`
- Use custom script to evaluate with Claude

## Test Results

### Claude-code Agent Test (2025-10-31)

**Command:**
```bash
uv run metacoder eval project/literature_mcp_eval_config_test.yaml \
  -c claude \
  -o results/raw/test_20251031.yaml
```

**Results:**
- ✅ Agent launched successfully
- ✅ MCP config written to `.mcp.json`
- ✅ Retrieved paper using artl-mcp
- ✅ Full-text content downloaded to `Documents/artl-mcp/`
- ❌ Evaluation step failed (API key issue)

**Runtime:**
- First test case: 30.60 seconds (agent execution only)

## Next Steps

### Immediate (to run experiments)

1. **Resolve API key issue** - Choose one of the solutions above
2. **Run full evaluation with claude-code:**
   ```bash
   uv run metacoder eval project/literature_mcp_eval_config_claude.yaml \
     -o results/raw/claude_full_20251031.yaml
   ```
3. **Compare with baseline goose results:**
   - Already have: `results/mcp_literature_eval_results_20250917.yaml`
4. **Run analysis notebook:**
   ```bash
   jupyter notebook notebook/experiment_1_cross_agent_analysis.ipynb
   ```

### Medium-term (for robustness)

1. Fix metacoder to support Anthropic evaluator models
2. Add retry logic for agent failures
3. Implement session isolation to prevent state carry-over
4. Add progress checkpointing for long runs

## File Locations

### Configuration
- Baseline (goose): `project/literature_mcp_eval_config.yaml`
- Experiment 1 (claude): `project/literature_mcp_eval_config_claude.yaml`

### Results
- Baseline (goose): `results/mcp_literature_eval_results_20250917.yaml`
- Claude-code: `results/raw/claude_full_YYYYMMDD.yaml` (to be generated)

### Analysis
- Notebook: `notebook/experiment_1_cross_agent_analysis.ipynb`
- Figures: `results/figures/exp1_*.png`

### Working Directories
- Agent execution: `eval_workdir/`
- Downloaded papers: `eval_workdir/*/Documents/artl-mcp/`
- MCP logs: `eval_workdir/*/.cache/*/mcp-logs-*/`

## Questions for User

1. Do you have an OPENAI_API_KEY we can use temporarily?
2. Or should we pursue fixing metacoder to use Anthropic?
3. Should we proceed with manual evaluation as a workaround?

## Summary

**The infrastructure is ready.** Claude-code successfully retrieves papers via MCPs. The only blocker is configuring the evaluation metric to work with available API keys. Once resolved, we can:
- Run the full 100-test evaluation (25 cases × 4 MCPs)
- Compare claude-code vs. goose performance
- Generate publication-quality figures
- Fill the "[AUTHOR to fill]" section in the manuscript
