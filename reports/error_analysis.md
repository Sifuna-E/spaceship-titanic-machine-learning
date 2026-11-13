Model Validation: Error Analysis.

## 1. Introduction

In this analysis we look at the classification errors made by the HistGradientBoosting model when validated onto the Spaceship Titanic dataset.

The goal is to gain an understanding of the kind of errors that were produced by the model, to understand the properties of the misclassified users, and to determine how to improve the predictive performance of the model.

Analysis is performed based on the predictions from the 20% of the data used for validation.

## 2. Overall Model Performance

This confusion matrix was created with 1,739 validation observations.

The model correctly classified 1391 passengers, and incorrectly classified 348 passengers.

The accuracy of the validation set was around 79.99%.

| Performance measure | Value |
|---|---:|
| Total validation passengers | 1,739 |
| Correct predictions | 1,391 |
| Incorrect predictions | 348 |
| Validation accuracy | 79.99% |
| Validation error rate | 20.01% |

## 3. Confusion Matrix

The confusion matrix gave the following outcomes:

Actual / Predicted | Not Transported | Transported |
|---|---:|---:|
| Not Transported | 662 | 201 |
| Transported | 147 | 729 |

The model correctly classified 662 passengers who were not conveyed, and 729 passengers who were conveyed.

But wrongly counted 201 passengers as transported when they were not. Those are predictions that are incorrect.

It also falsely calculated 147 transported passengers as "not transported". These are "no" predictions.

**Figure 1: Confusion Matrix**

The visualisation of the confusion matrix is saved in `reports/figures/confusion_matrix.png`.

## 4. Analysis of Classification Errors

A total of 348 passengers were misclassified.

Type of error | Number of errors | Percentage of errors |
|---|---:|---:|
| False Positive | 201 | 57.76% |
| False Negative | 147 | 42.24% |
| Total | 348 | 100% |

The percentage of false positives is around 57.76% and false negatives are around 42.24% of all classification errors.

This suggests that when the passenger was not transported, the model was more likely to predict transportation.

For the transported passengers, the precision of the model was about 78.39% and the recall was about 83.22%.

This indicates that the model has a relatively high rate of passengers who were transported, but some predictions it makes were correct in being positive.

## 5. Once the shipments are identified as misclassified, review of those characteristics.

Patterns were explored by checking a sample of 20 passenger records for misclassification.

Several observations emerged:

- A number of false-positive cases were when passengers were from Earth and had taken the CryoSleep option with no spending registered in any of the expenditure categories.
- A few false-negatives were due to passengers having CryoSleep turned off and positive spending.
There were also some missing records in the misclassified data sets, such as CryoSleep, VIP and spending variables.
Misclassifications were present in each HomePlanet/Destination combination.
The number of passengers in the cases studied ranged.

The observations indicate it is not only passengers that make classification errors.

The 20 records shown are, however, just a portion of the 348 errors. Therefore, one needs to interpret these patterns as more of a preliminary observation, rather than statistically proven correlations.

It would be necessary to do further investigations on all misclassified records to see if specific characteristics for passengers are related to an increased likelihood of misclassification.

## 6. Examples of possible reasons for misclassification.

The observed classification errors might be due to a number of reasons:

The passenger characteristics of the transported and non-transported are not unique, making it hard to differentiate between them.

Missing data in passenger data could hinder the predictive information that is given to the model.

4. **Complex relationships:** The relationship between passenger characteristics and transportation could have interactions that are not fully represented in the model.

There are some restrictions on the features available and they might not provide enough information to accurately differentiate some passengers.

Passenger group effects may also exist where passengers travelling in groups may have similar transportation outcomes and/or group information could be useful for further investigation.

## 7. Suggestions for the improvement in the future

The following are suggested to improve the errors identified from the error analysis:

- Conduct an investigation to determine if there are different rates of misclassification across the HomePlanet, CryoSleep and passenger group categories.
- Discuss how missing data impact prediction errors.
Investigate further feature engineering with additional data on passenger groups and cabin details.
- Make comparisons of the error patterns of various machine-learning models.
- Investigate whether model probability thresholds affect the balance between false positives and false negatives.

All proposed improvement should be validated in the same way to make sure the improvement of performance is real.

## 8. Conclusion

An error analysis is performed to give further insight into the performance of the HistGradientBoosting classification model.

The model performance was about 79.99% valid but 348 passengers were misclassified among 1739 passengers in the validation set.

The model gave more false positives than false negatives, meaning that it more often predicted that passengers would be transported.

Analyzing individual misclassified records uncovered several interesting trends in relation to CryoSleep, expenditure and missing data and passenger attributes.

In general, the analysis shows that evaluating a machine-learning model calls for more than just accuracy. When investigating the errors, it is important to find out if there are any limitations, what it does when it fails and where it could go next.
