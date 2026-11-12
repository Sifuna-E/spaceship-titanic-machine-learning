# Intermediate Status Report — Spaceship Titanic

**Report date:** Thursday, 12 November 2026  
**Checkpoint target:** Friday, 13 November 2026  
**Project status:** Substantial initial workflow complete; validation robustness, team contribution evidence and final reproducibility checks remain in progress.  
**Competition:** Kaggle Spaceship Titanic  
**Target / metric:** `Transported` / accuracy

## 1. Objective and approval

The project develops a binary classifier to predict whether a passenger was transported to another dimension. The Kaggle metric is accuracy. The team reports that the instructor approved use of this competition despite its “Getting Started” category. The written approval should be retained and checked against the course restriction before final assessment.

## 2. Data overview and audit

The labeled training data contain 8,693 rows and 14 columns; the unlabeled test data contain 4,277 rows and 13 columns. The target is nearly balanced: 4,315 `False` (49.64%) and 4,378 `True` (50.36%). There are no duplicate training rows or duplicate passenger IDs.

Missingness occurs in 12 training predictors (179–217 missing values per field; maximum 2.50%) and in the corresponding test predictors (80–106 missing values; maximum 2.48%). No target values are missing. The complete train/test missingness audit and variable definitions are in `reports/data_dictionary.md`.

## 3. EDA and anomaly decisions

The EDA includes target distribution, numeric distributions, categorical distributions and selected target relationships. The four figures are committed under `reports/figures/`.

Explicit training-data integrity checks found: 0 duplicate rows; 0 duplicate passenger IDs; 0 malformed passenger IDs; 0 malformed non-missing cabin strings; 0 negative ages; 0 ages above 100; and 0 negative spending cells. There are 3,653 rows with zero total recorded spending and 0 rows with all five spending fields missing. Zero spending is retained as a valid behaviour, not treated as an error.

Tukey's 1.5×IQR rule flags 77 age values above the upper fence and 1,788–1,861 values for each spending variable. These are distributional flags, not confirmed errors. The spending variables are zero-inflated and right-skewed, and the observed maxima are retained. No values have been deleted or winsorised on the basis of IQR alone. The full counts, fences and decisions are in the data dictionary.

## 4. Preprocessing and modelling

The current multi-model notebook pipeline uses median imputation plus numeric missingness indicators, most-frequent categorical imputation, one-hot encoding, and numeric standardisation. Preprocessing is fitted on the training partition and applied to the holdout partition. The latest reported comparison used a stratified 80/20 split with `random_state=42`.

| Model | Holdout validation accuracy |
|---|---:|
| Random Forest | **0.8045** |
| Tuned Random Forest | 0.8028 |
| Gradient Boosting | 0.7907 |
| Logistic Regression | 0.7901 |
| Majority baseline | 0.5037 |

Random Forest is the current working candidate. The tuned Random Forest did not improve the reported holdout accuracy. These values are local validation scores, not Kaggle leaderboard scores. The generated `submission.csv` contains 4,277 predictions and has not been uploaded to Kaggle.

## 5. Controlled feature ablation — completed 12 November 2026

A controlled experiment was run using one fixed stratified 80/20 split (`random_state=42`), the same preprocessing, and the same Random Forest settings (250 trees, `min_samples_leaf=2`, `max_features='sqrt'`, `random_state=42`) for both feature sets.

| Feature set | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Core predictors | 0.7872 | 0.7875 | 0.7911 | 0.7893 |
| Core + engineered predictors | **0.8056** | 0.8172 | 0.7911 | 0.8039 |

The expanded feature block improved accuracy by **0.0184 (1.84 percentage points)** on this holdout. The core set comprises the non-identifier original predictors (HomePlanet, CryoSleep, Destination, Age, VIP and the five spend variables). The expanded set adds cabin deck/number/side, passenger sequence and group size, age band, surname frequency, total/log spending, observed spend-field count and any/no-spend indicators. Raw `PassengerId`, `Name` and raw high-cardinality `Cabin` are not directly used.

Interpretation is deliberately limited: the experiment supports the combined engineered block on this split and model; it does not isolate the contribution of each individual feature and does not establish robustness across folds. Group size and surname frequency are calculated from train+test passenger metadata without target labels (target-free transductive construction). This choice is disclosed and must be checked using group-aware validation.

## 6. Progress against checkpoint expectations

| Requirement | Status at report date | Evidence / next action |
|---|---|---|
| Competition objective, target and metric | Complete | README and notebook |
| Data loading, dimensions, types and target distribution | Complete | Notebook and data dictionary |
| EDA and figures | Initial EDA complete | Four figures committed; expand written interpretation if required |
| Missing-value counts and treatment | Complete for train and test | Data dictionary |
| Anomaly counts and decisions | Complete for specified integrity/IQR checks | Data dictionary |
| Encoding, imputation and scaling | Implemented | Notebook; verify reproducibility |
| Feature engineering and impact | Combined-block ablation complete | `feature_ablation.csv`; feature-by-feature ablation remains |
| Baseline and three model families | Complete | Latest model comparison |
| Hyperparameter tuning | Initial search complete | Tuned RF did not beat working RF; avoid unsupported tuning claims |
| Validation and leakage controls | Partially complete | Stratified holdout; group-aware robustness still required |
| Same-protocol comparison table | Complete for latest reported comparison | `model_comparison.csv` |
| Final model / leaderboard comparison | In progress | RF provisional; Kaggle upload intentionally pending |
| GitHub README and notebook | Complete at current stage | Repository links and committed notebook |
| Both members' contribution evidence | In progress | Adedamola invited; acceptance and substantive commits not yet verified |
| Intermediate report and short progress slides | Prepared | This report and `progress_presentation.pptx` |

## 7. Team roles and contribution evidence

Eugine prepared the initial notebook workflow, data audit, feature-engineering integration and documentation. Adedamola to add independent EDA review, alternative feature/model experiments, cross-validation, error analysis and reproducibility checks. 

Both members should use their own GitHub accounts, make attributable commits, and be prepared to explain their contributions during the defense. All team members are expected to attend and speak during the final defense under the course requirements previously provided to the team.

## 8. Dated remaining-work plan

| Due date | Owner | Deliverable / acceptance evidence |
|---|---|---|
| Thu 12 Nov 2026 | Eugine | Commit updated README, dictionary, status report, model table, ablation table and four EDA figures to their documented paths. |
| Fri 13 Nov 2026 | Both | Each member reviews the notebook and report; make at least one substantive, attributable commit each; document exactly what changed. |
| Fri 13 Nov 2026 | Adedamola | Reproduce the current holdout comparison or document discrepancies, with environment/seed details. |
| Fri 13 Nov 2026 |Eugine | Verify README run instructions, repository paths, report links and presentation; send professor the public repository link and checkpoint summary. |
| Mon 16 Nov 2026 | Adedamola | Run group-aware validation (grouped by PassengerId prefix) and report fold/holdout metrics and limitations. |
| Tue 17 Nov 2026 | Both | Conduct feature-level ablation or permutation-based analysis; retain only defensible features. |
| Wed 18 Nov 2026 | Adedamola | Complete validation error analysis and one additional model-family experiment under a consistent protocol. |
| Thu 19 Nov 2026 | Eugine | Reconcile notebook and standalone script; record package versions, seeds and reproducible run instructions. |
| Fri 20 Nov 2026 | Both | Review final candidate, update comparison/report/slides, then decide jointly whether to upload a Kaggle submission. Record leaderboard result separately if submitted. |


## 9. Limitations and risks

- The headline model comparison is based on one holdout split; cross-validation and group-aware validation are outstanding.
- The controlled ablation uses a fixed model/split and tests the engineered block jointly, not individual feature contributions.
- Group/surname counts use unlabeled train+test metadata; their value and robustness need group-aware evaluation.
- The notebook's latest model results and the older standalone script are not yet fully reconciled; the notebook is the primary execution record.
- Instructor approval for the competition-category exception should be retained in writing.

## 10. Checkpoint conclusion

The project has progressed beyond initial setup: data audit, EDA, missingness treatment, baseline, three model families, initial tuning, a controlled combined-feature ablation, prediction-file generation, repository notebook and checkpoint documentation are available. The work is on a credible path to the intermediate checkpoint, but final checkpoint readiness depends on committing the evidence, confirming Adedamola's participation, and completing the Friday reproducibility review. The final model remains provisional pending group-aware validation and team review.
