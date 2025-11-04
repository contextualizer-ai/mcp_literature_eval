#!/bin/bash
cd /Users/jtr4v/PythonProject/mcp_literature_eval
export OPENAI_API_KEY=$(cat ~/openai.key)
export ANTHROPIC_API_KEY=$(cat ~/anthropic.key)
rm -f results/compare_agents/goose_20251103.yaml
uv run metacoder eval project/literature_mcp_eval_config.yaml -o results/compare_agents/goose_20251103.yaml
