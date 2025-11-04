#!/bin/bash
cd /Users/jtr4v/PythonProject/mcp_literature_eval
export OPENAI_API_KEY=$(cat ~/openai.key)
export ANTHROPIC_API_KEY=$(cat ~/anthropic.key)
uv run metacoder eval project/literature_mcp_eval_config_test.yaml -o /tmp/goose_extension_test.yaml
