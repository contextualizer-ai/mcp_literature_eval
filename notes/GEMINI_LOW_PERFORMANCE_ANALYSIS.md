# Gemini Low Performance Analysis

## Summary

Gemini's pass rate is significantly lower than Claude's (16% vs 47%). Initial investigation suggested Gemini wasn't calling MCP tools, but detailed session log analysis reveals a different story.

## Key Findings

### 1. Gemini IS Using MCP Tools

Contrary to the initial `tool_uses: null` metadata, examination of actual session logs shows:

```json
"toolCalls": [
  {
    "id": "get_pmid_text-1762279073080-732b2c0d27704",
    "name": "get_pmid_text",
    "args": {"pmid": "28027860"},
    "status": "success"
  }
]
```

**Evidence**: `eval_workdir/gemini-2-flash_gemini_PMID_28027860_Full_Text_artl/.gemini/tmp/.../session-2025-11-04T17-57-0b2dc2c3.json`

The discrepancy is likely due to how metacoder's GeminiCoder records tool usage metadata vs actual execution.

### 2. The Real Problem: Limited Content from MCP

Both Gemini AND Claude are receiving only **abstracts** from ARTL's `get_pmid_text`, not full paper text.

**Example - PMID:28027860**:

The MCP returns:
```
"From nocturnal frontal lobe epilepsy to Sleep-Related Hypermotor Epilepsy:
A 35-year diagnostic challenge.

Nocturnal frontal lobe epilepsy (NFLE) is a focal epilepsy with seizures
arising mainly during sleep... [abstract continues]"
```

But the test asks: **"What is the first sentence of section 2?"**

Expected: `"Even though many of NFLE's core features have been clarified in the last two decades, some critical issues remain controversial."`

This sentence is in the full paper text, NOT in the abstract.

### 3. Agent Response Differences

When faced with incomplete content:

**Gemini's approach**:
- Explicitly states: "The provided text does not contain explicit section numbers"
- Returns the first sentence from available content (the abstract title)
- More literal and conservative interpretation

**Claude's approach**:
- Attempts to interpret: "Based on the abstract structure, the first sentence of what appears to be the second section..."
- Makes educated guesses about what "section 2" might mean
- More creative interpretation, sometimes gets closer to expected answer by chance

### 4. Why This Affects Gemini More

| Factor | Gemini | Claude |
|--------|--------|--------|
| Conservative responses | ✓ Frequently states limitations | Less frequent |
| Creative interpretation | Lower | Higher |
| Hallucination attempts | Lower | Higher (sometimes helps!) |
| Literal tool output parsing | Higher | Lower |

**Result**: Claude's willingness to "guess" what section 2 might be (even from an abstract) occasionally produces semantically similar text to the expected answer, boosting its score.

## Failure Pattern Breakdown

From analyzing 84 failed Gemini tests:

- **Missing/Incomplete Response**: 72 failures (85.7%)
  - "The provided text does not contain..."
  - "No explicit section numbers found..."
  - Direct acknowledgment of incomplete data

- **Other**: 7 failures (8.3%)

- **Incorrect Information**: 3 failures (3.6%)

- **Execution Error**: 2 failures (2.4%)

## Tests That Passed for Both Agents

These tests worked because the MCP successfully returned the needed content:

1. `10_1038_nature12373_Supplementary_Material_A` - Supplementary file listing
2. `10_1038_s41564_022_01094_z_Full_Text_B` - Section length comparison
3. `NBK1256` - Table extraction
4. `PMC117972_Full_Text` - BioMCP (different MCP server)
5. `PMC2824148_Metadata` - Metadata query (not full text)

Notice: Metadata queries and some full-text queries succeed, suggesting ARTL has mixed coverage.

## Comparison to Claude Results

### Overall Pass Rates by MCP:

| MCP | Claude | Gemini | Difference |
|-----|--------|--------|------------|
| artl | 44.0% | 16.0% | -28.0 pp |
| biomcp | 72.0% | 20.0% | -52.0 pp |
| pubmed-mcp | 0.0% | 4.0% | +4.0 pp |
| simple-pubmed | 72.0% | 24.0% | -48.0 pp |

**Gemini is worse across all MCPs**, not just ARTL.

### Semantic Similarity Scores:

```
              count   mean   std   min   25%   50%   75%   max
claude         98.0  0.577  0.35  0.02  0.22  0.68  0.93  1.0
gemini        100.0  0.348  0.29  0.03  0.12  0.24  0.56  1.0
```

Gemini's median score (0.24) is dramatically lower than Claude's (0.68).

## Conclusions

1. **Gemini is NOT failing to use MCPs** - Session logs prove tool calls are happening
2. **Both agents struggle with incomplete MCP responses** - ARTL often returns abstracts instead of full text
3. **Gemini's conservative/literal approach hurts performance** - When content is incomplete, stating limitations lowers semantic similarity scores
4. **Claude's creative interpretation helps scores** - Even when wrong, attempts to answer can be semantically closer to expected output
5. **This is a measurement artifact** - Gemini may actually be MORE honest about data limitations, but gets penalized by CorrectnessMetric

## Recommendations

1. **Fix MCP Content Retrieval**: Investigate why ARTL's `get_pmid_text` returns abstracts vs full text
2. **Re-evaluate Scoring**: Consider whether Gemini's "honest limitation reporting" should be scored differently
3. **Test with Better MCPs**: If biomcp has better coverage, run more tests with it
4. **Prompt Engineering**: Consider adding instructions like "Try to answer even with incomplete data"

## Questions for Investigation

1. Why does ARTL return full text for some papers (PMC117972) but only abstracts for others (PMID:28027860)?
2. Is this a PMC vs PMID difference?
3. Could we prompt Gemini to be more "creative" like Claude when data is incomplete?
4. Should we add a test category specifically for "honest error reporting" vs "creative guessing"?
