# Custom GEval Implementation Plan

**Date:** 2025-11-25
**Status:** In Progress
**Related PR:** https://github.com/ai4curation/metacoder/pull/37

## Objective

Update test case evaluations to use custom GEval criteria for more precise and appropriate evaluation based on test type. This leverages the new MetricConfig capabilities added to metacoder.

## Background

### Current State
- All 25 test cases use simple string-based `- CorrectnessMetric`
- No custom evaluation criteria or steps
- Generic DeepEval default behavior for all test types
- Test cases already refactored into DRY structure (test_cases.yaml)

### New Capabilities (metacoder PR #37)
The metacoder custom GEval PR adds three configuration options:

1. **`criteria`**: Single evaluation criterion (auto-generates steps)
2. **`evaluation_steps`**: List of specific evaluation steps (more granular control)
3. **`rubric`**: Structured scoring guidelines with score ranges

**Rules:**
- `criteria` and `evaluation_steps` are mutually exclusive
- Must provide at least one of: `criteria`, `evaluation_steps`, or `rubric`
- Can combine `rubric` with either `criteria` or `evaluation_steps`

### Test Categories

Our 25 test cases fall into 6 categories:

| Category | Count | Test Names |
|----------|-------|------------|
| Text extraction | 10 | PMID_28027860_Full_Text, PMID_28027860_References, 10_1016_j_seizure_2016_11_023_Full_Text, 10_1371_journal_pone_0000217_Full_Text_A, 10_1038_nature12373_Full_Text, PMC2824148_Full_Text, 10_1038_s41564_022_01094_z_Full_Text_A, 10_1038_s41564_022_01094_z_Full_Text_B, PMID_32198168_nan, PMC117972_Full_Text |
| Metadata | 4 | PMID_28027860_Title, PMC2824148_Metadata, PMC5152751_Metadata, PMC3815380_PDF |
| Table / Figure / Figure Legend extraction | 4 | NBK1256, PMID_40307501_Figure_Legend, PMID_12089011_Full_Text, PMC3368421_nan |
| Supplementary material | 3 | 10_1371_journal_pone_0000217_Full_Text_B, 10_1038_nature12373_Supplementary_Material_A, 10_1038_nature12373_Supplementary_Material_B |
| Summarization | 2 | PMID_28027860_Table, PMC8086273_Retraction |
| Publication status | 2 | PMC4831113_Full_Text, PMC4831113_Retraction |

## Version Tracking Requirements

**CRITICAL:** Before rerunning evaluations, we must capture exact versions of:

### 1. Agent Versions
- `claude-code`: Check via `claude --version` or package.json
- `goose`: Check via `goose --version` or pip/uv list

### 2. MCP Server Versions
- `artl-mcp`: Check via `uvx artl-mcp --version` or package metadata
- `mcp-simple-pubmed`: Check via `uvx mcp-simple-pubmed --version`
- `biomcp-python`: Check via `uv pip show biomcp-python`
- `pubmed-mcp`: Check git commit hash from https://github.com/chrismannina/pubmed-mcp

### 3. LLM Model Versions
- Claude Sonnet 4: `claude-sonnet-4-20250514` (already in config)
- GPT-4o: Check exact model string in config
- GPT-4o-mini: Check exact model string in config
- GPT-5: Check exact model string in config
- Gemini: Check exact model string in config

### 4. Metacoder Version
- Version: 0.1.0 (currently installed)
- Git commit hash if using development version

### Implementation
Create `notes/evaluation_run_metadata.yaml` to capture all versions before each run.

## Test Case Review

We will review all 25 test cases one by one to determine appropriate custom GEval criteria.

### Review Process
For each test case, we will decide:
1. Which configuration type to use: `criteria`, `evaluation_steps`, or `rubric`
2. Specific evaluation instructions
3. Whether to use threshold (current: 0.9 for all)

### Test Case Analysis

---

#### 1. PMID_28027860_Full_Text
- **Group:** Text extraction
- **Input:** "What is the first sentence of section 2 in PMID:28027860?"
- **Expected:** "Even though many of NFLE's core features have been clarified in the last two decades, some critical issues remain controversial."
- **Current threshold:** 0.9
- **Type:** Exact verbatim text extraction

**Proposed metric:** TBD (pending review)

---

#### 2. PMID_28027860_Title
- **Group:** Metadata
- **Input:** "What is the title of PMID:28027860?"
- **Expected:** "From nocturnal frontal lobe epilepsy to Sleep-Related Hypermotor Epilepsy: A 35-year diagnostic challenge"
- **Current threshold:** 0.9
- **Type:** Metadata extraction (title)

**Proposed metric:** TBD (pending review)

---

#### 3. PMID_28027860_Table
- **Group:** Summarization
- **Input:** "According to PMID:28027860, what are the three levels of certainty for SHE?"
- **Expected:** "witnessed,video-documented,Video-EEG documented"
- **Current threshold:** 0.9
- **Type:** Information extraction from table (requires finding and understanding)

**Proposed metric:** TBD (pending review)

---

#### 4. PMID_28027860_References
- **Group:** Text extraction
- **Input:** "Find the citation in the paper PMID:28027860 for the claim 'The clinical spectrum of NFLS comprises distinct paroxysmal sleep-related attacks of variable duration and complexity'. What is the title of cited paper?"
- **Expected:** "The concept of paroxysmal nocturnal dystonia"
- **Current threshold:** 0.9
- **Type:** Reference extraction (exact title)

**Proposed metric:** TBD (pending review)

---

#### 5. 10_1016_j_seizure_2016_11_023_Full_Text
- **Group:** Text extraction
- **Input:** "What is the first sentence of the last paragraph from 10.1016/j.seizure.2016.11.023, before the Conflict of Interest statement?"
- **Expected:** "SHE diagnosis is primarily based on the clinical history."
- **Current threshold:** 0.9
- **Type:** Exact verbatim text extraction

**Proposed metric:** TBD (pending review)

---

#### 6. NBK1256
- **Group:** Table / Figure / Figure Legend extraction
- **Input:** "What is the last row of Table 2 in NBK1256?"
- **Expected:** "Cone-rod dystrophy,70%,Loss of central vision & color vision\nAbnormal fundoscopic exam"
- **Current threshold:** 0.9
- **Type:** Table data extraction
- **Note:** Comment says "often randomly hangs on this test"

**Proposed metric:** TBD (pending review)

---

#### 7. PMID_40307501_Figure_Legend
- **Group:** Table / Figure / Figure Legend extraction
- **Input:** "What is the first sentence of Figure 1 legend from PMID 40307501?"
- **Expected:** "Proposed system for bio-accelerated weathering of ultramafic materials for carbon mineralization."
- **Current threshold:** 0.9
- **Type:** Exact sentence from figure legend
- **Note:** Comment says "The legend is truncated in the default web view."

**Proposed metric:** TBD (pending review)

---

#### 8. 10_1371_journal_pone_0000217_Full_Text_A
- **Group:** Text extraction
- **Input:** "Convert the PDF for DOI 10.1371/journal.pone.0000217 to text and tell me the first sentence of the last paragraph of the Conclusions section."
- **Expected:** "However, phenotypic complexity remains an inherently abstract metric."
- **Current threshold:** 0.9
- **Type:** Exact verbatim text extraction

**Proposed metric:** TBD (pending review)

---

#### 9. 10_1371_journal_pone_0000217_Full_Text_B
- **Group:** Supplementary material
- **Input:** "How many appendices are in 10.1371/journal.pone.0000217?"
- **Expected:** "3"
- **Current threshold:** 0.9
- **Type:** Count/number extraction

**Proposed metric:** TBD (pending review)

---

#### 10. 10_1038_nature12373_Full_Text
- **Group:** Text extraction
- **Input:** "Get the full text content for DOI 10.1038/nature12373 and tell me the first sentence of the Methods Summary."
- **Expected:** "Nanodiamond measurement pulse sequence."
- **Current threshold:** 0.9
- **Type:** Exact verbatim text extraction

**Proposed metric:** TBD (pending review)

---

#### 11. 10_1038_nature12373_Supplementary_Material_A
- **Group:** Supplementary material
- **Input:** "What supplementary files are available for PMC4221854?"
- **Expected:** "NIHMS636072-supplement-supplemental_info.pdf"
- **Current threshold:** 0.9
- **Type:** Exact filename

**Proposed metric:** TBD (pending review)

---

#### 12. 10_1038_nature12373_Supplementary_Material_B
- **Group:** Supplementary material
- **Input:** "What is the figure legend for Figure S3 in 10.1038/nature12373?"
- **Expected:** "Fluorescence spectrum under green excitation of gold nanoparticles (blue data) and nanodiamonds (red data). The shaded region indicates the bandpass filter used for detection of gold. The arrows mark the respective y-axis scaling for each curve."
- **Current threshold:** 0.9
- **Type:** Exact text from supplementary figure legend
- **Note:** Comment says "Requires download of supplemental file and text extraction."

**Proposed metric:** TBD (pending review)

---

#### 13. PMC2824148_Full_Text
- **Group:** Text extraction
- **Input:** "What is the last sentence of PMC2824148 before the Acknowledgments?"
- **Expected:** "As far as the future work is concerned, it would be interesting to study the design of efficient spaced seeds for protein sequence search (see [6]), as well as to combine spaced seeds with other techniques such as seed families [17, 20, 16] or the group hit criterion [19]."
- **Current threshold:** 0.9
- **Type:** Exact verbatim text extraction
- **Note:** Comment says "Acknowledgments vs Acknowledgements?"

**Proposed metric:** TBD (pending review)

---

#### 14. PMC2824148_Metadata
- **Group:** Metadata
- **Input:** "What is the DOI for the final published version of PMC2824148?"
- **Expected:** "10.1142/S0219720006001977"
- **Current threshold:** 0.9
- **Type:** Metadata extraction (DOI)

**Proposed metric:** TBD (pending review)

---

#### 15. 10_1038_s41564_022_01094_z_Full_Text_A
- **Group:** Text extraction
- **Input:** "What are the main section headers in PMC8975739?"
- **Expected:** "Abstract,Main,Results,Discussion,Methods,Supplementary information,Acknowledgements,Author contributions,Peer review,Data availability,Code availability,Competing interests,Footnotes,References,Associated Data"
- **Current threshold:** 0.9
- **Type:** List of section headers (order and completeness matter)

**Proposed metric:** TBD (pending review)

---

#### 16. 10_1038_s41564_022_01094_z_Full_Text_B
- **Group:** Text extraction
- **Input:** "What is the longest section in PMID:35365791?"
- **Expected:** "Methods"
- **Current threshold:** 0.9
- **Type:** Analysis/comparison result (single word answer)

**Proposed metric:** TBD (pending review)

---

#### 17. PMID_12089011_Full_Text
- **Group:** Table / Figure / Figure Legend extraction
- **Input:** "What is the first footnote of Table 3 in PMID:12089011?"
- **Expected:** "a. Grouping at 89% similarity"
- **Current threshold:** 0.9
- **Type:** Exact text from table footnote
- **Note:** Comment says "Landscape Table orientation"

**Proposed metric:** TBD (pending review)

---

#### 18. PMC5152751_Metadata
- **Group:** Metadata
- **Input:** "Which publisher published PMC5152751?"
- **Expected:** "Nature"
- **Current threshold:** 0.9
- **Type:** Metadata extraction (publisher)

**Proposed metric:** TBD (pending review)

---

#### 19. PMC3368421_nan
- **Group:** Table / Figure / Figure Legend extraction
- **Input:** "What is the MIGS-22 property from Table 1?"
- **Expected:** "Oxygen requirement aerobe"
- **Current threshold:** 0.9
- **Type:** Specific table cell extraction

**Proposed metric:** TBD (pending review)

---

#### 20. PMID_32198168_nan
- **Group:** Text extraction
- **Input:** "What does the data management section state in PMID:32198168?"
- **Expected:** "Clinical data were collected into a Microsoft Excel 2010 database that was password protected."
- **Current threshold:** 0.9
- **Type:** Exact verbatim text extraction

**Proposed metric:** TBD (pending review)

---

#### 21. PMC3815380_PDF
- **Group:** Metadata
- **Input:** "Who was the Reviews and Special Issue editor for PMC3815380?"
- **Expected:** "Juan L. Ramos"
- **Current threshold:** 0.9
- **Type:** Metadata extraction (editor name)

**Proposed metric:** TBD (pending review)

---

#### 22. PMC117972_Full_Text
- **Group:** Text extraction
- **Input:** "What is the first sentence of the Microarray Analysis section in PMC117972?"
- **Expected:** "A global representation of the changes in expression of all the expressed sequence tags (ESTs) on the microarray is depicted in Figure 1."
- **Current threshold:** 0.9
- **Type:** Exact verbatim text extraction
- **Note:** Comment says "pubmedmcp consistently hangs on this test case"

**Proposed metric:** TBD (pending review)

---

#### 23. PMC4831113_Full_Text
- **Group:** Text extraction
- **Input:** "Show the Conclusions section of PMC4831113."
- **Expected:** "This article has been retracted. However, the Conclusions section stated the following: On the basis of phenotypic, phylogenetic and genomic analyses, we formally propose the creation of Haemophilus massiliensis sp. nov. that contains strain FF7T (CSUR P859 = DSM 28247) which is the type strain The strain was isolated from a peritoneal fluid specimen from a 44-year-old Senegalese woman admitted to Hôpital Principal in Dakar, Senegal."
- **Current threshold:** 0.9
- **Type:** Complex - must recognize retraction AND provide conclusion text

**Proposed metric:** TBD (pending review)

---

#### 24. PMC4831113_Retraction
- **Group:** Publication status
- **Input:** "Is PMC4831113 retracted?"
- **Expected:** "Yes"
- **Current threshold:** 0.9
- **Type:** Binary yes/no about retraction status

**Proposed metric:** TBD (pending review)

---

#### 25. PMC8086273_Retraction
- **Group:** Summarization
- **Input:** "Based on PMID 33926573 do microbes from alkaline sulphidic tailings show oxidative stresses? Is this finding from this paper reliable?"
- **Expected:** "The paper says no, microbes from alkaline sulphidic tailings do not show oxidative stresses, but it is retracted so the results should not be trusted."
- **Current threshold:** 0.9
- **Type:** Complex - extract finding AND evaluate reliability based on retraction
- **Note:** Comment says "this test case is kind of tricky and it seems like an extremely difficult case that even a good LLM + MCP might not pass. We've made some edits to give the LLM + MCP a fair chance"

**Proposed metric:** TBD (pending review)

---

## Decision Log

### General Principles (APPROVED 2025-11-25)

1. **No penalty for extra explanations**: Agents can provide context around answers without being penalized
2. **Flexible formatting**: Minor punctuation, whitespace, and formatting differences are acceptable
3. **Partial credit where appropriate**: Use evaluation_steps or rubrics to allow proportional scoring
4. **Keep thresholds at 0.9**: No changes to existing thresholds

### Approved Custom Metrics by Category

#### 1. Text Extraction (10 cases)
**Standard metric for most cases:**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check whether the actual output contains the exact text from expected output"
      - "The text must be verbatim, not paraphrased"
      - "Minor punctuation or whitespace differences are acceptable"
```

**Special case - Section headers list (10_1038_s41564_022_01094_z_Full_Text_A):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check how many section headers from the expected output are present in the actual output"
      - "Give partial credit proportional to the percentage of correct headers"
      - "Headers should be in the correct order when present"
      - "Minor formatting differences (spacing, capitalization) are acceptable"
```

**Special case - Retracted paper conclusion (PMC4831113_Full_Text):**
- Updated expected_output to remove "This article has been retracted. However, the Conclusions section stated the following:" prefix
- New expected: "On the basis of phenotypic, phylogenetic and genomic analyses..."
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check whether the actual output contains the exact text from expected output"
      - "The text must be verbatim, not paraphrased"
      - "Minor punctuation or whitespace differences are acceptable"
      - "Do not penalize if the output also mentions the article has been retracted"
```

#### 2. Metadata (4 cases)
**Standard metadata metric:**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if the [field] matches the expected output"
      - "Minor formatting differences are acceptable"
      - "The core [field] must be identical"
```

**Special case - DOI (PMC2824148_Metadata):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if the DOI exactly matches the expected output"
      - "Accept the DOI with or without 'https://doi.org/' prefix"
      - "Minor punctuation or formatting differences are acceptable"
      - "The core DOI must be identical"
```

**Special case - Publisher (PMC5152751_Metadata):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if the publisher name matches the expected output"
      - "Accept 'Nature' or 'Nature Publishing Group' as correct"
      - "Minor formatting differences are acceptable"
```

#### 3. Table / Figure / Figure Legend extraction (4 cases)
**Table row extraction (NBK1256):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check whether the actual output contains the table row data from expected output"
      - "The data values must match (Cone-rod dystrophy, 70%, Loss of central vision & color vision, Abnormal fundoscopic exam)"
      - "Allow minor formatting differences in how the row is presented (spacing, delimiters)"
      - "All data fields from the row must be present in the correct order"
```

**Figure legend / table footnote / table cell (others):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check whether the actual output contains the exact text from expected output"
      - "The text must be verbatim, not paraphrased"
      - "Minor punctuation or whitespace differences are acceptable"
```

#### 4. Supplementary material (3 cases)
**Count (10_1371_journal_pone_0000217_Full_Text_B):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if the actual output contains the number from expected output"
      - "Accept the number with or without additional context (e.g., '3' or 'There are 3 appendices')"
      - "The numeric value must be correct"
```

**Filename (10_1038_nature12373_Supplementary_Material_A):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if the actual output contains the filename from expected output"
      - "Accept the filename with or without additional context"
      - "The core filename must be present and identical"
      - "Minor formatting differences are acceptable"
```

**Figure legend from supplement (10_1038_nature12373_Supplementary_Material_B):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check whether the actual output contains the exact text from expected output"
      - "The text must be verbatim, not paraphrased"
      - "Minor punctuation or whitespace differences are acceptable"
```

#### 5. Summarization (2 cases)
**List extraction (PMID_28027860_Table):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if all three levels of certainty are present in the actual output"
      - "The three levels are: witnessed, video-documented, Video-EEG documented"
      - "Allow minor formatting differences (capitalization, spacing, delimiters)"
      - "All three items must be present"
```

**Complex synthesis with retraction (PMC8086273_Retraction):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if the output correctly states the paper's finding (no oxidative stresses)"
      - "Check if the output mentions the paper is retracted"
      - "Check if the output indicates the results should not be trusted due to retraction"
      - "Allow paraphrasing as long as the key points are present"
    rubric:
      - score: 0.0
        criteria: "Does not address the question or provides completely incorrect information"
      - score: 0.3
        criteria: "Mentions only the finding OR only the retraction, but not both"
      - score: 0.6
        criteria: "Mentions both the finding and retraction, but doesn't connect them to reliability"
      - score: 1.0
        criteria: "Correctly states the finding, mentions retraction, and indicates results shouldn't be trusted"
```

#### 6. Publication status (2 cases)
**Binary retraction check (PMC4831113_Retraction):**
```yaml
metrics:
  - name: CorrectnessMetric
    evaluation_steps:
      - "Check if the output indicates the paper is retracted"
      - "Accept 'Yes' or any affirmative statement that the paper is retracted"
      - "The answer must clearly indicate retraction status is positive"
```

## Implementation Steps

1. ✅ Create this plan document
2. ⏳ Review all 25 test cases one by one with user input
3. ⏳ Update test_cases.yaml with approved custom GEval definitions
4. ⏳ Run generate_configs.py to regenerate all agent config files
5. ⏳ Capture version metadata for all components
6. ⏳ Run metacoder evaluations
7. ⏳ Rerun analysis notebooks if needed
8. ⏳ Document results and compare with previous runs

## Next Steps

Start with test case #1 and work through all 25 systematically with user approval.
