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

### Quick Start

```bash
# Run a small test suite
uv run metacoder eval project/literature_mcp_eval_config_test.yaml
```

### Full Evaluation

```bash
# Run with goose agent (baseline)
uv run metacoder eval project/literature_mcp_eval_config.yaml \
  -o results/mcp_literature_eval_results_goose_$(date +%Y%m%d).yaml

# Run with claude-code agent (Experiment 1)
uv run metacoder eval project/literature_mcp_eval_config_claude.yaml \
  -o results/mcp_literature_eval_results_claude_$(date +%Y%m%d).yaml
```

### Environment Variables

Some MCPs require API keys or contact information:

```bash
export PUBMED_EMAIL="your.email@example.com"
export PUBMED_API_KEY="your_api_key_here"
```

Or configure directly in YAML files under `servers.<server>.env`.

## Test Suite

The evaluation includes **25 test cases** across **6 case groups**:

1. **Metadata** (4 tests) - Title, DOI, publisher retrieval
2. **Text extraction** (11 tests) - Section content, sentences, headers
3. **Table / Figure / Figure Legend extraction** (4 tests) - Structured data
4. **Supplementary material** (3 tests) - Supplemental file detection and retrieval
5. **Publication status** (1 test) - Retraction detection
6. **Summarization** (2 tests) - Content synthesis and analysis

Each MCP is tested against all 25 test cases, resulting in **100 evaluations per agent**.

## Analysis

Analyze results using the provided Jupyter notebooks:

```bash
# For cross-agent comparison (Experiment 1)
jupyter notebook notebook/experiment_1_cross_agent_analysis.ipynb

# For baseline visualization
jupyter notebook notebook/attic/visualize_results_yaml_executed.ipynb
```

The analysis notebooks generate:
- Pass rate comparisons by MCP and agent
- Case group sensitivity heatmaps
- Score distribution plots
- Error rate analysis
- Statistical significance tests

## Project Structure

```
mcp_literature_eval/
├── notes/                   # Experiment plans and documentation
│   ├── experiment_1_cross_agent_comparison.md
│   └── experiment_2_cross_model_evaluation.md
├── notebook/                # Jupyter notebooks for analysis
│   ├── experiment_1_cross_agent_analysis.ipynb
│   └── attic/              # Previous notebooks
├── project/                 # Evaluation configurations
│   ├── literature_mcp_eval_config.yaml        # Baseline (goose)
│   ├── literature_mcp_eval_config_claude.yaml # Experiment 1 (claude-code)
│   └── literature_mcp_eval_config_test.yaml   # Quick tests
├── results/                 # Evaluation results (YAML files)
│   └── figures/            # Generated plots
├── src/                     # Source code
└── tests/                   # Unit tests
```

## Experiments

### Experiment 1: Cross-Agent Comparison

Compares MCP performance across different coding agents (goose-cli, claude-code) to determine whether agent choice affects retrieval reliability.

**See:** `notes/experiment_1_cross_agent_comparison.md`

### Experiment 2: Cross-Model Evaluation

Re-evaluates existing outputs using different LLM judges to assess potential model-specific bias in evaluation.

**See:** `notes/experiment_2_cross_model_evaluation.md`

## Troubleshooting

### Known Issues

1. **NBK1256 test often hangs** - May require individual execution
2. **PMC117972 hangs with pubmed-mcp** - Known agent stability issue
3. **Full evaluation takes 2-4 hours** - Individual test cases take 2-5 minutes

### Getting Help

- Check the detailed READMEs in `project/` and `notes/` directories
- Review experiment plans for specific procedures
- See [metacoder documentation](https://github.com/ai4curation/metacoder)
- See [DeepEval documentation](https://docs.deepeval.com/)

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
