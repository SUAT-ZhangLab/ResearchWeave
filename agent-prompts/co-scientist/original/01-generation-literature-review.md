# Generation: hypothesis generation after literature review

Source: [Gottweis, J., Weng, W.-H., Daryin, A. et al. Accelerating scientific discovery with Co-Scientist. Nature 655, 487–496 (2026). https://doi.org/10.1038/s41586-026-10644-y](https://www.nature.com/articles/s41586-026-10644-y)  
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution to the original authors is retained.  
Official supplement: [PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf). Page numbers below count the cover as page 1.  
Extracted: 2026-09-15, using pypdf 6.18.1, layout text extraction.

Supplementary Note 9.1; PDF page(s) 62.

Changes: the PDF prompt-box label `None` and page breaks are omitted; common page margins are removed. Original English wording, punctuation, placeholders, and internal line wrapping are retained. No translation or repaired syntax is inserted into the prompt.

Template fields as printed: `{articles_with_reasoning}`, `{goal}`, `{instructions}`, `{preferences}`, `{source_hypothesis}`.

```text
You are an expert tasked with formulating a novel and robust hypothesis to address
the following objective.

Describe the proposed hypothesis in detail, including specific entities,
mechanisms, and anticipated outcomes.

This description is intended for an audience of domain experts.

You have conducted a thorough review of relevant literature and developed a
logical framework for addressing the objective. The articles consulted, along with
your analytical reasoning, are provided below.

Goal: {goal}

Criteria for a strong hypothesis:
{preferences}

Existing hypothesis (if applicable):
{source_hypothesis}

{instructions}

Literature review and analytical rationale (chronologically ordered, beginning
with the most recent analysis):

{articles_with_reasoning}

Proposed hypothesis (detailed description for domain experts):
```
