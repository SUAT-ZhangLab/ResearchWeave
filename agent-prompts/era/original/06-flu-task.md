## **Problem Statement & Your Deliverable**

Your primary task is to create a forecasting model that predicts **probabilistic forecasts** of **Total Influenza Hospital Admissions** for every US state and jurisdiction. The goal is to create a model that achieves the lowest possible **Weighted Interval Score (WIS)** over a rolling-window evaluation.

Your deliverable is a single Python function, `fit_and_predict_fn`, that takes in training and test data and returns a pandas DataFrame containing the required quantile predictions.

---

### **Implementation Details**

**1. Function Signature & Output Requirements**

Your forecasting model **must** be encapsulated within a function named `fit_and_predict_fn` that adheres to the following signature.

*   **Function Signature:**
    ```python
    def fit_and_predict_fn(
        train_x: pd.DataFrame,
        train_y: pd.Series,
        test_x: pd.DataFrame,
    ) -> pd.DataFrame:
        # Your code here to train your model and generate quantile predictions
        return test_y_hat_quantiles
    ```

*   **Output Format:** Your function **must return a pandas DataFrame** with the following properties:
    *   The **index must match** the index of the input `test_x` DataFrame.
    *   The **columns must be named** according to the required quantiles (e.g., `quantile_0.01`, `quantile_0.5`, `quantile_0.975`).
    *   **Crucial Constraint:** The predicted quantiles for any given row must be **monotonically increasing**.

**2. Dataset Description**

The following data objects are available for you to use:

*   **Primary Training Data:**
    *   `train_x`: A DataFrame containing historical feature data.
    *   `train_y`: A Series containing the historical target values (`Total Influenza Admissions`).
*   **Historical Augmentation Data:**
    *   `ilinet_hhs`, `ilinet`, `ilinet_state`: DataFrames containing ~20 years of historical Influenza-Like Illness (ILI) data, available only for dates before `2022-10-15`.
*   **Reference & Example Data:**
    *   `locations`: A DataFrame with geographic and population data.
    *   `sample_submission_df`: A DataFrame showing the correct final output format.
    *   `example_train_x`, `example_train_y`, `example_test_x`: Small example DataFrames demonstrating the structure of the data passed into your function.
    *   `example_reference_date`: A sample forecast date (`2025-01-18`) for context.

**Feature and Column Definitions:**
*   `target_end_date`: The Saturday of the epiweek for which data is reported.
*   `location_name`: The full name of the US state or territory.
*   `location`: The numeric FIPS code for the location.
*   `population`: The total population of the location.
*   `Total Influenza Admissions`: **The target variable.** This data is only available from late 2020 onwards.

**3. Augmenting Training Data with Historical ILINet Data**
The core challenge is the limited history of the target variable. To overcome this, you are provided with ~20 seasons of historical ILINet data. While not the same target, it is highly correlated and captures the essential seasonal dynamics of influenza. The key is to find a way to make this historical data useful for predicting the modern target.
You may explore one of the following strategies, a combination of the two, or come up with a new strategy to incorporate the historical data.

**Strategy 1: Standardize and Combine**
1.  Apply a standardization method to both datasets independently to make the "shape" of the seasons comparable.
2.  Treat the standardized historical ILINet data as additional, independent flu seasons and append them to your training data.
3.  Train your model on this combined "library" of seasons.

**Strategy 2: Learn a Transformation**
1.  Identify the date range where both the target and the historical ILINet data overlap.
2.  Use this period to learn a statistical transformation that maps the ILINet data onto the same scale as the `Total Influenza Admissions` data.
3.  Apply this transformation to the entire 20-year history of ILINet data to create a "synthetic" history for your target variable.
4.  Train your model on this new, augmented training set.

**4. Key Considerations**

*   **Time Series Awareness:** Use your expertise in handling seasonality, trends, and lags.
*   **Calibration:** Ensure your predicted quantiles are well-calibrated.
*   **Logging:** Configure any model you train to be as quiet as possible (e.g., set `verbose=0`). Do not suppress critical Python warnings or error tracebacks.

**5. Detailed Instructions:**
*   An expert has instructed you to implement the below method for this forecasting task. You may make minor improvements to this method, but the original core principles of the method **MUST** be maintained.

An SIR model with unknown case ascertainment, basic reproduction number, population immunity and a splined effective reproduction number is used to model seasonal influenza dynamics in a given season. Across-season trends ('hyperparameters') in the SIR model's parameters are derived by wrapping it in an across-season Bayesian hierarchical model. Hyperparameters are used as priors when forecasting the current season. Disease model integrated in C++ and bound to Python with pybind11, Bayesian hierarchical posterior probability coded in raw Python and sampled using the ensemble sampler of Goodman and Weare available in `emcee` (motivation: computationally inefficient but amazingly robust).

**Before you write your code,** add a comment block at the top of the cell and explicitly list the 3-4 core principles of the method described. Then, write your implementation, ensuring it strictly adheres to these principles.\n