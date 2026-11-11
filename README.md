# Spaceship Titanic: Data Analytics and Machine Learning

**Course project | Kaggle competition | Binary classification**

## 1. Project overview

This team project develops and evaluates machine-learning models to predict whether a passenger was transported to another dimension during the fictional Spaceship Titanic incident. The prediction target is `Transported`, a Boolean outcome (`True` or `False`).

- **Competition:** [Kaggle — Spaceship Titanic](https://www.kaggle.com/competitions/spaceship-titanic)
- **Task:** Binary classification
- **Evaluation metric:** Accuracy, the proportion of predictions that are correct
- **Current status:** Exploratory analysis, preprocessing, baseline and model comparisons, initial hyperparameter search, and a Kaggle-format prediction file have been completed. The prediction file has **not** been submitted to Kaggle.

> **Course approval note:** The team reports that the instructor approved this competition despite its “Getting Started” category. Keep the written approval with the course records and confirm that it covers the course-rule exception.

## 2. Team and responsibilities

| Member | Proposed responsibility |
|---|---|
| Eugine | Coordinate the project; data audit and dictionary; EDA; feature engineering; integration; report and presentation coordination |
| Adedamola | Independent review/reproduction of EDA; alternative feature and model experiments; cross-validation and tuning; error analysis; reproducibility review |

These are proposed responsibilities, not a claim that every task is already complete. The team should confirm the allocation and update this section to reflect actual work. Each member should commit their own contributions using their own GitHub account. Do not share credentials or create commits on behalf of the other member.

## 3. Data

The supplied training dataset contains **8,693 rows and 14 columns**, including the target. The test dataset contains **4,277 rows and 13 columns**. The training target is nearly balanced:

- `Transported = False`: 4,315 (49.64%)
- `Transported = True`: 4,378 (50.36%)

Predictors include passenger/group identifiers, home planet, cryosleep status, cabin, destination, age, VIP status, five onboard spending variables, and passenger name. See [`reports/data_dictionary.md`](reports/data_dictionary.md) for field descriptions and training-set missingness.

The competition data are not included in this repository. Download them from Kaggle and place local copies in a `data/` directory if running the standalone script. Follow the competition's data-use terms.

## 4. Current workflow

1. Inspect dimensions, data types, target distribution, duplicates, and missing values.
2. Explore numeric distributions, categorical frequencies, and relationships with the target.
3. Engineer predictors from passenger IDs, cabin structure, spending, age bands, and surname/group information.
4. Split the labeled data using a stratified 80/20 holdout split (`random_state=42`).
5. Fit preprocessing on the training partition and apply it to the validation partition.
6. Compare a majority-class baseline, logistic regression, random forest, and gradient boosting using accuracy.
7. Conduct a limited randomized search for Random Forest hyperparameters using 3-fold stratified cross-validation within the training partition.
8. Refit the selected working model on all labeled data and generate `submission.csv`.

Preprocessing currently includes median imputation and scaling for numeric predictors, and most-frequent imputation and one-hot encoding for categorical predictors. The fitted preprocessing is kept within the model workflow to avoid fitting imputation/encoding statistics on the holdout partition.

## 5. Latest local validation results

The latest confirmed Colab run reported the following holdout accuracy:

| Model | Validation accuracy |
|---|---:|
| Random Forest | **0.8045** |
| Tuned Random Forest | 0.8028 |
| Gradient Boosting | 0.7907 |
| Logistic Regression | 0.7901 |
| Majority-class baseline | 0.5037 |

The current working candidate is Random Forest at 0.8045. The tuned candidate did not improve the holdout result. These are **local validation results, not Kaggle leaderboard scores**. The submission file has not been uploaded.

## 6. Repository contents

- `notebooks/spaceship_titanic_analysis.ipynb` — Google Colab analysis notebook (primary record of the current run).
- `src/train_and_submit.py` — standalone script; review it against the notebook before treating it as an exact reproduction of the latest run.
- `reports/data_dictionary.md` — variable descriptions and missing-value audit.
- `reports/intermediate_status_report.md` — checkpoint progress report.
- `reports/progress_presentation.pptx` — short checkpoint presentation.
- `submission.csv` — generated prediction file; not yet submitted to Kaggle.

## 7. Work remaining

- Reconcile the standalone script with the current Colab notebook so the documented results can be reproduced exactly.
- Have both team members independently review the data and current modelling pipeline.
- Run robust repeated or 5-fold validation and investigate passenger-group dependence.
- Conduct controlled feature ablation using identical validation folds before claiming feature-engineering gains.
- Review feature importance and validation errors; document limitations.
- Consider one additional model family and compare it on the same validation protocol.
- After team review, submit the agreed final prediction file to Kaggle and record the accepted leaderboard score.
- Confirm actual member responsibilities and ensure each member has genuine, attributable GitHub commits.

## 8. Reproducibility and academic integrity

Use the notebook and script as working project materials, not as a substitute for understanding the analysis. Cite any external notebooks, papers, tutorials, or code that influence the project. Do not copy public notebooks blindly. Record software versions and random seeds, preserve the validation protocol, and distinguish all local validation metrics from competition leaderboard results.
