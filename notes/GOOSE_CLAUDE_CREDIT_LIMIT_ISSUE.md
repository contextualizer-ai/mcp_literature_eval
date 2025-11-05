# Goose + Claude Sonnet 4 Credit Limit Issue

## Summary

The Experiment 2 evaluation of Goose with claude-sonnet-4 was interrupted by an **Anthropic API credit limit** error on test 8 out of 100, resulting in invalid results.

## Evidence

### Credit Limit Error
Test 8 (`10_1371_journal_pone_0000217_Full_Text_A`) shows:
```
Error: Request failed with status: 400 Bad Request.
Message: Your credit balance is too low to access the Anthropic API.
Please go to Plans & Billing to upgrade or purchase credits.
```

### Performance Breakdown

| Phase | Tests | Pass Rate | Avg Score | Status |
|-------|-------|-----------|-----------|--------|
| **Before credit limit** | 1-7 | 28.6% (2/7) | 0.368 | VALID |
| **After credit limit** | 8-100 | 0.0% (0/93) | 0.010 | INVALID |
| **Overall (reported)** | 1-100 | 2.0% (2/100) | 0.029 | **INVALID** |

### Output Analysis

**Tests 1-7:** Normal Goose responses (avg 1,030 characters)
```
Example (Test 2 - PASSED):
"I'll look up the title for PMID:28027860 using the Europe PMC database.
The title of PMID:28027860 is: 'From nocturnal frontal lobe epilepsy to
Sleep-Related Hypermotor Epilepsy: A 35-year diagnostic challenge'"
```

**Tests 9-100:** Only session startup messages (avg 289 characters)
```
Example (Test 9 - FAILED):
"starting session | provider: anthropic model: claude-sonnet-4-20250514
logging to /Users/jtr4v/.local/share/goose/sessions/20251104_203808.jsonl
working directory: /Users/jtr4v/PythonProject/mcp_literature_eval/eval_workdir/..."
```

## Impact on Experiment 2 Results

### Current (Invalid) Results
```
gpt-5:           29.0% ✓ VALID
gpt-4o:          15.0% ✓ VALID
claude-sonnet-4:  2.0% ✗ INVALID (credit limit)
```

### Extrapolated True Performance

Based on tests 1-7 (before credit limit), the projected performance would be:
```
claude-sonnet-4: ~28-29% (similar to gpt-5)
```

This would completely change the interpretation:
- **Current conclusion**: "Model choice significantly affects Goose (27pp spread, gpt-5 >> claude)"
- **Corrected conclusion**: "gpt-5 and claude-sonnet-4 perform similarly (~29%), both better than gpt-4o (15%)"

## Comparison with Experiment 1

In Experiment 1, Goose with claude-sonnet-4 achieved **15.0%** across all 100 tests.

The discrepancy between:
- Exp1: 15% (100 tests completed)
- Exp2 tests 1-7: 28.6% (before credit limit)

This 13.6pp difference needs investigation. Possible explanations:
1. **Random variation** in the first 7 tests (small sample)
2. **Different model version** or API behavior
3. **Test difficulty** - the first 7 tests may have been easier
4. **Configuration differences** between experiments

## Required Action

**Re-run Goose + claude-sonnet-4 evaluation with sufficient API credits.**

The current results (`goose_claude_20251104.yaml`) should be:
1. Marked as INVALID
2. Excluded from analysis
3. Replaced with a complete 100-test run

## File Status

- **File**: `results/compare_models/goose_claude_20251104.yaml`
- **Status**: INVALID - DO NOT USE
- **Reason**: Credit limit hit on test 8/100
- **Valid tests**: Only tests 1-7 (7% of dataset)
- **Action needed**: Complete re-run with adequate credits

## Lesson Learned

For future expensive model evaluations:
1. Check credit balance before starting 100-test runs
2. Monitor cost during execution
3. Consider running a smaller pilot (e.g., 10 tests) to estimate total cost
4. Set up cost alerts in API dashboard

---

**Status**: Awaiting re-run with sufficient Anthropic API credits
**Date identified**: 2025-11-05
