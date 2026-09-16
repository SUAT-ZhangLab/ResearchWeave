# Overview

As single-cell technologies advance, single-cell datasets are growing both in
size and complexity. Especially in consortia such as the Human Cell Atlas,
individual studies combine data from multiple labs, each sequencing multiple
individuals possibly with different technologies. This gives rise to complex
batch effects in the data that must be computationally removed to perform a
joint analysis.

This task aims to develop a superhuman method for batch integration of
single-cell RNA-seq data which must remove the batch effect while not removing
relevant biological information. The input data is unnormalized raw gene
expression count data with multiple batches and consistent cell type labels. The
batch integrated output can be a low dimensional embedding of the data or a
feature matrix. The respective batch-integrated representation is then evaluated
using sets of metrics that capture how well batch effects are removed and
whether biological variance is conserved. There are over 200 methods developed
by humans for carrying this out and the goal is to develop methods that are
better than humans.