# Ranking: hypothesis comparison during tournament

Source: [Gottweis, J., Weng, W.-H., Daryin, A. et al. Accelerating scientific discovery with Co-Scientist. Nature 655, 487–496 (2026). https://doi.org/10.1038/s41586-026-10644-y](https://www.nature.com/articles/s41586-026-10644-y)  
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution to the original authors is retained.  
Official supplement: [PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf). Page numbers below count the cover as page 1.  
Extracted: 2026-09-15, using pypdf 6.18.1, layout text extraction.

Supplementary Note 9.3; PDF page(s) 65–66.

Changes: the PDF prompt-box label `None` and page breaks are omitted; common page margins are removed. Original English wording, punctuation, placeholders, and internal line wrapping are retained. No translation or repaired syntax is inserted into the prompt.

Template fields as printed: `{goal}`, `{hypothesis 1}`, `{hypothesis 2}`, `{idea_attributes}`, `{notes}`, `{preferences}`, `{review 1}`, `{review 2}`.

```text
You are an expert evaluator tasked with comparing two hypotheses.

Evaluate the two provided hypotheses (hypothesis 1 and hypothesis 2) and determine
which one is superior based on the specified {idea_attributes}.
Provide a concise rationale for your selection, concluding with the phrase "better
idea: <1 or 2>".

Goal: {goal}

Evaluation criteria:
{preferences}

Considerations:
{notes}
Each hypothesis includes an independent review. These reviews may contain
numerical scores. Disregard these scores in your comparative analysis, as they may
not be directly comparable across reviews.

Hypothesis 1:
{hypothesis 1}

Hypothesis 2:
{hypothesis 2}

Review of hypothesis 1:
{review 1}

Review of hypothesis 2:
{review 2}

Reasoning and conclusion (end with "better hypothesis: <1 or 2>"):
```
