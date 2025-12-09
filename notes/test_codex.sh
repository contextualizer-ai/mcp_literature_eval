#!/bin/bash
# Test script to debug codex 401 Unauthorized error
# The issue: setting HOME=. prevents codex from reading OpenAI API credentials

cd /Users/jtr4v/PythonProject/mcp_literature_eval/eval_workdir/gpt-4o_codex_PMID_28027860_Full_Text_artl

echo "=== Test 1: Without HOME override (should work) ==="
OPENAI_API_KEY=$(cat ~/openai.key) codex exec --json --dangerously-bypass-approvals-and-sandbox "What is 2+2?" 2>&1

echo ""
echo "=== Test 2: With HOME=. (current code, likely fails with 401) ==="
HOME=. OPENAI_API_KEY=$(cat ~/openai.key) codex exec --json --dangerously-bypass-approvals-and-sandbox "What is 2+2?" 2>&1
