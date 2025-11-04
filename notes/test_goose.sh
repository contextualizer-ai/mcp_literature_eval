#!/bin/bash
export GOOSE_PROVIDER__API_KEY=$(cat ~/anthropic.key)
export OPENAI_API_KEY=$(cat ~/openai.key)
export XDG_CONFIG_HOME=eval_workdir/claude-4-sonnet_goose_PMID_28027860_Title_artl
export GOOSE_DISABLE_KEYRING=1

cd /Users/jtr4v/PythonProject/mcp_literature_eval
goose run -t "test" 2>&1
