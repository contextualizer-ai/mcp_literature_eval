# CBORG Configuration for Experiment 2

## Overview

Configured Goose + Claude Sonnet evaluation to use CBORG (https://api.cborg.lbl.gov) instead of direct Anthropic API, eliminating personal API credit costs.

## Configuration Changes

### 1. Model Name
**Changed from:** `claude-sonnet-4-20250514`
**Changed to:** `anthropic/claude-sonnet`

CBORG uses the format `anthropic/claude-sonnet` to access Claude 4.0 Sonnet through their proxy.

### 2. Base URL
**Changed from:** Direct Anthropic API
**Changed to:** `https://api.cborg.lbl.gov`

### 3. Authentication
**Changed from:** `ANTHROPIC_API_KEY` (personal account)
**Changed to:** `ANTHROPIC_AUTH_TOKEN` from `~/cborg_june_25.key`

Note: Both `ANTHROPIC_AUTH_TOKEN` and `ANTHROPIC_API_KEY` are set to ensure compatibility with different SDK versions.

## Updated Files

### `project/literature_mcp_eval_config_goose_claude.yaml`
```yaml
coders:
  goose:
    env:
      GOOSE_MODEL: anthropic/claude-sonnet
      GOOSE_PROVIDER: anthropic
      ANTHROPIC_BASE_URL: https://api.cborg.lbl.gov

models:
  claude-sonnet-4:
    provider: anthropic
    name: anthropic/claude-sonnet
```

### `run_goose_claude_eval.sh`
```bash
#!/bin/bash
cd /Users/jtr4v/PythonProject/mcp_literature_eval
export OPENAI_API_KEY=$(cat ~/openai.key)
# CBORG uses ANTHROPIC_AUTH_TOKEN, but also set ANTHROPIC_API_KEY for compatibility
export ANTHROPIC_AUTH_TOKEN=$(cat ~/cborg_june_25.key)
export ANTHROPIC_API_KEY=$(cat ~/cborg_june_25.key)
export ANTHROPIC_BASE_URL=https://api.cborg.lbl.gov
export PUBMED_EMAIL=justinreese@lbl.gov
export PUBMED_API_KEY=01eec0a16472164c6d69163bd28368311808
rm -f results/compare_models/goose_claude_$(date +%Y%m%d).yaml
uv run metacoder eval project/literature_mcp_eval_config_goose_claude.yaml \
  -o results/compare_models/goose_claude_$(date +%Y%m%d).yaml
```

## Available CBORG Models

According to https://cborg.lbl.gov/models/:

**Claude Models (via Vertex AI / AWS):**
- `anthropic/claude-haiku` - Claude 4.5 Haiku (200k context, $1/$5 per 1M tokens)
- `anthropic/claude-sonnet` - Claude 4.0 Sonnet (200k context, $3/$15 per 1M tokens) ← **Using this**
- `anthropic/claude-opus` - Claude 4.1 Opus (200k context, $15/$75 per 1M tokens)

All models support:
- 200k context window
- Vision capabilities
- Tool use
- Function calling

## Benefits

1. **No personal API costs** - Uses LBL CBORG infrastructure
2. **Same model quality** - Claude 4.0 Sonnet via Google Vertex AI
3. **Institutional access** - Supported and managed by LBL

## Testing

Before running the full 100-test evaluation:

```bash
# Test CBORG connection with a single test
./run_goose_claude_eval.sh
```

Watch for:
- ✓ Successful connection to https://api.cborg.lbl.gov
- ✓ Model responses from `anthropic/claude-sonnet`
- ✗ Authentication errors (check `~/cborg_june_25.key`)
- ✗ Model not found errors (verify model name)

## Expected Runtime

- **100 tests** × ~30 seconds/test = ~50 minutes
- **Cost**: $0 (using CBORG)

## Comparison with Previous Attempt

| Metric | Direct Anthropic API | CBORG |
|--------|---------------------|--------|
| Endpoint | api.anthropic.com | api.cborg.lbl.gov |
| Auth | Personal API key | LBL CBORG token |
| Model | claude-sonnet-4-20250514 | anthropic/claude-sonnet |
| Cost | ~$20-30 for 100 tests | $0 |
| Result | Failed at test 8 (credit limit) | TBD |

---

**Status**: Ready to run
**Date**: 2025-11-05
