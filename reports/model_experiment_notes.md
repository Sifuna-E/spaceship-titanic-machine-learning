
# Additional Model Experiment: HistGradientBoosting

## 1. Model Selection

HistGradientBoostingClassifier was selected as an additional machine-learning approach to compare its performance with the existing models. It uses gradient boosting and histogram-based learning to identify patterns and relationships in structured data.

This experiment allowed us to investigate whether another tree-based boosting algorithm could improve the prediction of passenger transportation.

## 2. Feature Engineering

Two additional features were created:

- **TotalSpend:** The sum of the passenger's spending on RoomService, FoodCourt, ShoppingMall, Spa, and VRDeck. This feature represents the passenger's overall onboard spending.
- **GroupSize:** The number of passengers sharing the same passenger group identifier. This feature may help identify whether travelling in a group is associated with the transportation outcome.

These features were introduced to investigate whether passenger spending behaviour and group membership could provide additional predictive information.

## 3. Missing Value Treatment

Missing numerical values were handled using median imputation, while missing categorical values were handled using most-frequent-value imputation.

The imputation steps were included in the preprocessing pipeline so that imputation values were learned from the training data rather than the validation data. This helps prevent data leakage.

## 4. Categorical Encoding

Categorical variables were transformed using One-Hot Encoding. This converts categories into numerical indicator columns that can be processed by the machine-learning model.

The encoder was configured to ignore previously unseen categories during transformation, improving its ability to handle categories that may appear in validation or test data but were not present during training.

## 5. Validation Results

The HistGradientBoosting model achieved the following validation results:

| Metric | Score |
|---|---:|
| Accuracy | 0.7999 |
| Precision | 0.7839 |
| Recall | 0.8322 |
| F1-score | 0.8073 |

The model achieved approximately 80% accuracy on the validation dataset.

Its recall of 0.8322 indicates that it correctly identified a relatively high proportion of passengers belonging to the positive class.

## 6. Comparison with Random Forest

The Random Forest model previously achieved a validation accuracy of 0.8045, while HistGradientBoosting achieved 0.7999.

HistGradientBoosting therefore performed 0.0046 lower in accuracy, equivalent to a difference of 0.46 percentage points.

Based on accuracy, Random Forest performed slightly better. However, HistGradientBoosting provided a useful alternative model and achieved an F1-score of 0.8073.

## 7. Error Analysis

The model produced 348 incorrect predictions out of 1,739 validation passengers.

The errors consisted of:

- 201 false positives.
- 147 false negatives.

The model therefore produced more false positives than false negatives.

Inspection of misclassified passengers showed examples involving different home planets, destinations, ages, spending patterns, CryoSleep statuses, and group sizes. Some passengers with zero recorded spending and CryoSleep enabled were incorrectly predicted as transported.

These observations suggest that passenger characteristics can interact in ways that are not always captured correctly by the model.

## 8. Lessons Learnt

This experiment demonstrated that:

1. Different machine-learning algorithms can produce different predictive results on the same type of dataset.
2. Feature engineering provides additional information that may help a model identify patterns.
3. Missing-value treatment and categorical encoding are important parts of a reliable machine-learning pipeline.
4. A more complex model does not necessarily outperform a simpler or previously tested model.
5. Error analysis helps identify the types of passengers for whom the model makes incorrect predictions.

Overall, HistGradientBoosting achieved a validation accuracy of 79.99%. Although this was slightly below the previously recorded Random Forest accuracy, the experiment provided useful insights into model comparison, feature engineering, and prediction errors.

## 9. Limitations

The experiment used a holdout validation dataset. The results may vary depending on the validation split and model parameters. Further tuning and cross-validation could be explored to assess whether performance can be improved.
