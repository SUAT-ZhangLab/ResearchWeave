# Evolution: hypothesis generation through out-of-the-box thinking

Source: [Gottweis, J., Weng, W.-H., Daryin, A. et al. Accelerating scientific discovery with Co-Scientist. Nature 655, 487–496 (2026). https://doi.org/10.1038/s41586-026-10644-y](https://www.nature.com/articles/s41586-026-10644-y)  
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution to the original authors is retained.  
Official supplement: [PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf). Page numbers below count the cover as page 1.  
Extracted: 2026-09-15, using pypdf 6.18.1, layout text extraction.

Supplementary Note 9.4; PDF page(s) 68.

Changes: the PDF prompt-box label `None` and page breaks are omitted; common page margins are removed. Original English wording, punctuation, placeholders, and internal line wrapping are retained. No translation or repaired syntax is inserted into the prompt.

Template fields as printed: `{goal}`, `{hypotheses}`, `{preferences}`.

```text
You are an expert researcher tasked with generating a novel, singular hypothesis
inspired by analogous elements from provided concepts.

Goal: {goal}

Instructions:
1. Provide a concise introduction to the relevant scientific domain.
2. Summarize recent findings and pertinent research, highlighting successful
approaches.
3. Identify promising avenues for exploration that may yield innovative
hypotheses.
4. CORE HYPOTHESIS: Develop a detailed, original, and specific single hypothesis
for achieving the stated goal, leveraging analogous principles from the provided
ideas. This should not be a mere aggregation of existing methods or entities.
Think out-of-the-box.

Criteria for a robust hypothesis:
{preferences}

Inspiration may be drawn from the following concepts (utilize analogy and
inspiration, not direct replication):
{hypotheses}

Response:
```
