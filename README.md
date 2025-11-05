# MCP Literature Evaluation

Systematic evaluation framework for assessing Model Context Protocol (MCP) servers that provide access to scientific literature.

## Overview

This project evaluates multiple literature MCP servers across defined test cases spanning title retrieval, table extraction, conclusion parsing, and content summarization. We use DeepEval's Correctness and Hallucination metrics to evaluate performance on challenging tasks in scientific information retrieval.

## MCP Servers Evaluated

- **[artl-mcp](https://github.com/contextualizer-ai/artl-mcp)** - Simple MCP for retrieving literature using DOI, PMC, PMID
- **[biomcp](https://github.com/genomoncology/biomcp)** - Specialized biomedical knowledge from authoritative sources
- **[simple-pubmed](https://github.com/andybrandt/mcp-simple-pubmed)** - PubMed search with field-specific queries
- **[pubmed-mcp](https://github.com/chrismannina/pubmed-mcp)** - Advanced PubMed access with filtering

## Installation

```bash
# Clone the repository
git clone https://github.com/contextualizer-ai/mcp_literature_eval.git
cd mcp_literature_eval

# Install dependencies with uv
uv sync
```

## Dependencies

This project uses a specific branch of [metacoder](https://github.com/ai4curation/metacoder) for evaluation:

```bash
# To update metacoder
uv lock --upgrade-package metacoder
uv sync --reinstall
```

## Running Evaluations

**Use the Jupyter notebooks** to run evaluations and generate visualizations. The notebooks provide step-by-step instructions with environment setup, execution commands, and progress monitoring.

### Experiment 1: Cross-Agent Comparison

Compare MCP performance across different coding agents:

1. **Run evaluations:** `notebook/experiment_1_run_evaluations.ipynb`
   - Claude Code agent
   - Goose agent
   - Gemini CLI agent

2. **Analyze results:** `notebook/experiment_1_cross_agent_analysis.ipynb`
   - Pass rate comparisons
   - Statistical tests
   - Publication-quality figures

### Experiment 2: Cross-Model Comparison

Compare MCP performance across different LLM models using Goose agent:

1. **Run evaluations:** `notebook/experiment_2_run_evaluations.ipynb`
   - gpt-4o
   - gpt-5
   - gpt-4o-mini

2. **Analyze results:** `notebook/experiment_2_cross_model_analysis.ipynb`
   - Model performance comparison
   - Score distributions
   - Cross-experiment analysis

### Manual Execution (Advanced)

For manual runs or custom configurations:

```bash
# Example: Run gpt-4o-mini evaluation
export OPENAI_API_KEY=$(cat ~/openai.key)
export PUBMED_EMAIL=justinreese@lbl.gov
export PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808

uv run metacoder eval project/literature_mcp_eval_config_goose_gpt4o_mini.yaml \
  -o results/compare_models/goose_gpt4o_mini_$(date +%Y%m%d).yaml
```

**Duration:** Each full evaluation takes 2-3 hours (100 evaluations).

**Directory Structure:**
- `results/compare_agents/` - Cross-agent evaluation results (Experiment 1)
- `results/compare_models/` - Cross-model evaluation results (Experiment 2)
- `results/figures/` - Generated plots from analysis notebooks

### Environment Variables

#### Required API Keys

**For MCP servers:**
Some MCPs require API keys or contact information:

```bash
export PUBMED_EMAIL="your.email@example.com"
export PUBMED_API_KEY="your_api_key_here"
```

**For evaluation metrics:**
DeepEval uses OpenAI for the CorrectnessMetric evaluator. Set the API key:

```bash
# Load from file (recommended)
export OPENAI_API_KEY=$(cat ~/openai.key)

# Or set directly
export OPENAI_API_KEY="sk-proj-..."
```

Or configure MCP-specific settings directly in YAML files under `servers.<server>.env`.

## Test Suite

### Test Questions

The evaluation includes **25 test cases** defined in YAML configuration files (`project/literature_mcp_eval_config*.yaml`). Each test case specifies:

- **Question** (`input`): What to ask the agent (e.g., "What is the title of PMID:28027860?")
- **Expected answer** (`expected_output`): The correct answer for semantic comparison
- **Test category** (`group`): Type of retrieval task
- **Success threshold** (`threshold`): Minimum similarity score (0.9 = 90%)

**Example test case:**
```yaml
- name: PMID_28027860_Title
  group: "Metadata"
  input: "What is the title of PMID:28027860?"
  expected_output: "From nocturnal frontal lobe epilepsy to Sleep-Related Hypermotor Epilepsy: A 35-year diagnostic challenge"
  threshold: 0.9
```

### Test Categories

The 25 test cases cover **6 case groups**:

1. **Metadata** (8 tests) - Title, DOI, publisher retrieval
2. **Text extraction** (9 tests) - Section content, sentences, headers
3. **Table / Figure / Figure Legend extraction** (4 tests) - Structured data
4. **Supplementary material** (2 tests) - Supplemental file detection and retrieval
5. **Publication status** (1 test) - Retraction detection
6. **Summarization** (2 tests) - Content synthesis and analysis

### Evaluation Scale

- **4 MCP servers** × **25 test cases** = **100 evaluations per agent/model**
- Each test is scored using semantic similarity (CorrectnessMetric via DeepEval)
- Pass/fail determined by threshold (typically 0.9 for 90% semantic match)

## Analysis and Visualization

All analysis is performed in Jupyter notebooks located in `notebook/`:

### Experiment 1: Cross-Agent Analysis
**Notebook:** `experiment_1_cross_agent_analysis.ipynb`

Generates:
- Overall pass rate comparison across agents (Claude Code, Goose, Gemini)
- MCP-specific performance by agent
- Case group sensitivity heatmaps
- Score distribution violin plots
- Statistical tests (chi-square, Mann-Whitney U)
- Publication-quality figures saved to `results/figures/`

### Experiment 2: Cross-Model Analysis
**Notebook:** `experiment_2_cross_model_analysis.ipynb`

Generates:
- Overall pass rate comparison across models (gpt-4o, gpt-5, gpt-4o-mini)
- Model × MCP performance matrix
- Task type sensitivity by model
- Cross-experiment comparison (agent vs. model effects)
- Statistical significance tests
- Publication-quality figures saved to `results/figures/`

### Key Metrics

- **Pass rate:** % of tests scoring ≥ threshold (0.9)
- **Semantic similarity:** Cosine similarity between actual and expected outputs
- **Case group analysis:** Performance breakdown by task type
- **Statistical tests:** Chi-square and Mann-Whitney U tests for significance

## Project Structure

```
mcp_literature_eval/
├── notebook/                                    # Jupyter notebooks (primary interface)
│   ├── experiment_1_run_evaluations.ipynb     # Run Experiment 1
│   ├── experiment_1_cross_agent_analysis.ipynb # Analyze Experiment 1
│   ├── experiment_2_run_evaluations.ipynb     # Run Experiment 2
│   ├── experiment_2_cross_model_analysis.ipynb # Analyze Experiment 2
│   └── attic/                                  # Archived notebooks
├── project/                                     # Test configurations (YAML)
│   ├── literature_mcp_eval_config.yaml         # Goose + gpt-4o (baseline)
│   ├── literature_mcp_eval_config_claude.yaml  # Claude Code agent
│   ├── literature_mcp_eval_config_gemini.yaml  # Gemini CLI agent
│   ├── literature_mcp_eval_config_goose_gpt5.yaml        # Goose + gpt-5
│   ├── literature_mcp_eval_config_goose_gpt4o_mini.yaml  # Goose + gpt-4o-mini
│   └── literature_mcp_eval_config_test.yaml    # Quick test subset
├── results/
│   ├── compare_agents/                         # Experiment 1 results
│   ├── compare_models/                         # Experiment 2 results
│   └── figures/                                # Generated plots (PNG)
├── notes/                                       # Experiment documentation
│   ├── EXPERIMENT_1_RESULTS.md
│   └── EXPERIMENT_2_CROSS_MODEL.md
├── src/                                         # Source code
└── tests/                                       # Unit tests
```

## Experiments

### Experiment 1: Cross-Agent Comparison

**Question:** Does the choice of coding agent affect MCP retrieval performance?

Compares three coding agents using their default models:
- **Claude Code** (claude-sonnet-4) - Anthropic's official CLI
- **Goose** (gpt-4o) - Block's open-source coding agent
- **Gemini CLI** (gemini-1.5-pro-002) - Google's coding agent

**Key Finding:** Agent choice has a **32 percentage point spread** in pass rates (47% → 15%).

**Documentation:** `notes/EXPERIMENT_1_RESULTS.md`

### Experiment 2: Cross-Model Comparison

**Question:** Does the choice of LLM model affect MCP retrieval performance when using the same agent?

Compares three OpenAI models using Goose agent:
- **gpt-4o** - Baseline (from Experiment 1)
- **gpt-5** - Latest flagship model
- **gpt-4o-mini** - Smaller, faster model

**Objective:** Isolate model effects from agent architecture effects.

**Documentation:** `notes/EXPERIMENT_2_CROSS_MODEL.md`

## Troubleshooting

### Known Issues

1. **NBK1256 test often hangs** - May require individual execution
2. **PMC117972 hangs with pubmed-mcp** - Known agent stability issue
3. **Full evaluation takes 2-4 hours** - Individual test cases take 2-5 minutes

### Getting Help

- **Start here:** Open the Jupyter notebooks in `notebook/` - they contain step-by-step instructions
- **Test questions:** See `project/literature_mcp_eval_config*.yaml` for all test cases
- **Experiment details:** Check `notes/EXPERIMENT_1_RESULTS.md` and `notes/EXPERIMENT_2_CROSS_MODEL.md`
- **Metacoder framework:** [metacoder documentation](https://github.com/ai4curation/metacoder)
- **Evaluation metrics:** [DeepEval documentation](https://docs.deepeval.com/)

## Contributing

This is a research evaluation project. For questions or collaboration:
- Open an issue on GitHub
- Contact the authors (see `pyproject.toml`)

## License

BSD-3-Clause (see LICENSE)

## Authors

- Justin Reese (justinreese@lbl.gov)
- Charles Parker (ctparker@lbl.gov)
- Mark Miller (mam@lbl.gov)
- Chris Mungall (CJMungall@lbl.gov)

## References

- **Metacoder:** https://github.com/ai4curation/metacoder
- **DeepEval:** https://docs.deepeval.com/
- **Model Context Protocol:** https://modelcontextprotocol.io/
