# Notebooks Guide

Quick reference for the analysis notebooks in this project.

---

## Available Notebooks

### 1. Metacoder Fixes Documentation

**File:** `notebook/metacoder_fixes_documentation.ipynb`

**Purpose:** Documents all fixes made to the metacoder framework for Goose and Claude coders.

**Contains:**
- Detailed problem statements with evidence
- Root cause analysis for each bug
- Code fixes with line-by-line explanations
- Before/after performance comparisons
- Patch file references for upstream PRs
- Lessons learned and recommendations

**When to Use:**
- Understanding what bugs were fixed
- Preparing upstream PRs to metacoder
- Documenting methodology for manuscript
- Training others on the evaluation framework

**Key Sections:**
1. Goose MCP Extension Loading Bug (CRITICAL)
2. Claude Evaluation Crash Bug
3. Patch files for upstream contribution
4. Impact analysis
5. Recommendations

**Can Execute?** Yes - includes code cells to load and analyze Goose results

---

### 2. Cross-Agent Comparison Analysis

**File:** `notebook/experiment_1_cross_agent_analysis.ipynb`

**Purpose:** Compare MCP performance across different coding agents (goose, claude-code, gemini).

**Current Status:**
- ✅ Goose results loaded: `results/compare_agents/goose_20251103.yaml`
- ⏳ Claude results: Not yet generated
- ⏳ Gemini results: Not yet generated

**Analyses Included:**
1. Overall performance by agent (grouped bar charts)
2. Case group performance heatmap (which tasks are agent-sensitive)
3. Score distribution comparison (violin plots)
4. Error rate analysis (stacked bar charts)
5. Statistical tests (chi-square, Wilcoxon)
6. Key findings summary

**Generated Outputs:**
- `results/figures/exp1_overall_performance_by_agent.png`
- `results/figures/exp1_case_group_heatmap.png`
- `results/figures/exp1_score_distribution.png`
- `results/figures/exp1_error_rates.png`

**When to Use:**
- After completing evaluations for 2+ agents
- Comparing agent performance on same test cases
- Identifying which agents work best with which MCPs
- Generating figures for manuscript

**To Run:**
1. Ensure result files exist for agents you want to compare
2. Uncomment desired agents in cell-3
3. Execute all cells
4. Figures saved to `results/figures/`

**Can Execute Now?** Yes - works with just Goose results (will show single-agent stats)

---

## Running the Notebooks

### Prerequisites

```bash
# Install Jupyter if needed
uv add jupyter matplotlib seaborn pandas pyyaml scipy

# Or run via uv
uv run jupyter notebook
```

### Quick Start

```bash
# Navigate to notebook directory
cd notebook/

# Launch Jupyter
uv run jupyter notebook

# Or use JupyterLab
uv run jupyter lab
```

### Running Specific Notebook

```bash
# From project root
uv run jupyter notebook notebook/metacoder_fixes_documentation.ipynb
```

---

## Notebook Cell Execution Guide

### Metacoder Fixes Documentation

**Order to execute:**
1. Cell 1-2: Imports and setup
2. Cell 3+: Read and execute sequentially
3. Patch file display cells will show actual patch contents

**Expected outputs:**
- Patch file contents displayed
- Goose results summary statistics
- Before/after comparisons

### Cross-Agent Comparison Analysis

**Order to execute:**
1. Cell 1-2: Imports and setup
2. Cell 3: Load results (checks which files exist)
3. Cell 4-5: Create combined dataframe
4. Cells 6-17: Generate analyses and plots (execute in order)

**Expected outputs:**
- Confirmation messages for loaded results
- Statistical summaries printed
- Plots displayed inline
- Figures saved to `results/figures/`

**If only Goose results available:**
- Notebook will load only Goose data
- Cross-agent comparisons will be skipped (not enough agents)
- Single-agent statistics will still work
- Uncomment other agents in cell-3 when results available

---

## Troubleshooting

### "File not found" errors

**Problem:** Result files don't exist at expected paths

**Solution:**
1. Check if evaluation has been run
2. Verify file path in notebook matches actual location
3. Update cell-3 in cross-agent notebook with correct paths

### Import errors

**Problem:** Missing packages (matplotlib, seaborn, etc.)

**Solution:**
```bash
uv add jupyter matplotlib seaborn pandas pyyaml scipy
```

### Empty plots or missing data

**Problem:** Results file exists but contains no data

**Solution:**
1. Check if evaluation completed successfully
2. Verify YAML file is valid: `python -c "import yaml; yaml.safe_load(open('path/to/file.yaml'))"`
3. Check file size - should be several MB for 100 tests

### Statistical tests fail

**Problem:** Not enough agents for pairwise comparisons

**Solution:**
- Normal when only 1 agent's results available
- Tests will run automatically when 2+ agents loaded
- Ignore warnings about insufficient data

---

## Adding Results for New Agents

### Step 1: Run Evaluation

```bash
# For Claude
export OPENAI_API_KEY=$(cat ~/openai.key)
uv run metacoder eval project/literature_mcp_eval_config_claude.yaml \
  -o results/compare_agents/claude_20251103.yaml

# For Gemini
export OPENAI_API_KEY=$(cat ~/openai.key)
uv run metacoder eval project/literature_mcp_eval_config_gemini.yaml \
  -o results/compare_agents/gemini_20251103.yaml
```

### Step 2: Update Notebook

Edit `experiment_1_cross_agent_analysis.ipynb` cell-3:

```python
result_files = {
    'goose': '../results/compare_agents/goose_20251103.yaml',
    'claude-code': '../results/compare_agents/claude_20251103.yaml',  # Uncomment
    # 'gemini': '../results/compare_agents/gemini_20251103.yaml',  # Uncomment when ready
}
```

### Step 3: Re-run Analysis

- Execute all cells in order
- New plots will include all loaded agents
- Statistical tests will run if 2+ agents available

---

## Output Files

### Figures Directory

All plots saved to `results/figures/` with naming convention:
- `exp1_overall_performance_by_agent.png` - Bar chart of pass rates
- `exp1_case_group_heatmap.png` - Heatmap of performance by task type
- `exp1_score_distribution.png` - Violin plots of score distributions
- `exp1_error_rates.png` - Stacked bars showing pass/fail/error counts

**Format:** PNG, 300 DPI, publication-quality

### Notebook Outputs

Notebooks can be exported with outputs preserved:

```bash
# Export to HTML
uv run jupyter nbconvert --to html notebook/metacoder_fixes_documentation.ipynb

# Export to PDF (requires LaTeX)
uv run jupyter nbconvert --to pdf notebook/metacoder_fixes_documentation.ipynb
```

---

## Best Practices

### Before Running Analysis

1. ✅ Verify all result files exist
2. ✅ Check file sizes (should be ~4-5 MB for 100 tests)
3. ✅ Validate YAML syntax
4. ✅ Clear old outputs: `Kernel → Restart & Clear Output`

### During Execution

1. Run cells in order (don't skip cells)
2. Wait for each cell to complete before running next
3. Check for errors in cell outputs
4. Verify plots display correctly

### After Execution

1. Save notebook with outputs: `File → Save`
2. Export to HTML for sharing
3. Check that figures were saved to `results/figures/`
4. Review statistical test results for significance

---

## Integration with Manuscript

### Figures to Include

From `experiment_1_cross_agent_analysis.ipynb`:
- Overall performance comparison (Figure 1)
- Case group heatmap (Figure 2)
- Score distributions (Figure 3 or supplementary)
- Error analysis (Table 1 or supplementary)

### Tables to Generate

- Summary statistics by agent
- Pass rates by MCP server and agent
- Statistical test results (chi-square, Wilcoxon p-values)

### Text to Extract

- Key findings section (cell-17)
- Statistical significance statements
- Performance differences (percentage points)

---

## Future Enhancements

### Potential New Notebooks

1. **MCP Server Deep Dive**
   - Analyze each MCP server individually
   - Compare performance across agents
   - Identify server-specific issues

2. **Failure Mode Analysis**
   - Categorize failures: MCP vs agent vs compound
   - Qualitative analysis of error messages
   - Recommendations for improvement

3. **Prompt Engineering Experiments**
   - Test different prompt strategies
   - Compare retrieval success rates
   - Optimize for specific agents

4. **Longitudinal Analysis**
   - Track performance over time
   - Compare different versions of agents/MCPs
   - Identify improvements or regressions

---

**Last Updated:** 2025-11-03
**Notebooks Version:** 1.0
**Next Update:** After Claude evaluation completes
