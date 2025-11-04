# Notes Directory - Index

This directory contains documentation, status updates, and working notes for the MCP Literature Evaluation project.

**Last Updated:** 2025-11-03

---

## Quick Links

### 📋 Current Status
- **[PROJECT_STATUS_20251103.md](PROJECT_STATUS_20251103.md)** - Comprehensive project status (READ THIS FIRST)

### 📓 Notebooks
- **[NOTEBOOKS_README.md](NOTEBOOKS_README.md)** - Guide to all analysis notebooks

### 🧪 Experiments
- **[EXPERIMENT_1_STATUS.md](EXPERIMENT_1_STATUS.md)** - Cross-agent comparison experiment
- **[experiment_1_cross_agent_comparison.md](experiment_1_cross_agent_comparison.md)** - Experimental design
- **[experiment_2_cross_model_evaluation.md](experiment_2_cross_model_evaluation.md)** - Future cross-model experiment

### 🔧 Testing Scripts
- **[test_goose.sh](test_goose.sh)** - Goose evaluation test script
- **[test_goose_extension_fix.sh](test_goose_extension_fix.sh)** - Goose extension fix verification

---

## File Descriptions

### PROJECT_STATUS_20251103.md (11 KB)

**Comprehensive project status snapshot**

What it contains:
- Executive summary of all work completed
- Status of Goose evaluation (COMPLETE) and Claude evaluation (READY)
- Complete list of all 4 bugs fixed in metacoder
- Documentation of all files modified
- Results summary and metrics
- Next steps (immediate, short-term, medium-term)
- Known issues and lessons learned

When to read:
- Getting up to speed on project
- Understanding what's been done and what's next
- Before running new evaluations
- When writing methods/results sections

---

### NOTEBOOKS_README.md (8.3 KB)

**Complete guide to Jupyter notebooks**

What it contains:
- Descriptions of both notebooks (fixes documentation + cross-agent analysis)
- How to run each notebook
- Expected outputs and figures
- Troubleshooting guide
- How to add results for new agents
- Integration with manuscript

When to read:
- Before running analysis notebooks
- When adding new evaluation results
- Troubleshooting notebook errors
- Generating figures for manuscript

---

### EXPERIMENT_1_STATUS.md (11 KB)

**Detailed status of cross-agent comparison experiment**

What it contains:
- Experiment setup and configuration
- Test results from Claude-code runs
- Root cause analysis of failures
- Three types of fixes applied:
  1. Metacoder crash bug fix
  2. CLAUDE.md evaluation instructions
  3. Goose hints file for fair comparison
- Discovery of CLAUDE.md interference
- Findings valuable for manuscript

When to read:
- Understanding Claude evaluation issues
- Learning about agent configuration effects
- Understanding compound failure modes
- Writing about evaluation challenges

Historical context: This was written during initial Claude evaluation attempts before discovering the Goose extension loading bug.

---

### experiment_1_cross_agent_comparison.md (8.4 KB)

**Original experimental design document**

What it contains:
- Research question: Does agent choice affect MCP retrieval performance?
- Experimental methodology
- Test case design
- Agents to compare (goose, claude-code, gemini)
- Metrics and analysis plan
- Expected timeline

When to read:
- Understanding experimental design
- Planning analysis approach
- Writing methods section
- Designing similar experiments

Status: Design complete, Goose evaluation complete, Claude ready to run

---

### experiment_2_cross_model_evaluation.md (15 KB)

**Future experiment: Cross-model comparison**

What it contains:
- Research question: Does LLM model choice affect MCP performance?
- Models to test (GPT-4, Claude Opus, Claude Sonnet, Gemini)
- Why this matters (cost vs performance tradeoffs)
- Experimental design
- Statistical power analysis
- Budget estimates

When to read:
- Planning future experiments
- Understanding model vs agent distinction
- Estimating costs and timeline

Status: Design complete, not yet executed (waiting for Experiment 1 completion)

---

### test_goose.sh (298 B)

**Shell script to test Goose evaluation**

What it does:
```bash
#!/bin/bash
cd /Users/jtr4v/PythonProject/mcp_literature_eval
export OPENAI_API_KEY=$(cat ~/openai.key)
export ANTHROPIC_API_KEY=$(cat ~/anthropic.key)
uv run metacoder eval project/literature_mcp_eval_config.yaml \
  -o results/raw/goose_20251101.yaml
```

When to use:
- Quick testing of Goose evaluation
- Debugging Goose issues
- Running small test batches

Status: Historical - replaced by `run_goose_eval_fixed.sh` in project root

---

### test_goose_extension_fix.sh (253 B)

**Verification script for Goose extension fix**

What it does:
- Tests that `--with-extension` flags are being added correctly
- Runs small subset of tests
- Verifies MCP tools are accessible

When to use:
- Verifying extension fix is working
- Debugging extension loading issues
- Quick smoke test

Status: Used during debugging, kept for reference

---

## Directory Structure Context

```
mcp_literature_eval/
├── notes/                          # ← YOU ARE HERE
│   ├── README.md                   # This file
│   ├── PROJECT_STATUS_20251103.md  # Current status snapshot
│   ├── NOTEBOOKS_README.md         # Notebook guide
│   ├── EXPERIMENT_1_STATUS.md      # Claude eval debugging
│   ├── experiment_1_*.md           # Experiment designs
│   └── test_*.sh                   # Test scripts
├── notebook/                       # Jupyter notebooks
│   ├── metacoder_fixes_documentation.ipynb
│   └── experiment_1_cross_agent_analysis.ipynb
├── results/
│   ├── compare_agents/             # Active results
│   │   └── goose_20251103.yaml
│   ├── attic/                      # Archived results
│   └── figures/                    # Generated plots
├── METACODER_FIXES.md              # Goose fixes documentation
├── metacoder_*.patch               # Patch files for upstream
└── run_goose_eval_fixed.sh         # Main evaluation script
```

---

## Reading Order for New Team Members

### Day 1: Getting Oriented
1. **PROJECT_STATUS_20251103.md** - Understand where we are
2. **experiment_1_cross_agent_comparison.md** - Understand what we're testing
3. **METACODER_FIXES.md** (in project root) - Understand bugs we fixed

### Day 2: Understanding the Details
4. **EXPERIMENT_1_STATUS.md** - See what issues we encountered
5. **NOTEBOOKS_README.md** - Learn how to run analyses
6. **experiment_2_cross_model_evaluation.md** - See future plans

### Day 3: Hands-On
7. Run the notebooks (follow NOTEBOOKS_README.md)
8. Review results files in `results/compare_agents/`
9. Check patch files to understand exact code changes

---

## Document Ownership & Updates

### Who Updates What

**PROJECT_STATUS_YYYYMMDD.md**
- Create new dated version for major milestones
- Update when: Completing evaluations, fixing major bugs, reaching project phases
- Archive old versions (keep for history)

**NOTEBOOKS_README.md**
- Update when: Adding new notebooks, changing notebook structure
- Owner: Whoever maintains analysis code

**EXPERIMENT_N_STATUS.md**
- Update as experiment progresses
- Final update when experiment complete
- Then create new experiment file for next phase

**experiment_N_*.md**
- Design documents - mostly static after initial creation
- Update only if experimental design changes significantly

---

## Quick Commands

### Find something in notes
```bash
grep -r "keyword" notes/
```

### List all notes by date modified
```bash
ls -lt notes/
```

### Count lines in all markdown files
```bash
wc -l notes/*.md
```

### Search for TODO items
```bash
grep -n "TODO\|FIXME\|XXX" notes/*.md
```

---

## Related Documentation

### In Project Root
- **METACODER_FIXES.md** - Detailed Goose fixes documentation
- **README.md** - Project README
- **CLAUDE.md** - Instructions for Claude Code assistant

### In Project Directory
- **project/README.md** - Configuration file documentation
- **project/GEMINI.md** - Gemini-specific instructions

### Notebooks
- **notebook/metacoder_fixes_documentation.ipynb** - Interactive fix documentation
- **notebook/experiment_1_cross_agent_analysis.ipynb** - Analysis notebook

### Results
- **results/compare_agents/** - Active evaluation results
- **results/attic/** - Historical results
- **results/figures/** - Generated plots

---

## Version History

### 2025-11-03
- Created PROJECT_STATUS_20251103.md - comprehensive status
- Created NOTEBOOKS_README.md - notebook guide
- Created this README.md - notes index

### 2025-10-31
- Created EXPERIMENT_1_STATUS.md - Claude debugging
- Updated experiment files with findings

### 2025-10-30
- Created experiment_1_cross_agent_comparison.md
- Created experiment_2_cross_model_evaluation.md

---

## Contact

**Questions about:**
- Goose fixes → See `METACODER_FIXES.md` and `PROJECT_STATUS_20251103.md`
- Claude fixes → See `EXPERIMENT_1_STATUS.md` and patch files
- Running analyses → See `NOTEBOOKS_README.md`
- Experimental design → See `experiment_*.md` files

**Not documented yet?**
- Check project root `README.md`
- Check git history: `git log --all -- notes/`
- Ask team members

---

**Maintained by:** Project team
**Last comprehensive review:** 2025-11-03
**Next review:** After Claude evaluation completes
