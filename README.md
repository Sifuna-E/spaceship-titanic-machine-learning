# Spaceship Titanic — Data Analytics and Machine Learning

**Course project | Kaggle binary-classification competition**  
**Audit/update date:** 12 November 2026

## Project overview

This project predicts whether a passenger was transported to another dimension (`Transported`, Boolean). The competition evaluation metric is **accuracy**.

- Competition: [Kaggle — Spaceship Titanic](https://www.kaggle.com/competitions/spaceship-titanic)
- Training data: 8,693 rows × 14 columns
- Test data: 4,277 rows × 13 columns
- Current best result in the latest reported Colab model comparison: Random Forest validation accuracy **0.8045**
- Kaggle submission: a valid-format 4,277-row `submission.csv` has been generated but **has not been submitted**.

The team reports that the instructor approved this competition despite its “Getting Started” category. Retain the written approval and confirm that it explicitly covers the course-rule exception.

## Team and contributions

| Member | Role (proposed; update with evidence as work is completed) |
|---|---|
| Project lead (team member 1) | Coordination, data audit, EDA integration, feature engineering, documentation and presentation coordination. |
| Adedamola | Independent EDA review, additional feature/model experiments, validation and tuning, error analysis, reproducibility review. |

Do not describe proposed tasks as completed until the work is done. Each member must use their own GitHub account and commit their own contributions.

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── notebooks/
│   └── spaceship_titanic_analysis.ipynb
├── src/
│   └── train_and_submit.py        # earlier standalone prototype; not the source of all latest reported scores
├── reports/
│   ├── data_dictionary.md
│   ├── intermediate_status_report.md
│   ├── model_comparison.csv
│   ├── feature_ablation.csv
│   ├── progress_presentation.pptx
│   └── figures/
│       ├── target_distribution.png
│       ├── numeric_distributions.png
│       ├── categorical_distributions.png
│       └── target_relationships.png
└── submission.csv                 # generated predictions; not submitted
```

## How to run the committed notebook (recommended)

The **Google Colab notebook is the primary, supported execution route**. You do not need to run `src/train_and_submit.py` to reproduce the notebook workflow.

1. Open the committed notebook in Colab using this link: [Open notebook in Google Colab](https://colab.research.google.com/github/Sifuna-E/spaceship-titanic-machine-learning/blob/main/notebooks/spaceship_titanic_analysis.ipynb).
2. Download `train.csv`, `test.csv`, and `sample_submission.csv` from the [Kaggle competition data page](https://www.kaggle.com/competitions/spaceship-titanic/data). Do not commit private credentials or Kaggle API tokens.
3. In Colab, click the folder icon on the left, then Upload, and upload the three CSV files into the runtime's working directory. The notebook expects these exact filenames in its current working directory.
4. Choose **Runtime → Run all**. If Colab asks to install missing packages, run `!pip install -r` only after uploading `requirements.txt`, or install the packages listed below.
5. Review the printed dataset audit, EDA, validation model comparison, and generated `submission.csv`. Colab runtime files are temporary; download outputs you need to retain.

### Dependencies

The notebook uses Python 3, pandas, NumPy, Matplotlib and scikit-learn. Install the listed packages in a fresh environment with:

```bash
pip install -r requirements.txt
```

The earlier `src/train_and_submit.py` is retained as a standalone prototype. Its parameter settings and feature implementation are not guaranteed to reproduce the latest Colab notebook scores. Do not cite that script as the source of the current reported model comparison until it has been reconciled and rerun.

## Data and methods

The training target is nearly balanced: `False` = 4,315 (49.64%) and `True` = 4,378 (50.36%). The data include categorical passenger attributes, age, cabin, five spending variables, and passenger/group identifiers. See [`reports/data_dictionary.md`](reports/data_dictionary.md) for field definitions, train/test missingness, anomaly counts and treatment decisions.

The current multi-model comparison used a stratified 80/20 holdout split (`random_state=42`) and accuracy. The preprocessing workflow uses median imputation and missingness indicators for numeric variables, most-frequent imputation for categorical variables, and one-hot encoding. Preprocessing is fitted on the training partition and applied to the validation partition.

## Latest reported holdout comparison

| Model | Validation accuracy |
|---|---:|
| Random Forest | **0.8045** |
| Tuned Random Forest | 0.8028 |
| Gradient Boosting | 0.7907 |
| Logistic Regression | 0.7901 |
| Majority baseline | 0.5037 |

These are local holdout validation results, **not Kaggle leaderboard scores**. The untuned Random Forest is the current working candidate because tuning did not improve the reported holdout score. See [`reports/model_comparison.csv`](reports/model_comparison.csv).

## Controlled feature ablation (12 November 2026)

A separate controlled ablation compared a fixed Random Forest (250 trees, `min_samples_leaf=2`, `max_features='sqrt'`, `random_state=42`) on the same stratified 80/20 split (`random_state=42`). The core predictor set excludes raw identifiers, passenger name and high-cardinality raw cabin text. The expanded set adds parsed cabin components, passenger group/sequence features, age band, surname count and spending aggregates/indicators. Both feature sets use the same preprocessing and model settings.

| Feature set | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Core predictors | 0.7872 | 0.7875 | 0.7911 | 0.7893 |
| Core + engineered predictors | **0.8056** | 0.8172 | 0.7911 | 0.8039 |

The engineered set improved holdout accuracy by **1.84 percentage points** in this controlled experiment. This is evidence of incremental value for the combined engineered feature block under this split/model, not proof that every engineered feature helps individually. Group-aware validation and feature-by-feature ablations remain planned. Full results are in [`reports/feature_ablation.csv`](reports/feature_ablation.csv).

## EDA figures

The committed figures are stored in [`reports/figures/`](reports/figures/): target distribution, numeric distributions, categorical distributions, and selected feature/target relationships. They are descriptive; associations should not be interpreted as causal effects.

## Work remaining and checkpoint

See [`reports/intermediate_status_report.md`](reports/intermediate_status_report.md) for the dated action plan. Priorities are team contribution evidence, group-aware validation, model reproducibility, feature-level analysis, error analysis and final review before any Kaggle submission.

## Academic integrity and limitations

Cite any external notebooks, papers, tutorials or code used. Do not copy public notebooks blindly. Group/surname frequency features are calculated from train+test passenger metadata without target labels; this target-free transductive step is documented and requires a robustness check. Keep local validation scores separate from leaderboard results. The final Kaggle submission is deliberately pending team review.
