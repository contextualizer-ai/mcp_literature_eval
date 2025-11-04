# Gemini CLI --yolo Flag Fix

## Issue

When running Gemini CLI evaluations through metacoder, the process was hanging indefinitely after sending the prompt. Investigation revealed:

1. Gemini CLI was invoked with `-p` (non-interactive prompt mode)
2. The session log showed only the user message, no response
3. Process remained stuck for 17+ minutes with no progress

## Root Cause

Gemini CLI's non-interactive mode (`-p/--prompt`) **still requires user approval for tool calls** by default. When the MCP tools (like ARTL) needed to be invoked, Gemini was waiting for user confirmation, causing the process to hang indefinitely.

From `gemini --help`:
```
--yolo      Automatically accept all actions (aka YOLO mode)?  [boolean] [default: false]
--approval-mode  Set the approval mode: default (prompt for approval), auto_edit (auto-approve edit tools), yolo (auto-approve all tools)  [string] [choices: "default", "auto_edit", "yolo"]
```

## Solution

Modified metacoder's `GeminiCoder` class with two fixes:

### Fix 1: Add --yolo flag for non-interactive mode

**File**: `.venv/lib/python3.10/site-packages/metacoder/coders/gemini.py`

**Line 154-156** (changed):
```python
# Build the command using non-interactive mode (-p flag)
# Add --yolo flag to auto-approve all tool actions in non-interactive mode
command = ["gemini", "-p", text, "--yolo"]
```

Previously:
```python
# Build the command using non-interactive mode (-p flag)
command = ["gemini", "-p", text]
```

### Fix 2: Copy OAuth credentials to avoid re-authentication

Each test workdir gets a fresh `.gemini/` directory, causing Gemini CLI to re-authenticate (opening browser) for every test.

**File**: `.venv/lib/python3.10/site-packages/metacoder/coders/gemini.py`

**Line 116-133** (added after line 114):
```python
# Copy OAuth credentials from global config to avoid re-authentication
# This copies google_accounts.json and oauth_creds.json
global_gemini_dir = Path.home() / ".gemini"
for auth_file in ["google_accounts.json", "oauth_creds.json"]:
    auth_path = global_gemini_dir / auth_file
    if auth_path.exists():
        try:
            with open(auth_path) as f:
                auth_content = json.load(f)
            config_objects.append(
                CoderConfigObject(
                    file_type=FileType.JSON,
                    relative_path=f".gemini/{auth_file}",
                    content=auth_content,
                )
            )
        except Exception as e:
            logger.warning(f"Could not load {auth_file}: {e}")
```

## Testing

Verified the fix with a single test case:

```bash
# Before fix: Hung indefinitely (>17 minutes)
# After fix: Completed in ~19-21 seconds ✓

$ timeout 120 uv run metacoder eval /tmp/gemini_test_one_case.yaml -o /tmp/gemini_test_result.yaml
💎 Running command: gemini with prompt
💎 Command took 19.11 seconds
✓ Evaluation completed 🎉!
```

## Impact

- **Before**: Gemini evaluations impossible due to infinite hang
- **After**: Gemini evaluations complete successfully in reasonable time (~20-30 seconds per test)
- **Note**: This is a temporary patch to the installed metacoder package. The fix should be contributed upstream to the metacoder project.

## Related Issues

- Gemini evaluations also require `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` environment variables for the evaluation metrics (CorrectnessMetric uses these models for scoring)
- Updated `run_gemini_eval.sh` to export these keys

## Upstream Fix Needed

This fix should be submitted as a pull request to the metacoder repository:
- Repository: https://github.com/ai4curation/metacoder
- Suggested change: Add `--yolo` flag to the gemini command in `metacoder/coders/gemini.py`
- Alternative: Make approval mode configurable via the coder config YAML
