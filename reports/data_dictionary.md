# Data dictionary and data-quality audit

**Audit date:** 12 November 2026  
**Source:** Kaggle Spaceship Titanic competition files (`train.csv`, `test.csv`).

## Dataset overview

| Dataset | Rows | Columns | Target included? |
|---|---:|---:|---|
| Training | 8,693 | 14 | Yes (`Transported`) |
| Test | 4,277 | 13 | No |

## Field definitions

| Field | Data type | Meaning | Modelling notes |
|---|---|---|---|
| `PassengerId` | String identifier | Unique passenger ID formatted group_number; prefix denotes travel group and suffix passenger sequence. | Parse components as candidate features; do not treat raw ID as continuous. |
| `HomePlanet` | Categorical | Planet from which the passenger departed. | Categorical imputation and one-hot encoding. |
| `CryoSleep` | Boolean/categorical | Whether the passenger elected suspended animation. | Categorical imputation; potentially informative predictor. |
| `Cabin` | Structured string | Cabin formatted deck/number/side. | Split into deck, cabin number and side; retain missingness. |
| `Destination` | Categorical | Planet the passenger was scheduled to travel to. | Categorical imputation and one-hot encoding. |
| `Age` | Numeric, years | Passenger age in years. | Median imputation; age bands evaluated as a candidate engineered feature. |
| `VIP` | Boolean/categorical | Whether the passenger paid for VIP service. | Categorical imputation and one-hot encoding. |
| `RoomService` | Numeric amount | Amount billed for room-service amenities. | Highly right-skewed; many zeros; do not remove plausible high values. |
| `FoodCourt` | Numeric amount | Amount billed at the food court. | Highly right-skewed; many zeros; do not remove plausible high values. |
| `ShoppingMall` | Numeric amount | Amount billed at the shopping mall. | Highly right-skewed; many zeros; do not remove plausible high values. |
| `Spa` | Numeric amount | Amount billed at the spa. | Highly right-skewed; many zeros; do not remove plausible high values. |
| `VRDeck` | Numeric amount | Amount billed at the VR deck. | Highly right-skewed; many zeros; do not remove plausible high values. |
| `Name` | Text | Passenger first and last name. | Raw name excluded; surname frequency tested as a derived feature. |
| `Transported` | Boolean target | Whether the passenger was transported to another dimension. | Prediction target; present only in labeled training data. |

## Missing values in both datasets

Counts and percentages are computed independently using each dataset's row count. A dash means the field is not present in that dataset.

| Field | Train missing (n) | Train missing (%) | Test missing (n) | Test missing (%) |
|---|---:|---:|---:|---:|
| `PassengerId` | 0 | 0.00% | 0 | 0.00% |
| `HomePlanet` | 201 | 2.31% | 87 | 2.03% |
| `CryoSleep` | 217 | 2.50% | 93 | 2.17% |
| `Cabin` | 199 | 2.29% | 100 | 2.34% |
| `Destination` | 182 | 2.09% | 92 | 2.15% |
| `Age` | 179 | 2.06% | 91 | 2.13% |
| `VIP` | 203 | 2.34% | 93 | 2.17% |
| `RoomService` | 181 | 2.08% | 82 | 1.92% |
| `FoodCourt` | 183 | 2.11% | 106 | 2.48% |
| `ShoppingMall` | 208 | 2.39% | 98 | 2.29% |
| `Spa` | 183 | 2.11% | 101 | 2.36% |
| `VRDeck` | 188 | 2.16% | 80 | 1.87% |
| `Name` | 200 | 2.30% | 94 | 2.20% |
| `Transported` | 0 | 0.00% | — | — |

Training data have 2324 missing cells across predictors; test data have 1117 missing cells. The target has no missing values. Training missingness ranges from 2.50% (`CryoSleep`) to 2.06% among fields with missing values. Test missingness ranges from 2.48% (`FoodCourt`) to 1.87% among fields with missing values.

## Explicit anomaly and integrity audit (training data)

| Check | Count | Decision |
|---|---:|---|
| Duplicate complete rows | 0 | No duplicate rows removed. |
| Duplicate `PassengerId` values | 0 | IDs are unique; retain ID-derived group/sequence components as candidate features. |
| Invalid `PassengerId` pattern (`dddd_dd`) | 0 | No format correction required. |
| Non-missing `Cabin` values not matching `deck/number/side` | 0 | No malformed cabin values detected. |
| Negative ages | 0 | No impossible negative ages detected. |
| Ages greater than 100 | 0 | No implausibly high ages under this conservative rule. |
| Negative spending cells across five amenities | 0 | No impossible negative spending values detected. |
| Rows with zero total recorded spend | 3,653 | Retain; zero spend is a plausible behavioural value, not an error. |
| Rows with all five spending fields missing | 0 | No row has all five spend fields missing. |

### Tukey IQR flags — interpret as distributional extremes, not confirmed errors

IQR flags use the 1.5 × IQR rule on non-missing training values. Because spending is zero-inflated and strongly right-skewed, these counts are not grounds for deleting or winsorising records.

| Variable | Non-missing n | Min | Max | IQR upper fence | Values above upper fence |
|---|---:|---:|---:|---:|---:|
| Age | 8,514 | 0 | 79 | 66.5 | 77 |
| RoomService | 8,512 | 0 | 14,327 | 117.5 | 1,861 |
| FoodCourt | 8,510 | 0 | 29,813 | 190.0 | 1,823 |
| ShoppingMall | 8,485 | 0 | 23,492 | 67.5 | 1,829 |
| Spa | 8,510 | 0 | 22,408 | 147.5 | 1,788 |
| VRDeck | 8,505 | 0 | 24,133 | 115.0 | 1,809 |

**Decision:** retain these observations. Age extremes (77 records) are plausible within the observed 0–79 range. Spending extremes are plausible high expenditures given the data definition; no independent evidence indicates data-entry errors. Transformations such as `log1p` total spending are evaluated as features rather than altering source values.

## Missing-value treatment in the current pipeline

- Numeric predictors: median imputation, fitted on the training partition only; numeric missingness indicators are added.
- Categorical predictors: most-frequent imputation, followed by one-hot encoding with unseen categories ignored.
- Numeric scaling: standardisation is used in the multi-model comparison pipeline, mainly for logistic regression. Tree models do not require scaling, but the shared pipeline keeps preprocessing consistent.
- Missing values are not filled in the source CSVs; treatment occurs inside the fitted preprocessing pipeline.
- In the ablation experiment, aggregate spend features preserve missing total spend as missing rather than interpreting an all-unknown total as zero.

## Anomaly decisions and limitations

1. No duplicate, malformed-ID, malformed-cabin, negative-age, age-over-100, or negative-spending anomalies were detected under the checks above.
2. IQR outliers are flagged for review but retained; IQR is a univariate heuristic and is especially aggressive for zero-inflated spending data.
3. Zero total spend is retained as a meaningful value. The ablation feature code distinguishes a recorded zero from a missing total.
4. Group size and surname frequency are computed from passenger metadata across train and test without using target labels. This is target-free transductive feature construction and is documented; a group-aware validation check is still required to test robustness to related passengers.
5. Random stratified validation can place members of the same passenger group on both sides of the split. Group-aware validation remains a planned robustness check.

**Source:** Kaggle, [Spaceship Titanic — Data](https://www.kaggle.com/competitions/spaceship-titanic/data).
