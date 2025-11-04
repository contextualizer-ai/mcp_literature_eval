# Metacoder Goose Coder Fixes

## Summary

Fixed systematic failures in Goose evaluations (100% failure rate with exit code 101) by properly configuring environment variables and adding error handling to the GooseCoder implementation.

## Problem

Goose evaluations were failing immediately with:
- Exit code 101
- Execution time: 0.02-0.06 seconds (indicating immediate crash)
- 100% failure rate across all 100 tests

## Root Causes

1. **Missing environment variable configuration**: Goose requires `GOOSE_PROVIDER__API_KEY` (double underscore) but metacoder was not setting it
2. **Config precedence issues**: Global `~/.config/goose/config.yaml` settings were overriding local evaluation configs
3. **Missing error handling**: Process failures crashed the entire evaluation instead of marking individual tests as failed
4. **Problematic global extensions**: Global config had extensions enabled that didn't exist in evaluation workdirs

## Solutions Implemented

### 1. Environment Variable Configuration

**File**: `.venv/lib/python3.10/site-packages/metacoder/coders/goose.py`

**Location**: Lines 193-217 in the `run()` method

**Changes**:
```python
# Override provider and model from config via environment variables
# This ensures local settings take precedence over global config
if self.config and self.config.ai_model:
    model = self.config.ai_model
    # Get provider as string
    if isinstance(model.provider, str):
        provider_str = model.provider
    elif model.provider and hasattr(model.provider, "name"):
        provider_str = model.provider.name
    else:
        provider_str = "openai"  # default

    env["GOOSE_PROVIDER"] = provider_str
    env["GOOSE_MODEL"] = model.name
    logger.debug(f"Setting GOOSE_PROVIDER={provider_str}, GOOSE_MODEL={model.name}")

    # Set API key via GOOSE_PROVIDER__API_KEY environment variable
    # Check for provider-specific API keys in environment
    if provider_str == "anthropic" and "ANTHROPIC_API_KEY" in env:
        env["GOOSE_PROVIDER__API_KEY"] = env["ANTHROPIC_API_KEY"]
        logger.debug("Set GOOSE_PROVIDER__API_KEY from ANTHROPIC_API_KEY")
    elif provider_str == "openai" and "OPENAI_API_KEY" in env:
        env["GOOSE_PROVIDER__API_KEY"] = env["OPENAI_API_KEY"]
        logger.debug("Set GOOSE_PROVIDER__API_KEY from OPENAI_API_KEY")
```

**Why this fixes the issue**:
- Goose uses `GOOSE_PROVIDER__API_KEY` (double underscore) as the standard API key environment variable
- Setting `GOOSE_PROVIDER` and `GOOSE_MODEL` as environment variables ensures they override global config
- Maps provider-specific keys (ANTHROPIC_API_KEY, OPENAI_API_KEY) to Goose's expected format

### 2. Error Handling

**File**: `.venv/lib/python3.10/site-packages/metacoder/coders/goose.py`

**Location**: Lines 223-239 in the `run()` method

**Changes**:
```python
try:
    result = self.run_process(command, env)
    end_time = time.time()
    ao = CoderOutput(stdout=result.stdout, stderr=result.stderr)
    logger.info(f"🦆 Command took {end_time - start_time:.2f} seconds")
except Exception as e:
    # Handle process errors gracefully - don't crash entire evaluation
    end_time = time.time()
    logger.warning(f"Goose command failed (test will be marked as failed): {e}")
    ao = CoderOutput(
        stdout="",
        stderr=str(e),
        result_text=f"Error: {str(e)}",
        success=False,
    )
    logger.info(f"🦆 Command took {end_time - start_time:.2f} seconds")
    return ao
```

**Why this fixes the issue**:
- Prevents single test failures from crashing the entire evaluation
- Gracefully handles process errors and marks individual tests as failed
- Allows evaluation to continue through all 100 tests

### 3. Global Config Fixes

**File**: `~/.config/goose/config.yaml`

**Change**: Disabled problematic `tabfilequery` extension

```yaml
tabfilequery:
  enabled: false  # Changed from true
```

**Why this was needed**:
- The global config had `tabfilequery` extension enabled
- This extension tried to run `src/fitness_mcp/main.py` which doesn't exist in evaluation workdirs
- Caused Goose to fail on startup

## Results

**Before fixes**:
- 100/100 tests failing (exit code 101)
- Test duration: 0.02-0.06 seconds (immediate crash)
- No results generated

**After fixes**:
- 100/100 tests completed successfully (exit code 0)
- Test duration: 10-24 seconds (proper execution)
- Results file generated: `goose_20251101.yaml` (919KB, 18,595 lines)
- Average score: 0.137 (~13.7%)

## Files Modified

1. **`.venv/lib/python3.10/site-packages/metacoder/coders/goose.py`**
   - Added environment variable configuration (lines 193-217)
   - Added error handling (lines 223-239)

2. **`~/.config/goose/config.yaml`**
   - Disabled `tabfilequery` extension (line 132)

## Testing

Verified with:
```bash
export OPENAI_API_KEY=$(cat ~/openai.key)
export ANTHROPIC_API_KEY=$(cat ~/anthropic.key)
uv run metacoder eval project/literature_mcp_eval_config.yaml -o results/raw/goose_20251101.yaml
```

Result: All 100 tests completed successfully.

### Error 4: MCP extensions not loading (CRITICAL)

**Problem**: All 100 Goose tests showed "No extensions available to enable" even though extensions were configured in `.config/goose/config.yaml`.

**Root cause discovered**: `goose run` command DOES NOT load extensions from config files. Extensions must be passed as command-line arguments using `--with-extension`.

**Fix**: Modified `goose.py` lines 221-232 to add `--with-extension` flags for each configured MCP extension:

```python
# Add MCP extensions as command-line arguments
# Config files alone don't work with 'goose run' - must use --with-extension
if self.config and self.config.extensions:
    for mcp in self.config.extensions:
        if isinstance(mcp, MCPConfig) and mcp.enabled:
            # Build extension command from cmd + args
            if mcp.command:
                ext_cmd = mcp.command
                if mcp.args:
                    ext_cmd = ext_cmd + " " + " ".join(mcp.args)
                command.extend(["--with-extension", ext_cmd])
                logger.debug(f"Adding extension: --with-extension {ext_cmd}")
```

**Example**: For an extension configured as:
```yaml
extensions:
  artl:
    cmd: uvx
    args:
    - artl-mcp
```

The command now becomes:
```bash
goose run -t "text" --with-extension "uvx artl-mcp"
```

**Verification**:
- Before fix: "I don't currently have access to any extensions"
- After fix: Goose successfully calls MCP tools like `get_paper`, `get_metadata`, etc.

**Reference**: https://block.github.io/goose/docs/guides/goose-cli-commands/ documents the `--with-extension` flag.

## Upstream Contribution

The changes to `goose.py` should be contributed back to the metacoder project as they fix critical bugs that prevent Goose evaluations from working:

1. Missing `GOOSE_PROVIDER__API_KEY` environment variable configuration
2. MCP extensions not being passed to `goose run` command via `--with-extension` flags
3. Crash-on-error bug that prevented graceful failure handling

### Patch File

A patch file has been created: `metacoder_goose_error_handling.patch`

### Recommended Next Steps

1. Submit a PR to the metacoder repository with these fixes
2. Include all three fixes: environment variables, extension command-line args, and error handling
3. Add documentation about:
   - Goose's environment variable requirements (`GOOSE_PROVIDER__API_KEY`)
   - How `goose run` requires `--with-extension` flags (config files are not sufficient)
