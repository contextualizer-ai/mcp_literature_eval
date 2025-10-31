# CLAUDE.md for mcp_literature_eval

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Eval of MCPs that retrieve stuff to do with scientific literature

The project uses `uv` for dependency management and `just` as the command runner.

## IMPORTANT INSTRUCTIONS

- we use test driven development, write tests first before implementing a feature
- do not try and 'cheat' by making mock tests (unless asked)
- if functionality does not work, keep trying, do not relax the test just to get poor code in
- always run tests
- use docstrings

We make heavy use of doctests, these serve as both docs and tests. `just test` will include these,
or do `just doctest` just to write doctests

In general AVOID try/except blocks, except when these are truly called for, for example
when interfacing with external systems. For wrapping deterministic code,  these are ALMOST
NEVER required, if you think you need them, it's likely a bad smell that your logic is wrong.

## Essential Commands


### Testing and Quality
- `just test` - Run all tests, type checking, and formatting checks
- `just pytest` - Run Python tests only
- `just mypy` - Run type checking
- `just format` - Run ruff linting/formatting checks
- `uv run pytest tests/test_simple.py::test_simple` - Run a specific test

### Running the CLI
- `uv run mcp_literature_eval --help` - Run the CLI tool with options

### Documentation
- `just _serve` - Run local documentation server with mkdocs

## Project Architecture

### Core Structure
- **src/my_awesome_tool/** - Main package containing the CLI and application logic
  - `cli.py` - Typer-based CLI interface, entry point for the application
- **tests/** - Test suite using pytest with parametrized tests
- **docs/** - MkDocs-managed documentation with Material theme

### Technology Stack
- **Python 3.10+** with `uv` for dependency management
- **LinkML** for data modeling (linkml-runtime)
- **Typer** for CLI interface
- **pytest** for testing
- **mypy** for type checking
- **ruff** for linting and formatting
- **MkDocs Material** for documentation

### Key Configuration Files
- `pyproject.toml` - Python project configuration, dependencies, and tool settings
- `justfile` - Command runner recipes for common development tasks
- `mkdocs.yml` - Documentation configuration
- `uv.lock` - Locked dependency versions

## Development Workflow

1. Dependencies are managed via `uv` - use `uv add` for new dependencies
2. All commands are run through `just` or `uv run`
3. The project uses dynamic versioning from git tags
4. Documentation is auto-deployed to GitHub Pages at https://monarch-initiative.github.io/my-awesome-tool

---

## EVALUATION MODE: Answering Literature Retrieval Questions

**When you receive questions about scientific papers** (e.g., "What is the title of PMID:12345?"), you are in **evaluation mode**. This is testing MCP server performance.

### Guidelines for Evaluation Mode:

1. **Use the MCP tools** available to retrieve the requested paper
   - Try `mcp__artl__get_pmid_text` or similar MCP tools
   - Don't assume content is inaccessible - try the MCPs first

2. **Answer from what the MCP retrieved**
   - If the MCP successfully returns content, extract the requested information
   - Don't say "I cannot access" if the MCP gave you the content
   - Don't add unnecessary commentary about paper relevance or domain

3. **Be direct and precise**
   - Extract exactly what was asked for (title, sentence, table row, etc.)
   - Match the expected format when possible
   - Provide just the answer, not explanations about why you can/can't answer

4. **Do NOT restrict by topic**
   - Answer questions about ANY paper, regardless of subject area
   - Don't reject papers because they're "not about X domain"
   - The evaluation covers diverse scientific literature

### Example - Good Response:
**Q**: "What is the first sentence of section 2 in PMID:28027860?"
**A**: "Even though many of NFLE's core features have been clarified in the last two decades, some critical issues remain controversial."

### Example - Bad Response:
**Q**: "What is the first sentence of section 2 in PMID:28027860?"
**A**: "I cannot access section 2 of this paper because it's behind a paywall and not available in open access..."
*(Bad because: If the MCP retrieved it, you DO have access - answer from what was retrieved!)*
