# Intermediate Status Report — Spaceship Titanic

**Project status:** Initial modelling pipeline completed; validation and documentation improvements in progress.  
**Competition:** Kaggle Spaceship Titanic  
**Prediction target:** `Transported`  
**Evaluation metric:** Accuracy  
**Team:** Eugine and Adedamola

## 1. Project objective

The project develops a binary classification model to predict whether each passenger was transported to another dimension. The Kaggle competition evaluates predictions using accuracy, the proportion of passenger outcomes predicted correctly.

The competition is listed in Kaggle's “Getting Started” category. The team reports that the instructor approved the topic; written confirmation of the exception should be retained with the project records.

## 2. Dataset and initial audit

| Dataset | Rows | Columns |
|---|---:|---:|
| Labeled training data | 8,693 | 14 |
| Unlabeled test data | 4,277 | 13 |

The training target is nearly balanced: 4,315 passengers (49.64%) are labeled `False` and 4,378 (50.36%) are labeled `True`. No duplicate training rows or duplicate training `PassengerId` values were found.

The predictors include passenger identifiers, home planet, cryosleep status, cabin, destination, age, VIP status, five amenity-spending variables, and name. A full field-level description and training missingness table are provided in `data_dictionary.md`.

## 3. Exploratory data analysis

The initial EDA examined target balance, missingness, numeric distributions, categorical frequencies, and selected relationships with `Transported`.

Key observations:
- The target is nearly balanced, making the majority-class baseline approximately 50%.
- Spending variables contain many zeros and are strongly right-skewed.
- Age is concentrated among younger and middle-aged passengers, with a tail toward older ages.
- Initial plots suggest differences in transport rates across categories such as `CryoSleep`, `HomePlanet`, and cabin deck. These are descriptive associations, not evidence of causation.
- Large spending values have not been automatically removed as errors; their plausibility needs to be assessed rather than treating every extreme value as invalid.

## 4. Missing values and treatment

Missing values occur in 12 predictor fields. Counts in the 8,693-row training dataset range from 179 (`Age`, 2.06%) to 217 (`CryoSleep`, 2.50%). No missing values were recorded for `PassengerId` or `Transported`.

Current preprocessing:
- Numeric fields: median imputation, with numeric missingness indicators.
- Categorical fields: most-frequent imputation.
- Categorical encoding: one-hot encoding with unknown categories ignored.
- Numeric scaling: standardization in the numeric preprocessing pipeline.

The preprocessing is fitted on the training partition and then applied to validation data. This reduces the risk of preprocessing leakage. The team should additionally inspect test-set missingness and assess whether explicit categorical missingness indicators improve performance.

## 5. Feature engineering

The current workflow constructs candidate features including:
- Passenger group size and passenger number from `PassengerId`.
- Cabin deck, cabin number, and cabin side from `Cabin`.
- Total spending, log total spending, any-spend and no-spend indicators.
- Age bands.
- Surname frequency/count.

These features are plausible representations of group structure, cabin location, spending behaviour, and age categories. Their incremental value must be established through a controlled ablation using identical validation splits/folds and model settings. The team is **not** treating results from different notebook runs as a definitive feature-engineering gain.

## 6. Validation design and current model results

The current reported model comparison uses a stratified 80/20 train/validation split with `random_state=42`. Accuracy is calculated on the held-out validation partition. Preprocessing is fitted on the training partition only.

| Model | Latest validation accuracy |
|---|---:|
| Random Forest | **0.8045** |
| Tuned Random Forest | 0.8028 |
| Gradient Boosting | 0.7907 |
| Logistic Regression | 0.7901 |
| Majority-class baseline | 0.5037 |

The current working candidate is Random Forest (0.8045). The tuned Random Forest (0.8028) did not improve the current holdout result, so additional tuning is not automatically justified. The team will prioritize robust validation and reproducibility over tuning for its own sake.

**Metric qualification:** These values are local validation accuracies. They are not Kaggle leaderboard scores. The `submission.csv` file has been generated and contains 4,277 predictions with the required `PassengerId` and `Transported` columns, but it has **not** been uploaded to Kaggle.

## 7. Work completed to date

- Loaded the training, test, and sample-submission datasets in Google Colab.
- Inspected dataset dimensions, column types, target distribution, missingness, and duplicates.
- Produced initial EDA plots and examined key feature/target relationships.
- Implemented numeric and categorical preprocessing.
- Engineered candidate passenger-group, cabin, spending, and age features.
- Established a majority-class baseline.
- Compared three model families: logistic regression, random forest, and gradient boosting.
- Ran an initial randomized hyperparameter search for Random Forest.
- Generated a Kaggle-format prediction file and checked that it contains 4,277 predictions.
- Saved the Colab notebook to the project GitHub repository.
- Invited Adedamola to collaborate; acceptance and substantive contributions are still to be confirmed.

## 8. Remaining work and immediate plan

1. **Team onboarding:** Confirm Adedamola accepts the GitHub invitation, reviews the notebook, and agrees to documented task ownership.
2. **Reproducibility:** Reconcile the standalone script with the current Colab notebook; verify that documented model results can be reproduced.
3. **Robust validation:** Run repeated or 5-fold stratified cross-validation and report mean and variability. Investigate group-aware validation because passengers sharing a group may not be independent.
4. **Feature ablation:** Compare raw and engineered feature sets under identical folds and model settings.
5. **Model analysis:** Inspect feature importance and validation errors; consider one additional model family under the same validation protocol.
6. **Submission:** After team review and model selection, submit the agreed file to Kaggle and record the accepted leaderboard score separately from local validation.
7. **Communication:** Complete the README, data dictionary, and progress presentation; ensure both team members make genuine commits and speak during the final defense.

## 9. Team responsibilities

The following is a proposed division and must be updated to reflect actual work completed:
- **Project lead (team member 1):** coordination, data audit, data dictionary, EDA integration, feature engineering, README/report integration, and presentation coordination.
- **Adedamola:** independent EDA review, alternative feature/model experiments, cross-validation and tuning, error analysis, reproducibility checks, and presentation of the modelling/validation section.

Both members should use their own GitHub accounts and commit only work they actually performed. The project should not claim completed contributions before the corresponding work and commits exist.

## 10. Current limitations

- The current reported comparison is based on one holdout split; robustness across folds has not yet been established.
- The tuned model's holdout accuracy is slightly lower than the untuned Random Forest result.
- Group/surname frequency features require transparent documentation and robustness checks.
- The standalone script and current Colab notebook need to be reconciled before claiming full reproducibility.
- No Kaggle leaderboard score is available because the submission has not been uploaded.

## 11. Checkpoint conclusion

The team has completed a substantial initial workflow: data audit, exploratory analysis, preprocessing, baseline modelling, comparison of three model families, initial hyperparameter search, and generation of a valid-format prediction file. The next phase focuses on reproducibility, validation robustness, controlled feature evaluation, and documented collaboration. The project is progressing, but the model should remain provisional until those checks are completed.
