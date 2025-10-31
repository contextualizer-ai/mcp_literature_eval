# Experiment 1: Cross-Agent Comparison

## Objective
Determine whether the choice of coding agent (goose-cli, claude-code, gemini-cli) affects MCP retrieval performance, thereby distinguishing MCP-specific failures from agent-specific failures.

## Background
The manuscript currently has a placeholder section "Impact of coding agent" that needs to be filled. The Discussion section notes that agent robustness affects results, with Goose 1.6.0 showing fragility in back-to-back test execution (hanging, incomplete cleanup). This experiment will test whether these issues are Goose-specific or general to all agents.

## Hypothesis
Agent implementation differences (error handling, retry logic, session management) will affect observed MCP performance, particularly in edge cases and sequential test execution.

## Experimental Design

### Variables

**Independent Variable:**
- Coding agent: goose-cli, claude-code, gemini-cli (if available)

**Dependent Variables:**
- Pass rate (% tests passed per MCP)
- Error rate (% tests that errored vs. failed)
- Execution stability (test completion rate)
- Response quality (semantic similarity scores)

**Controlled Variables:**
- Same test suite (25 test cases from `literature_mcp_eval_config.yaml`)
- Same MCPs (artl, biomcp, pubmed-mcp, simple-pubmed)
- Same evaluator model (claude-sonnet-4-20250514)
- Same evaluation metric (CorrectnessMetric with threshold 0.9)

### Test Matrix

```
4 MCPs × 25 test cases × 3 agents = 300 test runs
```

### Execution Plan

#### Step 1: Baseline (Already Complete)
- **Agent:** goose-cli (Goose 1.6.0)
- **Status:** Complete (results in `results/mcp_literature_eval_results_20250917.yaml`)
- **Notes:** Some tests required individual execution due to agent hanging

#### Step 2: claude-code Evaluation
- **Agent:** claude-code (latest version)
- **Config:** Create `literature_mcp_eval_config_claude.yaml` with `claude-code` coder
- **Execution:**
  ```bash
  # Update config to use claude-code
  uv run metacoder run --config project/literature_mcp_eval_config_claude.yaml
  ```
- **Output:** `results/mcp_literature_eval_results_claude_YYYYMMDD.yaml`

#### Step 3: gemini-cli Evaluation (Optional)
- **Agent:** gemini-cli (if available in metacoder)
- **Config:** Create `literature_mcp_eval_config_gemini.yaml` with `gemini-cli` coder
- **Execution:**
  ```bash
  uv run metacoder run --config project/literature_mcp_eval_config_gemini.yaml
  ```
- **Output:** `results/mcp_literature_eval_results_gemini_YYYYMMDD.yaml`

### Configuration Changes

Modify the `coders:` section in the YAML config:

**For claude-code:**
```yaml
coders:
  claude-code: {}
```

**For gemini-cli:**
```yaml
coders:
  gemini-cli: {}
```

Keep all other sections identical to `literature_mcp_eval_config.yaml`.

## Data Collection

### Primary Metrics
For each agent, collect:
1. **Pass/Fail/Error counts** by MCP and case group
2. **Semantic similarity scores** for all test cases
3. **Execution metadata:**
   - Total runtime
   - Number of hangs/timeouts
   - Number of tests requiring re-runs
   - Error messages and failure modes

### Secondary Observations
Document qualitatively:
- Agent behavior during failures (retry attempts, error messages, graceful degradation)
- Session stability (can all 25 tests run sequentially?)
- Output format consistency
- Agent-specific quirks or capabilities

## Analysis Plan

### Quantitative Analysis

1. **Pass Rate Comparison**
   - Create bar chart: `% Passed by MCP and Agent`
   - Statistical test: Chi-square test for independence (agent × pass/fail)

2. **Score Distribution**
   - Box plots of semantic similarity scores by agent
   - Violin plots showing score distributions per MCP and agent
   - Wilcoxon signed-rank test for paired comparisons

3. **Error Analysis**
   - Error rate by agent and case group
   - Classification of error types (timeout, MCP failure, agent crash, etc.)

4. **Case Group Performance**
   - Heatmap: Agent × Case Group → % Passed
   - Identify which case groups show agent-dependent performance

### Qualitative Analysis

5. **Failure Mode Comparison**
   - Review failed test outputs across agents
   - Classify failures using the 5-category system:
     1. Fabricated content
     2. Incorrect but plausible substitution
     3. Truncation presented as complete
     4. Misinterpreted structure
     5. Generative fallback after retrieval failure
   - Determine if certain agents are more prone to specific failure types

6. **Agent Robustness**
   - Compare stability in sequential execution
   - Document which agents handle edge cases (NBK1256, PMC117972) better
   - Assess retry logic and error recovery

## Visualization Plan

### Figure 1: Overall Performance by Agent
- Grouped bar chart: MCP on x-axis, % Passed on y-axis, grouped by agent
- Shows if any agent consistently outperforms others

### Figure 2: Case Group Performance Heatmap
- Rows: Case groups (Metadata, Text extraction, etc.)
- Columns: Agents
- Cell color: % Passed
- Reveals which task types are agent-sensitive

### Figure 3: Score Distribution Violin Plots
- One violin per agent, showing distribution of similarity scores
- Overlay with box plot showing median and quartiles
- Identifies if agents differ in scoring patterns

### Figure 4: Error Rate Comparison
- Stacked bar chart: Error types (timeout, crash, MCP fail) by agent
- Shows agent stability differences

## Expected Outcomes

### If Agent Choice Matters Significantly:
- Pass rates differ by >20% between agents for same MCP
- Certain case groups (e.g., "Text extraction") show agent-dependent performance
- Some agents handle edge cases (NBK1256, PMC117972) better than others
- Implies: Observed failures in baseline may be agent-specific, not MCP-specific

### If Agent Choice Doesn't Matter:
- Pass rates within ±5% across agents for same MCP
- Similar error rates and failure modes
- Implies: Current results reflect true MCP limitations, not agent artifacts

### If Agent Choice Matters for Stability Only:
- Similar pass rates but different error rates
- Some agents complete all tests sequentially, others require re-runs
- Implies: Agent robustness is important for practical use but doesn't affect MCP capability assessment

## Integration with Manuscript

### New Content for "Impact of coding agent" Section

Replace the placeholder with:

```markdown
To assess whether observed MCP performance reflected inherent retrieval
limitations or agent orchestration artifacts, we repeated the evaluation
using three different coding agents: goose-cli (Goose 1.6.0), claude-code,
and gemini-cli. All agents executed the identical test suite against the
same four MCPs and were evaluated using the same model (claude-sonnet-4-20250514)
and metric (CorrectnessMetric, threshold 0.9).

[Insert findings: e.g., "Agent choice had minimal impact on pass rates
(within ±X%), suggesting that observed failures reflect MCP limitations
rather than agent artifacts. However, agent robustness varied substantially:
claude-code completed all 100 test runs without hanging, while goose-cli
required manual intervention on Y% of cases."]

Figure X shows [insert figure description].

These results indicate that [conclusion about agent impact].
```

### Updates to Discussion Section

Add paragraph:

```markdown
The cross-agent comparison revealed that [agent impact summary]. This finding
has important implications for MCP evaluation methodology: [implications].
Future evaluations should consider [recommendations for agent selection].
```

## Timeline

- **Week 1:** Configure claude-code tests, execute runs
- **Week 2:** Configure gemini-cli tests (if available), execute runs
- **Week 3:** Data analysis and visualization
- **Week 4:** Manuscript integration

## Potential Challenges

1. **Agent availability:** Gemini-cli may not be available in metacoder yet
2. **Agent-specific config:** Some agents may require different environment setup
3. **Timeout behavior:** Agents may have different default timeouts for MCP calls
4. **Cost:** Running 100-300 additional test cases may incur API costs

## Success Criteria

This experiment succeeds if it:
1. Generates data to fill the "[AUTHOR to fill]" section
2. Determines whether agent choice confounds MCP evaluation
3. Provides actionable guidance for future MCP evaluation methodology
4. Produces at least 2 publication-quality figures

## References to Existing Data

- Baseline results: `results/mcp_literature_eval_results_20250917.yaml`
- Test configuration: `project/literature_mcp_eval_config.yaml`
- Visualization notebook: `notebook/visualize_results_yaml_executed.ipynb`
