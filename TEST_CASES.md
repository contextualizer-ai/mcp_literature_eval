# MCP Literature Evaluation Test Cases

This document describes the 25 test cases used to evaluate MCP server performance for scientific literature retrieval.

**Location:** Test cases are defined in the `cases:` section of each evaluation configuration file (`project/literature_mcp_eval_config*.yaml`).

**Evaluation:** Each case is tested against 4 MCP servers (artl, simple-pubmed, biomcp, pubmed-mcp), resulting in 100 evaluations per agent/model.

**Scoring:** Responses are evaluated using semantic similarity (DeepEval CorrectnessMetric) with a pass threshold of 0.9 (90% match).

---

## Summary by Category

| Category | Count | Description |
|----------|-------|-------------|
| Text extraction | 11 | Retrieving specific sentences, paragraphs, or sections from papers |
| Metadata | 4 | Extracting bibliographic information (title, DOI, publisher) |
| Summarization | 2 | Synthesizing information from paper content |
| Table/Figure/Legend extraction | 4 | Retrieving structured data and figure captions |
| Supplementary material | 3 | Accessing supplemental files and their contents |
| Publication status | 1 | Detecting retracted papers |

---

## Test Cases

### 1. Text Extraction (11 cases)

Test cases that require extracting specific text content from papers.

| # | Case Name | Question | Expected Answer | Paper |
|---|-----------|----------|----------------|-------|
| 1 | PMID_28027860_Full_Text | What is the first sentence of section 2 in PMID:28027860? | "Even though many of NFLE's core features have been clarified in the last two decades, some critical issues remain controversial." | PMID:28027860 |
| 2 | PMID_28027860_References | Find the citation in the paper PMID:28027860 for the claim 'The clinical spectrum of NFLS comprises distinct paroxysmal sleep-related attacks of variable duration and complexity'. What is the title of cited paper? | "The concept of paroxysmal nocturnal dystonia" | PMID:28027860 |
| 3 | 10_1016_j_seizure_2016_11_023_Full_Text | What is the first sentence of the last paragraph from 10.1016/j.seizure.2016.11.023, before the Conflict of Interest statement? | "SHE diagnosis is primarily based on the clinical history." | DOI:10.1016/j.seizure.2016.11.023 |
| 4 | 10_1371_journal_pone_0000217_Full_Text_A | Convert the PDF for DOI 10.1371/journal.pone.0000217 to text and tell me the first sentence of the last paragraph of the Conclusions section. | "However, phenotypic complexity remains an inherently abstract metric." | DOI:10.1371/journal.pone.0000217 |
| 5 | 10_1038_nature12373_Full_Text | Get the full text content for DOI 10.1038/nature12373 and tell me the first sentence of the Methods Summary. | "Nanodiamond measurement pulse sequence." | DOI:10.1038/nature12373 |
| 6 | PMC2824148_Full_Text | What is the last sentence of PMC2824148 before the Acknowledgments? | "As far as the future work is concerned, it would be interesting to study the design of efficient spaced seeds for protein sequence search (see [6]), as well as to combine spaced seeds with other techniques such as seed families [17, 20, 16] or the group hit criterion [19]." | PMC2824148 |
| 7 | 10_1038_s41564_022_01094_z_Full_Text_A | What are the main section headers in PMC8975739? | "Abstract,Main,Results,Discussion,Methods,Supplementary information,Acknowledgements,Author contributions,Peer review,Data availability,Code availability,Competing interests,Footnotes,References,Associated Data" | PMC8975739 |
| 8 | 10_1038_s41564_022_01094_z_Full_Text_B | What is the longest section in PMID:35365791? | "Methods" | PMID:35365791 |
| 9 | PMID_32198168_nan | What does the data management section state in PMID:32198168? | "Clinical data were collected into a Microsoft Excel 2010 database that was password protected." | PMID:32198168 |
| 10 | PMC117972_Full_Text | What is the first sentence of the Microarray Analysis section in PMC117972? | "A global representation of the changes in expression of all the expressed sequence tags (ESTs) on the microarray is depicted in Figure 1." | PMC117972 |
| 11 | PMC4831113_Full_Text | Show the Conclusions section of PMC4831113. | "This article has been retracted. However, the Conclusions section stated the following: On the basis of phenotypic, phylogenetic and genomic analyses, we formally propose the creation of Haemophilus massiliensis sp. nov. that contains strain FF7T (CSUR P859 = DSM 28247) which is the type strain The strain was isolated from a peritoneal fluid specimen from a 44-year-old Senegalese woman admitted to Hôpital Principal in Dakar, Senegal." | PMC4831113 |

### 2. Metadata (4 cases)

Test cases that extract bibliographic metadata.

| # | Case Name | Question | Expected Answer | Paper |
|---|-----------|----------|----------------|-------|
| 12 | PMID_28027860_Title | What is the title of PMID:28027860? | "From nocturnal frontal lobe epilepsy to Sleep-Related Hypermotor Epilepsy: A 35-year diagnostic challenge" | PMID:28027860 |
| 13 | PMC2824148_Metadata | What is the DOI for the final published version of PMC2824148? | "10.1142/S0219720006001977" | PMC2824148 |
| 14 | PMC5152751_Metadata | Which publisher published PMC5152751? | "Nature" | PMC5152751 |
| 15 | PMC3815380_PDF | Who was the Reviews and Special Issue editor for PMC3815380? | "Juan L. Ramos" | PMC3815380 |

### 3. Summarization (2 cases)

Test cases requiring synthesis of information.

| # | Case Name | Question | Expected Answer | Paper |
|---|-----------|----------|----------------|-------|
| 16 | PMID_28027860_Table | According to PMID:28027860, what are the three levels of certainty for SHE? | "witnessed,video-documented,Video-EEG documented" | PMID:28027860 |
| 17 | PMC8086273_Retraction | Based on PMID 33926573 do microbes from alkaline sulphidic tailings show oxidative stresses? Is this finding from this paper reliable? | "The paper says no, microbes from alkaline sulphidic tailings do not show oxidative stresses, but it is retracted so the results should not be trusted." | PMID:33926573 |

### 4. Table / Figure / Figure Legend Extraction (4 cases)

Test cases requiring extraction of structured data or figure captions.

| # | Case Name | Question | Expected Answer | Paper |
|---|-----------|----------|----------------|-------|
| 18 | NBK1256 | What is the last row of Table 2 in NBK1256? | "Cone-rod dystrophy,70%,Loss of central vision & color vision\nAbnormal fundoscopic exam" | NBK1256 |
| 19 | PMID_40307501_Figure_Legend | What is the first sentence of Figure 1 legend from PMID 40307501? | "Proposed system for bio-accelerated weathering of ultramafic materials for carbon mineralization." | PMID:40307501 |
| 20 | PMID_12089011_Full_Text | What is the first footnote of Table 3 in PMID:12089011? | "a. Grouping at 89% similarity" | PMID:12089011 |
| 21 | PMC3368421_nan | What is the MIGS-22 property from Table 1? | "Oxygen requirement aerobe" | PMC3368421 |

### 5. Supplementary Material (3 cases)

Test cases accessing supplemental files.

| # | Case Name | Question | Expected Answer | Paper |
|---|-----------|----------|----------------|-------|
| 22 | 10_1371_journal_pone_0000217_Full_Text_B | How many appendices are in 10.1371/journal.pone.0000217? | "3" | DOI:10.1371/journal.pone.0000217 |
| 23 | 10_1038_nature12373_Supplementary_Material_A | What supplementary files are available for PMC4221854? | "NIHMS636072-supplement-supplemental_info.pdf" | PMC4221854 |
| 24 | 10_1038_nature12373_Supplementary_Material_B | What is the figure legend for Figure S3 in 10.1038/nature12373? | "Fluorescence spectrum under green excitation of gold nanoparticles (blue data) and nanodiamonds (red data). The shaded region indicates the bandpass filter used for detection of gold. The arrows mark the respective y-axis scaling for each curve." | DOI:10.1038/nature12373 |

### 6. Publication Status (1 case)

Test cases checking retraction status.

| # | Case Name | Question | Expected Answer | Paper |
|---|-----------|----------|----------------|-------|
| 25 | PMC4831113_Retraction | Is PMC4831113 retracted? | "Yes" | PMC4831113 |

---

## Paper Identifiers Used

The test suite uses various paper identifier types:

- **PMID** (PubMed ID): 28027860, 40307501, 12089011, 32198168, 35365791, 33926573
- **PMC** (PubMed Central ID): PMC2824148, PMC5152751, PMC3368421, PMC3815380, PMC117972, PMC4831113, PMC8086273, PMC8975739, PMC4221854
- **DOI** (Digital Object Identifier): 10.1016/j.seizure.2016.11.023, 10.1371/journal.pone.0000217, 10.1038/nature12373, 10.1038/s41564_022_01094_z
- **BookShelf ID**: NBK1256

---

## Known Issues

1. **NBK1256** - Test often hangs; may require individual execution
2. **PMC117972** - Hangs with pubmed-mcp server; known agent stability issue

---

## Adding New Test Cases

To add a new test case to the evaluation suite:

1. Edit the `cases:` section in **all** config files in `project/`
2. Use this template:

```yaml
- name: Descriptive_Name
  group: "Category"  # One of: Text extraction, Metadata, Summarization, etc.
  metrics:
  - CorrectnessMetric
  input: "Your question here"
  expected_output: "Expected answer here"
  threshold: 0.9
```

3. Verify consistency across all config files using:
```bash
md5 <(awk '/^cases:/,0' project/literature_mcp_eval_config*.yaml)
```

4. Update this document with the new test case details
