**Input Format:** The input data file (`input_adata`) is an `ad.AnnData` object
that includes the main data matrix in `.X` attribute (these are input raw gene
expression counts we want to transform). The data has already been subset to
2000 highly variable genes.

**Output Format:** The output data (`output_adata`) MUST be an `ad.AnnData`
object. The transformed dataset or embedding must be stored in `X_emb` key under
`obsm` annotation.

```
output_data = ad.AnnData(
    obs=adata.obs,
    var=adata.var,
    obsm={
        'X_emb': # transformed dataset goes here.
    },
)
```

Importantly, **to remove batch effects while conserving biological factors you
may experiment with data preprocessing (e.g. via scanpy) as well as modeling.**

**Evaluation Harness and `eliminate_batch_effect_fn`:** You will implement a
function, `eliminate_batch_effect_fn`, to generate a transformed dataset that
represents the original data without batch effects. The evaluation harness will
evaluate via `score` function below whether the transformed datasets has
eliminated batch effects while preserving important biological features. In
particular, we would like to preserve cell type variation. The `score` function
implements various metrics used to measure how well you are doing on the task.
Your goal is to maximize the score from the `score` function below by writing
the best possible method/code for `eliminate_batch_effect_fn`.

**1. Objective:**

*   The goal is to create a `eliminate_batch_effect_fn` that transforms the
    dataset into a new dataset that not only eliminiates batch effects but
    preserves biological information. We will evaluate the output using average
    of the following specific metrics (after scaling):
    *   ASW Batch: Modified average silhouette width (ASW) of batch. The metric
        is scaled so that 0 indicates suboptimal batch mixing and 1 indicates
        optimal batch mixing.
    *   ASW Label: Average silhouette width of cell type labels. ASW is computed
        on cell identity labels and scaled to a value between 0 (worst) and 1
        (best).
    *   ARI: Adjusted Rand Index compares clustering overlap, correcting for
        random labels and considering correct overlaps and disagreements. The
        Adjusted Rand Index (ARI) compares the overlap of two clusterings; it
        considers both correct clustering overlaps while also counting correct
        disagreements between two clusterings. We compare the cell-type labels
        with the NMI-optimized Louvain clustering computed on the integrated
        dataset. The adjustment of the Rand index corrects for randomly correct
        labels. An ARI of 0 or 1 corresponds to random labeling or a perfect
        match, respectively. The score ranges between 0 and 1 with larger values
        indicating better conservation of the data-driven cell identity
        discovery after integration compared to annotated labels.
    *   NMI: The normalized mutual information is a version of the mutual
        information corrected by the entropy of clustering and ground truth
        labels (e.g. cell type). The score ranges between 0 and 1, with 0
        representing no sharing and 1 representing perfect sharing of
        information between clustering and annotated cell labels. NMI compares
        overlap by scaling using mean entropy terms and optimizing Louvain
        clustering to obtain the best match between clusters and labels.
        Normalized Mutual Information (NMI) compares the overlap of two
        clusterings. We use NMI to compare the cell-type labels with Louvain
        clusters computed on the integrated dataset. The overlap was scaled
        using the mean of the entropy terms for cell-type and cluster labels.
        Thus, NMI scores of 0 or 1 correspond to uncorrelated clustering or a
        perfect match, respectively. We performe optimized Louvain clustering
        for this metric to obtain the best match between clusters and labels.
    *   Graph connectivity: Connectivity of the subgraph per cell type label.
        The graph connectivity metric assesses whether the kNN graph
        representation, G, of the integrated data directly connects all cells
        with the same cell identity label. The resultant score has a range of
        (0;1], where 1 indicates that all cells with the same cell identity are
        connected in the integrated kNN graph, and the lowest possible score
        indicates a graph where no cell is connected.
    *   Isolated labels ASW: Score how well isolated labels are distinguished
        from all other labels using the average-width silhouette score. Isolated
        cell labels are defined as the labels present in the least number of
        batches in the integration task. The score evaluates how well these
        isolated labels separate from other cell identities. The isolated label
        ASW score is obtained by computing the ASW of isolated versus
        non-isolated labels on the embedding and scaling this score to be
        between 0 and 1. The final score for each metric version consists of the
        mean isolated score of all isolated labels.
    *   Isolated labels F1: Evaluate how well isolated labels coincide with
        clusters. Score how well isolated labels are distinguished from other
        labels by data-driven clustering. The F1 score is used to evaluate
        clustering with respect to the ground truth cell type labels. It returns
        a value between 0 and 1, where 1 shows that all of the isolated label
        cells and no others are captured in the cluster.
    *   kBET: kBET determines how well batches are mixed within a cell type. The
        kBET algorithm determines whether the label composition of a k nearest
        neighborhood of a cell is similar to the expected (global) label
        composition. The test is repeated for a random subset of cells, and the
        results are summarized as a rejection rate over all tested
        neighborhoods. kBET score is scaled between 0 and 1 so that larger
        scores are associated with better batch mixing.
    *   iLISI: Local inverse Simpson's Index for batch label. The metric
        assesses whether clusters of cells in a single-cell RNA-seq dataset are
        well-mixed across a categorical batch variable. The original iLISI score
        ranges from 0 to the number of categories, with the latter indicating
        good cell mixing. This is rescaled to a score between 0 and 1.
    *   cLISI: Local inverse Simpson's Index for cell type label. The metric
        assesses whether clusters of cells in a single-cell RNA-seq dataset are
        well-mixed across a categorical cell type variable. The original cLISI
        score ranges from 0 to the number of categories, with the latter
        indicating good cell mixing. This is rescaled to a score between 0
        and 1.
    *   PCR: Principal component regression compares the explained variance by
        batch before and after integration. The score ranges between 0 and 1.
        The larger the score, the more different the variance contributions are
        before and after integration.
    *   Cell cycle conservation score: Cell cycle conservation score based on
        principle component regression on cell cycle gene scores. The cell-cycle
        conservation score evaluates how well the cell-cycle effect can be
        captured before and after integration. Values close to 0 indicate lower
        conservation and 1 indicates complete conservation of the variance
        explained by cell cycle. In other words, the variance remains unchanged
        within each batch for complete conservation, while any deviation from
        the preintegration variance contribution reduces the score.

**2. Function Signature:**

*   Your `eliminate_batch_effect_fn` *must* adhere to this signature:

```python
def eliminate_batch_effect_fn(
    adata: ad.AnnData,
    config: dict[str, Any],
) -> ad.AnnData:
  # Your code here to return ad.AnnData without batch variation.
  return output_data  # ad.AnnData without batch variation
```

*   `adata`: input ad.AnnData object containing raw gene expression counts in
    `adata.X` field and batch labels in `adata.obs['batch']` field.
*   `config`: Configuration parameters (dictionary for hyperparameters, etc.).
    **Don't forget to specify parameters in this `config` dictionary.**

*   Your function **must return an ad.AnnData object** structured in the
    following way:

```python
output_data = ad.AnnData(
    obs=adata.obs,
    var=adata.var,
    obsm={
        'X_emb': # transformed dataset goes here.
    },
)
```

**Your implementation should NOT use `cell_type` information in any way.**

**3. Minimize use of specialized single-cell python packages.**

There are many python packages used in single cell genomics. The only one that
we have installed in the coding environment is scanpy. Thus, instead of using
algorithms you might be tempted to use, please write your own native description
of these algorithms using scanpy, sklearn, numpy, scipy, tensorflow, torch, jax
or equivalent. There is much room to be creative in getting rid of batch
variation using purely native tools.

**4. Data Set Size:**

Please be aware that the datafile is large and if you use the wrong algorithm
you could OOM your sandbox or the algorithm could take a long time to run. As an
example, a typical matrix size is 329,762 cells × 2,000 genes.

**5. Error Handling:**

*   The harness includes robust error handling. If your
    `eliminate_batch_effect_fn` raises an exception, the harness will catch it,
    log the traceback, assign a `worst_score`, and continue the evaluation. This
    is important to ensure that a single error doesn't halt the entire process.
    The `traceback` and any `stdout` and `stderr` output from your function are
    captured and stored.
*   Pay attention to the `first_traceback` in the output. This is the *first*
    error that occurred across all the datasets.
*   Print statements within your `eliminate_batch_effect_fn` will be captured in
    the `stdout` and `stderr` streams. Use these judiciously for debugging.

**6. Configuration:**

*   The `config` dictionary is passed to your `eliminate_batch_effect_fn`,
    allowing you to parameterize your model. You should design your function to
    utilize the values in the `config` dictionary.

**7. Deliverable:**

*   Implement the `eliminate_batch_effect_fn` function to return an `ad.AnnData`
    object in `X_emb` key under `obsm` annotation.
*   Specify hyperparameters in the `config` dictionary. This dictionary will be
    passed as an argument to your `eliminate_batch_effect_fn`.

**8. Major advice:**

*   An expert has identified the following method as a promising candidate for
    solving batch integration:
    *   Conditional Variational Autoencoder trained on gene expression,
        conditioned on batch ID. Latent space explicitly split into biological
        and batch components. Loss combines reconstruction error, KL divergence
        for both latent components, and an adversarial loss (via gradient
        reversal layer) penalizing batch information within the biological
        component. Output is the batch-corrected biological latent embedding.