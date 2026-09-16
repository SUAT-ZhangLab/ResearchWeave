# Reflection: observations explained or contradicted by a hypothesis

Source: [Gottweis, J., Weng, W.-H., Daryin, A. et al. Accelerating scientific discovery with Co-Scientist. Nature 655, 487–496 (2026). https://doi.org/10.1038/s41586-026-10644-y](https://www.nature.com/articles/s41586-026-10644-y)  
License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Attribution to the original authors is retained.  
Official supplement: [PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-026-10644-y/MediaObjects/41586_2026_10644_MOESM1_ESM.pdf). Page numbers below count the cover as page 1.  
Extracted: 2026-09-15, using pypdf 6.18.1, layout text extraction.

Supplementary Note 9.2; PDF page(s) 64–65.

Changes: the PDF prompt-box label `None` and page breaks are omitted; common page margins are removed. Original English wording, punctuation, placeholders, and internal line wrapping are retained. No translation or repaired syntax is inserted into the prompt.

Template fields as printed: `{article}`, `{hypothesis}`.

```text
You are an expert in scientific hypothesis evaluation. Your task is to analyze the
relationship between a provided hypothesis and observations from a scientific
article. Specifically, determine if the hypothesis provides a novel causal
explanation for the observations, or if they contradict it.

Instructions:

1. Observation extraction: list relevant observations from the article.
2. Causal analysis (individual): for each observation:
   a. State if its cause is already established.
   b. Assess if the hypothesis could be a causal factor (hypothesis =>
observation). Start with: "would we see this observation if the hypothesis was
true:".
   c. Explain if it's a novel explanation. If not, or if a better explanation
exists, state: "not a missing piece."
3. Causal analysis (summary): determine if the hypothesis offers a novel
explanation for a subset of observations. Include reasoning. Start with: "would we
see some of the observations if the hypothesis was true:".
4. Disproof analysis: determine if any observations contradict the hypothesis.
Start with: "does some observations disprove the hypothesis:".
5. Conclusion: state: "hypothesis: <already explained, other explanations more
likely, missing piece, neutral, or disproved>".

Scoring:
* Already explained: hypothesis consistent, but causes are known. No novel
explanation.
* Other explanations more likely: hypothesis *could* explain, but better
explanations exist.
* Missing piece: hypothesis offers a novel, plausible explanation.

* Neutral: hypothesis neither explains nor is contradicted.
* Disproved: observations contradict the hypothesis.

Important: if observations are expected regardless of the hypothesis, and don't
disprove it, it's neutral.

Article:
{article}

Hypothesis:
{hypothesis}

Response {provide reasoning. end with: "hypothesis: <already explained, other
explanations more likely, missing piece, neutral, or disproved>".)
```
