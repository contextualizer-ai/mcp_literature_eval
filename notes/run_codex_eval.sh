#!/bin/bash
# Run codex evaluation with MCP support

# Clean up any stale locks
find eval_workdir -name ".lock" -type f -delete

# Remove previous results
rm -f results/compare_agents/codex_20251205.yaml

# Run the evaluation
OPENAI_API_KEY=$(cat ~/openai.key) \
PUBMED_EMAIL=justinreese@lbl.gov \
PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808 \
uv run metacoder eval project/literature_mcp_eval_config_codex.yaml \
-o results/compare_agents/codex_20251205.yaml
