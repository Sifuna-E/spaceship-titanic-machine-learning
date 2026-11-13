# Additional Model Experiment: HistGradientBoosting

## 1. Model Selection

The machine-learning method HistGradientBoostingClassifier was chosen to be compared in order to get an insight into how it performs against the current models. It can recognize patterns and relationships in structured data using gradient boosting and histogram-based learning.

In this experiment, we had the opportunity to explore the possibility of using another tree-based boosting algorithm to enhance the prediction of the transportation of passengers.

## 2. Feature Engineering

Two more features were developed:

TotalSpend: It is the total amount spent by the passenger for the RoomService, FoodCourt, ShoppingMall, Spa and VRDeck. This feature is the total amount spent on board by the passenger.
- **GroupSize**: The number of passengers who are in the same passenger group identifier. This is a feature that can be used to determine if traveling with a group is related to the transportation outcome.

The features were added to explore if they would add extra predictive information to help explain the passengers' spending behaviour and group membership.

## 3. Missing Value Treatment

Missing numerical values were imputed using median imputation and missing categorical values were imputed using most frequent value imputation.

The imputation steps were integrated in the preprocessing pipeline to learn the imputation values from the training set and not from the validation set. This helps minimize data leak.

## 4. Categorical Encoding

One-Hot Encoding was performed for categorical variables. This transforms categories to numerical indicator columns which can be used to process by machine-learning model.

The encoder was configured to ignore categories that it did not see during them training to be able to handle categories that might be seen during the validation or test data sets but not during the training.

## 5. Validation Results

The following results were obtained for validation of the HistGradientBoosting model:

| Metric | Score |
|---|---:|
| Accuracy | 0.7999 |
| Precision | 0.7839 |
| Recall | 0.8322 |
| F1-score | 0.8073 |

The model successfully predicted about 80% of the validation data.

It had a recall of 0.8322, meaning that a decent amount of passengers that belonged to the positive class were correctly recalled.

## 6. Comparing with Random Forest.

The previous model with Random Forest had an accuracy of 0.8045 on validation data and the previous model with HistGradientBoosting had an accuracy of 0.7999 on validation data.

HistGradientBoosting thus achieved 0.0046 less in accuracy, which is 0.46 percentage points less.

Based on accuracy, Random Forest performed slightly better. An alternative model which proved to be useful was HistGradientBoosting with an F1-score of 0.8073, however.

## 7. Error Analysis

The model made 348 false predictions of 1739 passengers in the validation.

The following errors were made:

- 201 false positives.
- 147 false negatives.

The model thus made more errors of false positive than false negative.

These were examples of misclassified passengers found during the inspection, with instances of various home planets, destinations, ages, spending habits, CryoSleep status and group sizes. A certain number of passengers who had no spending recorded and who chose to use CryoSleep were mispredicted to be transported.

The observations indicate that there may be interactions between passenger characteristics which the model may not correctly account for.

## 8. Lessons Learnt

In this experiment, they were able to prove that:

2. There are several different machine-learning algorithms which can generate varying predictions from the same data set.
2. Feature engineering gives the model other information it might be useful for it to find patterns.
An effective machine learning pipeline involves dealing with missing values and encoding categorical data.
4. A more complex model may not necessarily outperform a simpler or previously-tested model.
5. Error analysis is used to determine the misclassified passengers for which the model makes wrong predictions.

The overall accuracy of the model on the validation set was 79.99% using HistGradientBoosting. This was a bit less than the previously recorded accuracy of the Random Forest, but the exercise was helpful in gaining context for model comparisons, feature engineering and model errors.

## 9. Limitations

A hold-out validation dataset was used for the experiment. Results can vary with the split of data for validation and with the model parameters. Further tuning and cross validation could be considered to see if improved performance is possible.
