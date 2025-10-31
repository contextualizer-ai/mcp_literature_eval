# Experiment 2: Cross-Model Evaluation

## Objective
Validate evaluation reliability by determining whether the choice of evaluator model affects performance assessment of MCP outputs, thereby addressing potential model-specific bias in the evaluation framework.

## Background
The manuscript acknowledges: "there exists a risk of model-specific bias" because claude-sonnet-4-20250514 was used both to generate responses (via the coding agent) and to evaluate them (via DeepEval metrics). An evaluator model may be more tolerant of its own phrasing conventions or failure modes, potentially inflating apparent performance. This experiment tests whether evaluation scores are robust across different judge models.

## Hypothesis
Different evaluator models will produce similar pass/fail decisions and semantic similarity scores when judging the same MCP outputs, indicating robust evaluation. Alternatively, systematic differences may reveal evaluator bias or task-specific model capabilities.

## Experimental Design

### Variables

**Independent Variable:**
- Evaluator model: claude-sonnet-4, claude-opus, claude-haiku, GPT-4 (if accessible)

**Dependent Variables:**
- Semantic similarity scores (0-1 scale)
- Pass/fail decisions (using threshold 0.9)
- Inter-model agreement (Cohen's kappa, Pearson correlation)

**Controlled Variables:**
- Same MCP outputs (from `results/mcp_literature_eval_results_20250917.yaml`)
- Same test cases (25 cases)
- Same evaluation metric (CorrectnessMetric)
- Same threshold (0.9)
- Same expected outputs

### Key Insight: Re-evaluation Without Re-retrieval
This experiment is **efficient** because:
- We already have MCP outputs from the baseline run (20250917)
- We don't need to call MCPs again—just re-evaluate existing responses
- This tests evaluator bias independently from MCP capability

### Test Matrix

```
4 MCPs × 25 test cases × 4 evaluator models = 400 evaluations
(but only ~100 unique MCP outputs to re-score)
```

## Execution Plan

### Step 1: Extract Baseline Outputs

Create a script to parse `mcp_literature_eval_results_20250917.yaml` and extract:
- Test case name
- MCP server
- Actual output (the text response from the MCP)
- Expected output
- Original score (from claude-sonnet-4)
- Original pass/fail decision

Save as: `data/baseline_outputs_20250917.json`

```python
import yaml
import json

# Load baseline results
with open('results/mcp_literature_eval_results_20250917.yaml', 'r') as f:
    baseline = yaml.safe_load(f)

# Extract outputs for re-evaluation
outputs = []
for result in baseline['results']:
    outputs.append({
        'case_name': result['name'],
        'case_group': result.get('case_group'),
        'mcp_servers': result['servers'],
        'input_prompt': result.get('input'),
        'expected_output': result.get('expected_output'),
        'actual_output': result.get('actual_output'),
        'original_score': result.get('score'),
        'original_passed': result.get('passed'),
        'original_evaluator': 'claude-sonnet-4-20250514'
    })

with open('data/baseline_outputs_20250917.json', 'w') as f:
    json.dump(outputs, f, indent=2)
```

### Step 2: Configure Evaluator Models

Create evaluation configs for each model:

**Config 1: Claude Opus** (`eval_config_opus.yaml`)
```yaml
name: cross-model evaluation - opus
description: Re-evaluate baseline outputs with Claude Opus

models:
  claude-opus:
    provider: anthropic
    name: claude-opus-4-20250514  # Use latest Opus version

# Load test cases from baseline outputs
# (Implementation detail: adapt metacoder to accept pre-generated outputs)
```

**Config 2: Claude Haiku** (`eval_config_haiku.yaml`)
```yaml
models:
  claude-haiku:
    provider: anthropic
    name: claude-haiku-4-20250514  # Use latest Haiku version
```

**Config 3: GPT-4** (`eval_config_gpt4.yaml`)
```yaml
models:
  gpt-4:
    provider: openai
    name: gpt-4-turbo-2024-04-09  # Or latest available
```

### Step 3: Re-evaluation Pipeline

Two approaches:

#### Approach A: Use DeepEval Directly (Recommended)
Bypass metacoder and call DeepEval's CorrectnessMetric directly for each evaluator:

```python
from deepeval.metrics import CorrectnessMetric
from deepeval.test_case import LLMTestCase
import json

# Load baseline outputs
with open('data/baseline_outputs_20250917.json', 'r') as f:
    outputs = json.load(f)

# Define evaluator models
evaluators = [
    ('claude-opus', 'claude-opus-4-20250514'),
    ('claude-haiku', 'claude-haiku-4-20250514'),
    ('gpt-4', 'gpt-4-turbo-2024-04-09')
]

results = []

for eval_name, model_name in evaluators:
    print(f"\nEvaluating with {eval_name}...")

    for output in outputs:
        # Create test case
        test_case = LLMTestCase(
            input=output['input_prompt'],
            actual_output=output['actual_output'],
            expected_output=output['expected_output']
        )

        # Create metric with this evaluator
        metric = CorrectnessMetric(
            threshold=0.9,
            model=model_name  # Specify evaluator model
        )

        # Measure
        metric.measure(test_case)

        # Store result
        results.append({
            'case_name': output['case_name'],
            'case_group': output['case_group'],
            'mcp_servers': output['mcp_servers'],
            'evaluator': eval_name,
            'evaluator_model': model_name,
            'score': metric.score,
            'passed': metric.score >= 0.9,
            'reason': metric.reason,
            'original_score': output['original_score'],
            'original_passed': output['original_passed']
        })

# Save results
with open('results/cross_model_evaluation_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

#### Approach B: Modify Metacoder Config (If Supported)
If metacoder supports loading pre-generated outputs, create a config that skips MCP calls and only runs evaluation.

### Step 4: Execute Re-evaluation

```bash
# Create data directory if needed
mkdir -p data

# Extract baseline outputs
python scripts/extract_baseline_outputs.py

# Run re-evaluation with multiple models
python scripts/cross_model_reevaluation.py

# Expected output: results/cross_model_evaluation_results.json
```

## Data Collection

### Primary Data Structure

For each test case × MCP × evaluator combination, record:
```json
{
  "case_name": "PMID_28027860_Full_Text",
  "case_group": "Text extraction",
  "mcp_server": "artl",
  "actual_output": "[MCP response text]",
  "expected_output": "[Expected text]",
  "evaluators": {
    "claude-sonnet-4": {"score": 0.85, "passed": false, "reason": "..."},
    "claude-opus": {"score": 0.88, "passed": false, "reason": "..."},
    "claude-haiku": {"score": 0.82, "passed": false, "reason": "..."},
    "gpt-4": {"score": 0.91, "passed": true, "reason": "..."}
  },
  "inter_model_agreement": 0.75  // Cohen's kappa or similar
}
```

### Metrics to Compute

1. **Score Correlation:** Pearson correlation between evaluator pairs
2. **Pass/Fail Agreement:** Cohen's kappa between evaluator pairs
3. **Score Variance:** Std dev of scores across evaluators per test case
4. **Disagreement Cases:** Test cases where evaluators disagree on pass/fail

## Analysis Plan

### Quantitative Analysis

#### 1. Inter-Model Agreement

**Correlation Matrix:**
- Compute Pearson correlation of scores between all evaluator pairs
- Create heatmap showing correlations
- Expected: r > 0.85 indicates high agreement

**Cohen's Kappa:**
- Compute kappa for pass/fail decisions between evaluator pairs
- Interpretation:
  - κ < 0.40: Poor agreement
  - 0.40 ≤ κ < 0.60: Moderate agreement
  - 0.60 ≤ κ < 0.80: Substantial agreement
  - κ ≥ 0.80: Almost perfect agreement

#### 2. Score Distribution Analysis

**Box Plots:**
- Box plot of scores by evaluator model
- Shows if certain models are systematically more/less generous

**Bland-Altman Plots:**
- Plot mean score vs. difference in scores for each evaluator pair
- Identifies systematic bias (one model consistently higher/lower)

#### 3. Pass Rate Comparison

**Contingency Tables:**
- For each evaluator pair, create 2×2 table:
  ```
              Eval2 Pass | Eval2 Fail
  Eval1 Pass     a      |     b
  Eval1 Fail     c      |     d
  ```
- Compute agreement rate: (a + d) / (a + b + c + d)

#### 4. Disagreement Analysis

**Identify High-Variance Cases:**
- Find test cases where evaluator scores have high std dev (>0.2)
- Examine actual outputs for these cases
- Classify why evaluators disagreed

**Case Group Sensitivity:**
- Compute inter-evaluator agreement by case group
- Determine if certain task types show more evaluator disagreement

### Qualitative Analysis

#### 5. Evaluator Reasoning Comparison

For disagreement cases, compare the `reason` field from CorrectnessMetric:
- Do evaluators cite different aspects of the output?
- Do some evaluators focus on semantic meaning vs. exact wording?
- Are certain evaluators more tolerant of formatting differences?

#### 6. Systematic Bias Detection

Check if certain evaluators are:
- **More lenient:** Higher scores across all test cases
- **More strict:** Lower scores across all test cases
- **Task-specific:** Better at certain case groups (e.g., Metadata vs. Text extraction)

## Visualization Plan

### Figure 1: Inter-Model Correlation Heatmap
- 4×4 heatmap showing Pearson correlations between evaluator models
- Color scale: 0 (white) to 1 (dark blue)
- Annotate cells with correlation coefficients

### Figure 2: Score Distribution by Evaluator
- Four box plots (one per evaluator model)
- Shows median, quartiles, and outliers
- Overlay individual points with jitter for visibility

### Figure 3: Bland-Altman Plots (3 subplots)
- Compare baseline (claude-sonnet-4) against each other evaluator:
  - (a) Sonnet vs. Opus
  - (b) Sonnet vs. Haiku
  - (c) Sonnet vs. GPT-4
- x-axis: Mean score
- y-axis: Difference in scores
- Shows systematic bias and agreement limits

### Figure 4: Agreement Matrix
- Heatmap showing pass/fail agreement (Cohen's kappa) between evaluator pairs
- Similar to Figure 1 but for categorical decisions

### Figure 5: High-Variance Cases
- Bar chart of test cases with std dev > 0.2 across evaluators
- Grouped by case group
- Identifies which test cases are most evaluator-sensitive

## Expected Outcomes

### Scenario 1: High Agreement (Preferred)
- Pearson r > 0.85 between all evaluator pairs
- Cohen's κ > 0.70 for pass/fail decisions
- Low variance in scores per test case (std dev < 0.1)
- **Implication:** Evaluation is robust; original results are trustworthy

### Scenario 2: Moderate Agreement
- Pearson r = 0.70–0.85
- Cohen's κ = 0.50–0.70
- Some test cases show high variance
- **Implication:** Evaluation is generally reliable but some edge cases are evaluator-dependent

### Scenario 3: Low Agreement (Concerning)
- Pearson r < 0.70
- Cohen's κ < 0.50
- High variance across many test cases
- **Implication:** Evaluator choice significantly affects conclusions; need to:
  - Use ensemble evaluation (average scores across models)
  - Revise expected outputs to be less ambiguous
  - Use multiple evaluators and report ranges

### Scenario 4: Systematic Bias
- High correlation but systematic offset (one model always higher/lower)
- Bland-Altman plots show non-zero mean difference
- **Implication:** Some models are more lenient/strict; need to adjust thresholds or use ensemble

## Integration with Manuscript

### Update Methods Section

Add to "Evaluation using metacoder" subsection:

```markdown
To assess evaluation robustness and potential model-specific bias, we
re-evaluated all MCP outputs using four different LLM judges: claude-sonnet-4
(baseline), claude-opus-4, claude-haiku-4, and GPT-4. Each evaluator
independently scored the same set of actual outputs against expected outputs
using DeepEval's CorrectnessMetric with threshold 0.9. This approach allowed
us to measure inter-evaluator agreement without re-running MCP retrievals.
```

### Add New Results Subsection: "Evaluator Robustness"

```markdown
## Evaluator Robustness

To determine whether evaluation scores were dependent on the choice of judge
model, we re-evaluated all baseline outputs using four different evaluators
(Figure X). Inter-evaluator agreement was [high/moderate/low], with Pearson
correlations ranging from [min] to [max] (Figure Xa) and Cohen's kappa for
pass/fail decisions ranging from [min] to [max] (Figure Xb).

[If high agreement:]
The strong agreement across evaluators (mean κ = X.XX, mean r = X.XX)
indicates that evaluation results are robust to evaluator choice, validating
our baseline findings.

[If moderate agreement:]
While evaluators showed moderate overall agreement (mean κ = X.XX), certain
test cases exhibited high score variance (Figure Xc). These high-variance
cases were concentrated in [case groups], suggesting that [interpretation].

[If systematic bias detected:]
Bland-Altman analysis revealed systematic bias, with [model X] consistently
scoring [higher/lower] than [model Y] by an average of [difference] points
(Figure Xd). This bias was most pronounced in [case group] tasks.

[Always include:]
These findings highlight the importance of [conclusions about evaluation
methodology for MCP assessment].
```

### Update Discussion Section

Add paragraph:

```markdown
The cross-model evaluation experiment addressed concerns about model-specific
bias in our assessment framework. [Summary of findings]. This has important
implications for developing standardized MCP benchmarks: [implications].
We recommend that future evaluations [recommendations for multi-evaluator
approaches or evaluation best practices].
```

## Timeline

- **Week 1:** Extract baseline outputs, set up re-evaluation pipeline
- **Week 2:** Run re-evaluations with all four models
- **Week 3:** Statistical analysis and correlation/agreement metrics
- **Week 4:** Visualization and manuscript integration

## Potential Challenges

1. **API Access:** May need OpenAI API key for GPT-4 evaluation
2. **Cost:** Re-evaluating 100+ outputs with multiple models (but much cheaper than re-running MCP retrievals)
3. **DeepEval Compatibility:** Ensure DeepEval supports specifying evaluator model
4. **Metacoder Integration:** May need to bypass metacoder and use DeepEval directly

## Success Criteria

This experiment succeeds if it:
1. Quantifies inter-evaluator agreement with statistical rigor
2. Identifies and characterizes any systematic evaluator bias
3. Provides evidence for or against the "model-specific bias" concern
4. Produces actionable recommendations for MCP evaluation methodology
5. Generates at least 3 publication-quality figures

## Code Deliverables

1. `scripts/extract_baseline_outputs.py` - Extract outputs from baseline YAML
2. `scripts/cross_model_reevaluation.py` - Re-evaluate with multiple models
3. `scripts/analyze_evaluator_agreement.py` - Compute correlations, kappa, etc.
4. `notebook/cross_model_evaluation_analysis.ipynb` - Visualization and analysis
5. `results/cross_model_evaluation_results.json` - Raw results
6. `results/evaluator_agreement_stats.json` - Computed statistics

## References to Existing Data

- Baseline results: `results/mcp_literature_eval_results_20250917.yaml`
- Test configuration: `project/literature_mcp_eval_config.yaml`
- Existing visualization: `notebook/visualize_results_yaml_executed.ipynb`

## Notes

This experiment is particularly valuable because:
- It's **low cost** (no MCP re-runs needed)
- It's **high impact** (addresses a major methodological concern)
- It's **generalizable** (findings apply to all LLM-based evaluation)
- It's **publishable** (contributes to evaluation methodology literature)
