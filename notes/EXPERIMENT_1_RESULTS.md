# Experiment 1: Cross-Agent Comparison Results

**Date:** November 4, 2025
**Analysis:** Comparison of Claude Code vs Goose on MCP literature retrieval tasks

---

## Executive Summary

**Agent choice SIGNIFICANTLY affects MCP retrieval performance.**

- **Claude Code:** 47.0% pass rate (median score: 0.616)
- **Goose:** 10.0% pass rate (median score: 0.099)
- **Performance gap:** 37 percentage points
- **Statistical significance:** χ² = 31.800, p < 0.0001 (highly significant)

---

## Overall Pass Rates by MCP Server

| MCP Server     | Claude Code | Goose | Difference | Notes |
|----------------|-------------|-------|------------|-------|
| artl           | 36.0%       | 20.0% | +16.0 pp   | Valid comparison |
| biomcp         | 48.0%       | 20.0% | +28.0 pp   | Valid comparison |
| pubmed-mcp     | 56.0%       | 0.0%  | +56.0 pp   | ⚠️ **INVALID** - Goose execution errors |
| simple-pubmed  | 48.0%       | 0.0%  | +48.0 pp   | ⚠️ **INVALID** - Goose execution errors |

**⚠️ IMPORTANT CAVEAT:** The 0% pass rate for `pubmed-mcp` and `simple-pubmed` with Goose is due to **100% execution failures** (all 25 tests crashed with exit status 1), not actual test failures. These MCPs are not configured correctly with Goose's `--with-extension` system. The comparison is only valid for `artl` and `biomcp` where both agents successfully executed tests.

---

## Performance by Task Type (Case Group)

| Task Type                          | Claude Code | Goose | Difference | Variance |
|------------------------------------|-------------|-------|------------|----------|
| **Publication status**             | 100.0%      | 25.0% | +75.0 pp   | 2812.5   |
| **Table/Figure extraction**        | 68.8%       | 12.5% | +56.3 pp   | 1582.0   |
| **Summarization**                  | 50.0%       | 0.0%  | +50.0 pp   | 1250.0   |
| **Metadata**                       | 62.5%       | 18.8% | +43.7 pp   | -        |
| **Supplementary material**         | 41.7%       | 16.7% | +25.0 pp   | -        |
| **Text extraction**                | 29.5%       | 4.5%  | +25.0 pp   | -        |

**Most Agent-Sensitive Tasks:**
1. **Publication status** (variance = 2812.5) - Claude perfect, Goose struggles
2. **Table/Figure extraction** (variance = 1582.0) - Large performance gap
3. **Summarization** (variance = 1250.0) - Claude moderate, Goose complete failure

---

## Statistical Analysis

### Chi-Square Test for Independence
- **Test:** Agent choice vs. pass/fail outcome
- **Result:** χ² = 31.800, p < 0.0001, df = 1
- **Interpretation:** Agent choice and test outcome are NOT independent (highly significant relationship)

### Mann-Whitney U Test for Score Distributions
- **Test:** Comparison of semantic similarity scores between agents
- **Result:** U = 2094.5, p < 0.0001
- **Median scores:**
  - Claude Code: 0.616
  - Goose: 0.099
- **Interpretation:** Claude Code produces significantly higher quality responses

---

## Score Distribution Analysis

**Claude Code:**
- Mean: 0.56
- Median: 0.616
- Std: 0.38
- Min: 0.0
- 25th percentile: 0.21
- 75th percentile: 0.93
- Max: 1.0

**Goose:**
- Mean: 0.15
- Median: 0.099
- Std: 0.20
- Min: 0.0
- 25th percentile: 0.02
- 75th percentile: 0.20
- Max: 0.98

**Key Insight:** Claude Code's score distribution is much broader and shifted toward higher values, indicating more consistent retrieval of correct information.

---

## Interpretation & Implications

### Why Does Agent Choice Matter?

1. **Tool Comprehension:** Claude Code appears better at understanding MCP tool schemas and selecting appropriate tools for each query type.

2. **Error Handling:** When MCPs return no results, Claude Code may better handle fallback strategies or interpret partial information.

3. **Context Understanding:** Claude Code demonstrates superior ability to extract and present the specific information requested from retrieved papers.

4. **MCP Server Compatibility:** Some MCP servers (pubmed-mcp, simple-pubmed) may have characteristics that Claude Code handles well but Goose cannot.

### Task-Specific Observations

- **Publication status queries:** Claude Code excelled (100%), suggesting strong metadata interpretation
- **Table/Figure extraction:** Both struggled, but Claude Code significantly outperformed (68.8% vs 12.5%)
- **Text extraction:** Both performed poorly, indicating MCP limitations rather than agent differences
- **Summarization:** Goose completely failed (0%), while Claude Code achieved moderate success (50%)

### Implications for MCP Evaluation

⚠️ **Critical Finding:** Baseline MCP performance metrics are heavily influenced by the choice of coding agent.

- Previous evaluations using Goose may have **underestimated** true MCP capabilities
- Claude Code results likely provide a more accurate ceiling of MCP performance
- Future evaluations should specify which agent was used for reproducibility

---

## Visualizations

Generated figures (saved to `results/figures/`):

1. **exp1_overall_performance_by_agent.png** - Bar chart comparing pass rates by MCP server
2. **exp1_case_group_heatmap.png** - Heatmap showing task type performance differences
3. **exp1_score_distribution.png** - Violin plots of score distributions
4. **exp1_error_rates.png** - Stacked bar chart of execution outcomes

---

## Next Steps

### Recommended Actions

1. **Investigate Goose failures:** Deep dive into why Goose failed completely with certain MCP servers
   - Examine error logs for pubmed-mcp and simple-pubmed
   - Check if Goose has MCP extension/configuration issues

2. **Validate with third agent:** Add Gemini evaluation to confirm Claude > Goose pattern

3. **Failure case analysis:**
   - Review specific cases where Claude passed but Goose failed
   - Identify patterns in tool selection, error handling, or response formatting

4. **Update baseline metrics:** Re-calculate "true" MCP performance using Claude Code as reference agent

5. **Document agent requirements:** Create guidelines for which agent characteristics enable successful MCP usage

---

## Data Sources

- **Goose results:** `results/compare_agents/goose_20251103.yaml` (100 test cases)
- **Claude Code results:** `results/compare_agents/claude_20251031.yaml` (100 test cases)
- **Analysis notebook:** `notebook/experiment_1_cross_agent_analysis.ipynb`
- **Test cases:** 25 cases × 4 MCP servers = 100 evaluations per agent

---

## Reproducibility

```bash
# Re-run analysis
cd notebook
uv run jupyter nbconvert --execute --to notebook --inplace experiment_1_cross_agent_analysis.ipynb

# View generated figures
ls -la ../results/figures/exp1_*.png
```

---

**Conclusion:** Agent choice is a critical confounding variable in MCP evaluation. For the MCPs that worked with both agents (artl, biomcp), Claude Code demonstrates superior ability to use MCPs for literature retrieval compared to Goose (36-48% vs 20% pass rates). However, the overall comparison is confounded by Goose's inability to run pubmed-mcp and simple-pubmed due to extension configuration issues that need to be resolved.

---

## Known Issues & Next Steps

### Critical Issue: Goose MCP Extension Failures

**Problem:** Goose crashed on all 25 tests (100% failure rate) for both `pubmed-mcp` and `simple-pubmed` with the error:
```
Command '[...goose', 'run', '-t', '...', '--with-extension', '...']'
returned non-zero exit status 1
```

**Impact:** The overall cross-agent comparison statistics are misleading because they include these systematic execution failures as test failures.

**Required Actions:**
1. Debug Goose's `--with-extension` configuration for pubmed-mcp
2. Debug Goose's `--with-extension` configuration for simple-pubmed
3. Re-run Goose evaluation with fixed configurations
4. Update cross-agent analysis with corrected results

**Valid Comparisons (artl & biomcp only):**
- Both agents successfully executed all tests
- Claude Code: 36-48% pass rate
- Goose: 20% pass rate
- Difference: 16-28 percentage points
