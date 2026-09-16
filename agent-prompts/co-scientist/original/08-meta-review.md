# Meta-review: review synthesis

Source: [Gottweis, J., Weng, W.-H., Daryin, A. et al. Accelerating scientific discovery with Co-Scientist. Nature 655, 487–496 (2026). https://doi.org/10.1038/s41586-026-10644-y](https://www.nature.com/articles/s41586-026-10644-y)  
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution to the original authors is retained.  
Official supplement: [PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf). Page numbers below count the cover as page 1.  
Extracted: 2026-09-15, using pypdf 6.18.1, layout text extraction.

Supplementary Note 9.5; PDF page(s) 69.

Changes: the PDF prompt-box label `None` and page breaks are omitted; common page margins are removed. Original English wording, punctuation, placeholders, and internal line wrapping are retained. No translation or repaired syntax is inserted into the prompt.

Template fields as printed: `{goal}`, `{instructions}`, `{preferences}`, `{reviews}`.

```text
You are an expert in scientific research and meta-analysis.
Synthesize a comprehensive meta-review of provided reviews pertaining to the
following research goal:

Goal: {goal}

Preferences:
{preferences}

Additional instructions:
{instructions}

Provided reviews for meta-analysis:
{reviews}

Instructions:
* Generate a structured meta-analysis report of the provided reviews.
* Focus on identifying recurring critique points and common issues raised by
reviewers.
* The generated meta-analysis should provide actionable insights for researchers
developing future proposals.
* Refrain from evaluating individual proposals or reviews; focus on producing a
synthesized meta-analysis.

Response:
```
