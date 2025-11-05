# Experiment 2: Cross-Model Evaluation (Goose Agent)

## Objective
Determine whether the choice of underlying LLM model affects MCP retrieval performance when using the same coding agent (Goose).

## Background
Experiment 1 showed that **agent choice significantly affects performance** (Claude Code: 47%, Gemini: 16%, Goose with gpt-4o: 15%). This experiment tests whether the poor Goose performance was due to the agent architecture or the underlying model (gpt-4o).

## Hypothesis
Different underlying models will produce different MCP retrieval performance even when using the same agent (Goose), indicating that model choice is a critical factor independent of agent architecture.

## Experimental Design

### Variables

**Independent Variable:**
- Underlying LLM model used by Goose agent:
  - gpt-4o (OpenAI, used in Experiment 1)
  - gpt-5 (OpenAI, latest flagship model)
  - claude-sonnet-4-20250514 (Anthropic)

**Dependent Variables:**
- Semantic similarity scores (0-1 scale)
- Pass/fail decisions (using threshold 0.9)
- Pass rate by MCP server
- Pass rate by case group

**Controlled Variables:**
- Same agent (Goose CLI)
- Same MCP servers (artl, simple-pubmed, biomcp, pubmed-mcp)
- Same test cases (25 cases × 4 MCPs = 100 evaluations)
- Same evaluation metric (CorrectnessMetric)
- Same threshold (0.9)
- Same environment variables (PUBMED_EMAIL, PUBMED_API_KEY)

### Test Matrix

```
3 models × 4 MCPs × 25 test cases = 300 evaluations
```

## Execution Plan

### Configurations Created

1. **Goose + gpt-4o** (baseline from Experiment 1)
   - Config: `literature_mcp_eval_config.yaml`
   - Run script: `run_goose_eval.sh`
   - Results: `results/compare_models/goose_gpt4o_20251104.yaml`
   - Status: ✅ Complete (reused from Experiment 1)

2. **Goose + gpt-5** (new)
   - Config: `literature_mcp_eval_config_goose_gpt5.yaml`
   - Run script: `run_goose_gpt5_eval.sh`
   - Results: `results/compare_models/goose_gpt5_$(date).yaml`
   - Status: 🔄 Running

3. **Goose + claude-sonnet-4** (new)
   - Config: `literature_mcp_eval_config_goose_claude.yaml`
   - Run script: `run_goose_claude_eval.sh`
   - Results: `results/compare_models/goose_claude_$(date).yaml`
   - Status: 🔄 Running

### Model Configuration Details

Each Goose config specifies the model via environment variables:

```yaml
coders:
  goose:
    env:
      GOOSE_MODEL: [model-name]
      GOOSE_PROVIDER: [openai|anthropic]
```

**gpt-5 config:**
```yaml
GOOSE_MODEL: gpt-5
GOOSE_PROVIDER: openai
```

**claude-sonnet-4 config:**
```yaml
GOOSE_MODEL: claude-sonnet-4-20250514
GOOSE_PROVIDER: anthropic
```

## Expected Timeline

- **Test duration**: ~30-40 minutes per model (100 tests)
- **Total runtime**: ~1.5 hours for both new models
- **Analysis**: ~30 minutes
- **Total**: ~2 hours

## Analysis Plan

### Primary Metrics

1. **Overall Pass Rates**
   - Compare % passed across the three models
   - Identify best-performing model with Goose

2. **MCP-Specific Performance**
   - Pass rates by MCP server for each model
   - Determine if certain MCPs work better with certain models

3. **Case Group Performance**
   - Pass rates by task type (Text extraction, Metadata, etc.)
   - Identify model strengths and weaknesses

4. **Statistical Comparison**
   - Chi-square test for independence
   - Effect size calculation

### Visualization Plan

1. **Figure 1: Overall Performance Comparison**
   - Grouped bar chart: 3 models × 4 MCPs
   - Shows pass rates for each model-MCP combination

2. **Figure 2: Case Group Heatmap**
   - Rows: Case groups
   - Columns: Models
   - Values: % passed
   - Identifies task-specific model performance

3. **Figure 3: Score Distribution**
   - Violin/box plots for each model
   - Shows score distributions and variability

## Comparison with Experiment 1

| Experiment | Focus | Variables | Agent(s) | Model(s) |
|------------|-------|-----------|----------|----------|
| **Experiment 1** | Agent choice | Agent architecture | Claude Code, Gemini CLI, Goose | Fixed per agent |
| **Experiment 2** | Model choice | Underlying LLM | Goose only | gpt-4o, gpt-5, claude-sonnet-4 |

Key question: **Is Goose's poor performance (15%) due to the agent or the model?**

If claude-sonnet-4 with Goose achieves ~47% (matching Claude Code), this suggests:
- The agent architecture is comparable
- The model is the critical factor
- gpt-4o may be less effective for this task

If all three models achieve ~15% with Goose, this suggests:
- The Goose agent architecture is the limiting factor
- Model choice has minimal impact
- Agent design matters more than model choice

## Expected Outcomes

### Scenario 1: Model Matters More Than Agent
- **Goose + claude-sonnet-4**: ~40-50% pass rate (similar to Claude Code)
- **Goose + gpt-5**: ~30-40% pass rate
- **Goose + gpt-4o**: ~15% pass rate (baseline)
- **Implication**: Model choice is critical; Goose agent is fine

### Scenario 2: Agent Matters More Than Model
- **All three models**: ~10-20% pass rate
- **Implication**: Goose agent architecture limits performance regardless of model

### Scenario 3: Mixed Effects
- **Goose + claude-sonnet-4**: ~25-35% (better but not matching Claude Code)
- **Goose + gpt-5**: ~20-30%
- **Goose + gpt-4o**: ~15%
- **Implication**: Both agent and model matter; interaction effects present

## Success Criteria

This experiment succeeds if it:
1. Quantifies the impact of model choice on Goose performance
2. Determines whether Goose + claude-sonnet-4 can match Claude Code performance
3. Provides evidence for agent vs. model importance
4. Generates publication-quality comparison visualizations
5. Informs recommendations for MCP agent selection

## Integration with Manuscript

### Methods Section Addition

```markdown
To isolate the effect of underlying LLM model from agent architecture, we
conducted a cross-model evaluation using Goose CLI with three different models:
gpt-4o (baseline), gpt-5, and claude-sonnet-4-20250514. This design allows us
to determine whether the agent's architecture or the underlying model primarily
drives MCP retrieval performance.
```

### Results Section Addition

```markdown
## Cross-Model Performance (Goose Agent)

Using Goose CLI with different underlying models revealed [finding about model
importance]. Goose with claude-sonnet-4 achieved [X]% pass rate compared to
[Y]% with gpt-4o and [Z]% with gpt-5 (Figure X). This [X-point difference]
[suggests/does not suggest] that model choice is a [primary/secondary] factor
in MCP retrieval performance.

[Comparison to Experiment 1 findings about agent choice vs. model choice]
```

## Notes

- This experiment reuses the Goose MCP configuration fixes from Experiment 1 (PUBMED_EMAIL, PUBMED_API_KEY environment variables)
- All evaluations use the same metacoder version and evaluation metrics
- Results will be stored in `results/compare_models/` to distinguish from Experiment 1 (agent comparison)

## File Structure

```
project/
  literature_mcp_eval_config_goose_gpt5.yaml    # GPT-5 config
  literature_mcp_eval_config_goose_claude.yaml  # Claude config
  literature_mcp_eval_config.yaml               # gpt-4o (from Exp1)

run_goose_gpt5_eval.sh                          # Run GPT-5 evaluation
run_goose_claude_eval.sh                        # Run Claude evaluation
run_goose_eval.sh                               # Run gpt-4o (from Exp1)

results/compare_models/
  goose_gpt4o_20251104.yaml                     # gpt-4o results
  goose_gpt5_20251104.yaml                      # GPT-5 results (pending)
  goose_claude_20251104.yaml                    # Claude results (pending)
```
