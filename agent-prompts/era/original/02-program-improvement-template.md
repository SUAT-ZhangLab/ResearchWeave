
{problem.description}

Here is a preview of the training data:
{data_preview}

The goal is to predict 'MedHouseVal'. The metric is RMSE (Root Mean Squared Error).
Lower is better.

The previous solution had a score (RMSE) of: {rmse:.5f}
Previous Solution Code:
```python
{parent_solution.program}
```

Please generate a NEW, IMPROVED Python function named `train_and_predict` that:
1. Accepts `train_path` and `test_path` as strings.
2. Trains a regression model.
3. Returns the predictions for the test set as a numpy array or list.
4. You can use pandas, numpy, scikit-learn.

IMPORTANT: DO NOT use `xgboost` or `lightgbm`.

Your code must look like this:
```python
import pandas as pd
import numpy as np
# ... other imports

def train_and_predict(train_path, test_path):
    # Load data
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    
    # ... Feature Engineering ...
    # ... Training ...
    
    # Predict
    predictions = ... 
    return predictions
```
Provide the full, runnable code including imports.

IMPORTANT CONSTRAINTS FOR SPEED:
1. DO NOT use GridSearchCV or RandomizedSearchCV.
2. If using RandomForest or Boosting, set `n_estimators` to maximum 50.
3. Keep the model lightweight (execution time limit is 60 seconds).
