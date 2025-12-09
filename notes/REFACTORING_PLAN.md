# Config File Refactoring Plan: Shared Test Cases

## Problem
- 6 config files with duplicated test case definitions (~250 lines each)
- Updating test cases (e.g., adding custom GEval criteria) requires editing all 6 files identically
- High risk of inconsistency across agent/model comparisons

## Solution
**Preprocessing approach**: Separate test cases from agent metadata, merge with script

## New Directory Structure

```
project/
├── test_cases.yaml                              # ← Single source of truth for test cases
├── templates/                                    # ← Agent-specific metadata only
│   ├── claude_template.yaml
│   ├── gemini_template.yaml
│   ├── goose_claude_template.yaml
│   ├── goose_gpt4o_template.yaml
│   ├── goose_gpt4o_mini_template.yaml
│   └── goose_gpt5_template.yaml
├── generated/                                    # ← Auto-generated - DO NOT EDIT
│   ├── literature_mcp_eval_config_claude.yaml
│   ├── literature_mcp_eval_config_gemini.yaml
│   ├── literature_mcp_eval_config_goose_claude.yaml
│   ├── literature_mcp_eval_config_goose_gpt4o.yaml
│   ├── literature_mcp_eval_config_goose_gpt4o_mini.yaml
│   └── literature_mcp_eval_config_goose_gpt5.yaml
└── scripts/
    ├── generate_configs.py                       # ← Merges templates + test_cases
    └── validate_configs.py                       # ← Verifies test case consistency
```

## Implementation Steps

### 1. Extract Test Cases
- [x] Extract `cases:` section from existing config files
- [x] Create `project/test_cases.yaml` with shared test definitions
- [x] Verify all 6 files have identical test cases

### 2. Create Templates
- [x] Create `project/templates/` directory
- [x] Extract metadata sections (name, coders, models, servers) from each config
- [x] Create one template file per agent/model combination

### 3. Write Generation Script
- [x] Create `project/scripts/generate_configs.py`
- [x] Load test_cases.yaml
- [x] For each template file:
  - Load template
  - Merge with test_cases
  - Write to `project/generated/`
- [x] Add validation to ensure identical test cases across all generated files

### 4. Update Notebooks
**Files that need path updates:**

| Notebook | Line(s) | Old Path | New Path |
|----------|---------|----------|----------|
| `notebook/experiment_1_run_evaluations.ipynb` | 68 | `project/literature_mcp_eval_config_goose_gpt4o.yaml` | `project/generated/literature_mcp_eval_config_goose_gpt4o.yaml` |
| `notebook/experiment_1_run_evaluations.ipynb` | 76 | `project/literature_mcp_eval_config_gemini.yaml` | `project/generated/literature_mcp_eval_config_gemini.yaml` |
| `notebook/experiment_1_run_evaluations.ipynb` | 157 | `project/literature_mcp_eval_config_claude.yaml` | `project/generated/literature_mcp_eval_config_claude.yaml` |
| `notebook/experiment_1_run_evaluations.ipynb` | 161 | `project/literature_mcp_eval_config_goose_gpt4o.yaml` | `project/generated/literature_mcp_eval_config_goose_gpt4o.yaml` |
| `notebook/experiment_1_run_evaluations.ipynb` | 165 | `project/literature_mcp_eval_config_gemini.yaml` | `project/generated/literature_mcp_eval_config_gemini.yaml` |
| `notebook/experiment_2_run_evaluations.ipynb` | 123 | `project/literature_mcp_eval_config_goose_gpt5.yaml` | `project/generated/literature_mcp_eval_config_goose_gpt5.yaml` |
| `notebook/experiment_2_run_evaluations.ipynb` | 168 | `project/literature_mcp_eval_config_goose_gpt4o_mini.yaml` | `project/generated/literature_mcp_eval_config_goose_gpt4o_mini.yaml` |
| `notebook/experiment_2_run_evaluations.ipynb` | 335 | `project/literature_mcp_eval_config_goose_gpt4o_mini.yaml` | `project/generated/literature_mcp_eval_config_goose_gpt4o_mini.yaml` |

**Action items:**
- [ ] Update all paths in notebooks from `project/literature_mcp_eval_config_*.yaml` to `project/generated/literature_mcp_eval_config_*.yaml`
- [ ] Update any bash scripts or documentation referencing the old paths
- [ ] Add note in notebooks about running `generate_configs.py` before evaluations

### 5. Workflow After Refactoring

**To update test cases:**
1. Edit `project/test_cases.yaml` (single source of truth)
2. Run `python project/scripts/generate_configs.py`
3. Verify: All 6 generated files updated consistently
4. Run evaluations as normal

**To update agent metadata:**
1. Edit specific template in `project/templates/`
2. Run `python project/scripts/generate_configs.py`
3. Only that agent's config is updated

## Benefits
- ✅ Single source of truth for test cases
- ✅ Easy to add custom GEval criteria (edit once, applies to all)
- ✅ Impossible to have inconsistent test cases across agents
- ✅ Clear separation: test logic vs. agent configuration
- ✅ Automated validation

## Risks & Mitigation
- **Risk**: Forgetting to regenerate configs after editing test_cases.yaml
  - **Mitigation**: Add pre-commit hook or makefile target
  - **Mitigation**: Validation script checks if generated files are up-to-date

- **Risk**: Accidentally editing generated files
  - **Mitigation**: Add "DO NOT EDIT" header to all generated files
  - **Mitigation**: Add `.gitattributes` to mark as generated

- **Risk**: Breaking existing notebook workflows
  - **Mitigation**: Update all notebooks in one commit
  - **Mitigation**: Test full workflow end-to-end before committing

## Next Steps After Refactoring
1. Add custom GEval criteria to test_cases.yaml
2. Categorize tests (exact text extraction, metadata retrieval, etc.)
3. Apply appropriate custom metrics to each category
4. Regenerate all configs
5. Run comprehensive evaluation with improved metrics
