#!/bin/bash
# Run codex evaluation with GPT-5 and MCP support

# Clean up any stale locks
find eval_workdir -name ".lock" -type f -delete 2>/dev/null || true

# Create results directory if it doesn't exist
mkdir -p results/compare_agents

# Set output file with timestamp
OUTPUT_FILE="results/compare_agents/codex_gpt5_$(date +%Y%m%d).yaml"

# Run the evaluation
OPENAI_API_KEY=$(cat ~/openai.key) \
PUBMED_EMAIL=justinreese@lbl.gov \
PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808 \
uv run metacoder eval project/generated/literature_mcp_eval_config_codex.yaml \
-o "$OUTPUT_FILE"

echo "Codex GPT-5 evaluation complete. Results saved to: $OUTPUT_FILE"
