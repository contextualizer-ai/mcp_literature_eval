#!/bin/bash
cd /Users/jtr4v/PythonProject/mcp_literature_eval
export OPENAI_API_KEY=$(cat ~/openai.key)
export ANTHROPIC_API_KEY=$(cat ~/anthropic.key)
export PUBMED_EMAIL=justinreese@lbl.gov
export PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808
rm -f results/compare_models/goose_claude_$(date +%Y%m%d).yaml
uv run metacoder eval project/literature_mcp_eval_config_goose_claude.yaml \
  -o results/compare_models/goose_claude_$(date +%Y%m%d).yaml
