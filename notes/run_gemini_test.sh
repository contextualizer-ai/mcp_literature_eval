#!/bin/bash
export OPENAI_API_KEY=$(cat ~/openai.key)
export PUBMED_EMAIL=justinreese@lbl.gov
export PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808
cd /Users/jtr4v/PythonProject/mcp_literature_eval
rm -f test_gemini_result.yaml
uv run metacoder eval test_gemini_single.yaml -o test_gemini_result.yaml
