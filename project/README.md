# Evaluation Configuration Files

This directory contains YAML configuration files for metacoder evaluations.

## Configuration Files

- **`literature_mcp_eval_config.yaml`** - Full evaluation with goose agent (baseline)
- **`literature_mcp_eval_config_claude.yaml`** - Full evaluation with claude-code agent (Experiment 1)
- **`literature_mcp_eval_config_test.yaml`** - Small test suite for development
- **`literature_mcp_eval_config_NBK.yaml`** - NBK-specific tests
- **`literature_mcp_encoding_test.yaml`** - Encoding tests

## Quick Start

```bash
# Test configuration (quick)
uv run metacoder eval project/literature_mcp_eval_config_test.yaml

# Full evaluation with goose
uv run metacoder eval project/literature_mcp_eval_config.yaml

# Full evaluation with claude-code
uv run metacoder eval project/literature_mcp_eval_config_claude.yaml
```

## Configuration Structure

Each YAML file contains:
- **`coders`** - Which AI coding agent to use (goose, claude, codex)
- **`models`** - LLM models for evaluation
- **`servers`** - MCP server configurations
- **`server_combinations`** - Which servers to test
- **`cases`** - Test cases with input/expected output

See the main README for detailed usage instructions.
