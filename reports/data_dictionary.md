# Data dictionary and missing-value audit

## Dataset overview

| Dataset | Rows | Columns | Target included? |
|---|---:|---:|---|
| Training | 8,693 | 14 | Yes (`Transported`) |
| Test | 4,277 | 13 | No |

The training data contain 8,693 labeled passenger records. The test data contain 4,277 records for which predictions are required. The table below documents the training schema. Definitions follow the Kaggle competition data description.

## Field definitions

| Field | Data type | Meaning | Modelling notes |
|---|---|---|---|
| `PassengerId` | Identifier (string) | Unique passenger identifier, formatted as `group_number` (for example, `0001_01`). The prefix identifies a passenger group; the suffix identifies a person within that group. | Parse group and within-group number into candidate predictors; do not treat the raw ID as a continuous quantity. |
| `HomePlanet` | Categorical | Planet from which the passenger departed. | Impute missing category within the training pipeline; one-hot encode. |
| `CryoSleep` | Boolean/categorical | Whether the passenger elected to be placed in suspended animation for the duration of the voyage. | Missing values require imputation; consider its relationship with spending, but do not infer causality. |
| `Cabin` | Structured string | Cabin identifier formatted as `deck/number/side`. | Can be split into `CabinDeck`, `CabinNumber`, and `CabinSide`; preserve missingness information where useful. |
| `Destination` | Categorical | Planet the passenger was scheduled to travel to. | Impute and one-hot encode. |
| `Age` | Numeric | Passenger age in years. | Median imputation; age bands may be tested as engineered features. |
| `VIP` | Boolean/categorical | Whether the passenger paid for special VIP service during the voyage. | Impute as a category; inspect class imbalance. |
| `RoomService` | Numeric | Amount billed for room-service amenities. | Spending variable; values are highly right-skewed and many are zero. |
| `FoodCourt` | Numeric | Amount billed at the food court. | Spending variable; values are highly right-skewed and many are zero. |
| `ShoppingMall` | Numeric | Amount billed at the shopping mall. | Spending variable; values are highly right-skewed and many are zero. |
| `Spa` | Numeric | Amount billed at the spa. | Spending variable; values are highly right-skewed and many are zero. |
| `VRDeck` | Numeric | Amount billed at the VR deck. | Spending variable; values are highly right-skewed and many are zero. |
| `Name` | Text | Passenger's first and last name. | May be parsed for surname/group features; consider privacy and avoid using raw name as a numeric feature. |
| `Transported` | Boolean target | Whether the passenger was transported to another dimension. | Prediction target; present only in the labeled training data. |

## Training-set missingness

Missing counts and percentages below are from the 8,693-row training dataset. Percentages are calculated as missing values divided by 8,693.

| Field | Missing values | Missing (%) |
|---|---:|---:|
| `CryoSleep` | 217 | 2.50% |
| `ShoppingMall` | 208 | 2.39% |
| `VIP` | 203 | 2.34% |
| `HomePlanet` | 201 | 2.31% |
| `Name` | 200 | 2.30% |
| `Cabin` | 199 | 2.29% |
| `VRDeck` | 188 | 2.16% |
| `Spa` | 183 | 2.10% |
| `FoodCourt` | 183 | 2.10% |
| `Destination` | 182 | 2.09% |
| `RoomService` | 181 | 2.08% |
| `Age` | 179 | 2.06% |
| `PassengerId` | 0 | 0.00% |
| `Transported` | 0 | 0.00% |

The largest missingness rate is 2.50% (`CryoSleep`) and the smallest non-zero rate is 2.06% (`Age`). Missingness is modest but occurs across categorical, numeric, and text/structured fields. Missingness in the test set should be audited separately before final training and prediction; the table above must not be presented as test-set missingness.

## Current treatment and rationale

- Numeric predictors: median imputation is used within the preprocessing pipeline. Median is less sensitive than the mean to the strongly right-skewed spending distributions.
- Categorical predictors: most-frequent imputation is used, followed by one-hot encoding with unknown categories ignored.
- Numeric scaling: standardization is included in the numeric pipeline, principally for scale-sensitive models such as logistic regression. Tree-based models generally do not require scaling, but a shared preprocessing workflow is currently used.
- Missingness indicators: numeric imputation currently adds indicators for numeric fields. A separate explicit missing-category strategy for categorical fields can be tested.
- `Name` and `Cabin`: engineered components are extracted where possible; raw text/structured columns are excluded from the current model feature matrix.
- Spending values: high values are not automatically classified as errors. The spending distributions are strongly right-skewed and many observations are zero. Retain plausible values, inspect impossible/negative values explicitly, and use a log-transformed total-spending feature as a candidate.

## Data-quality checks recorded so far

- No duplicate training rows were found.
- No duplicate `PassengerId` values were found in the training data.
- Spending distributions are strongly right-skewed with many zero values.
- Large spending values are not automatically outliers to remove; they may represent genuine high spending.
- The training target is nearly balanced: `False` = 4,315 (49.64%) and `True` = 4,378 (50.36%).

## Important methodological cautions

1. Missingness counts above are for the training data only.
2. Imputation, scaling, and encoding must be fitted on training folds only, then applied to validation folds.
3. Group/surname counts calculated using unlabeled test predictors can be a form of transductive feature construction. Document it clearly and test robustness; never use test target labels (which are unavailable).
4. Passenger records may be related within groups. A random stratified split can place members of the same group in both train and validation partitions. Add a group-aware robustness check before making strong generalization claims.
5. Feature-engineering gains must be tested by an ablation experiment using the same split/folds and model settings. Do not rely on scores from different runs as a controlled comparison.

**Source:** Kaggle, *Spaceship Titanic — Data* (competition data description): https://www.kaggle.com/competitions/spaceship-titanic/data
