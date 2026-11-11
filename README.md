# spaceship-titanic-machine-learning
Spaceship Titanic — Data Analytics & Machine Learning Project
Competition and task
Kaggle: Spaceship Titanic

Predict Transported (whether a passenger was transported to an alternate dimension) from passenger and travel records. This is binary classification. Kaggle evaluates accuracy: the proportion of test passengers whose class is predicted correctly. Accuracy rewards correct classifications equally for both classes.
Course-rule check: Kaggle currently categorizes this as a “Getting Started Prediction Competition.” The course brief advises avoiding competitions with this tag. The professor has approved this topic according to the team; retain written confirmation that this approval is an explicit exception.

Team
- Eugine — data audit, exploratory analysis, feature engineering, model evaluation, final integration and presentation lead.
- Adedamola — independent EDA/feature hypotheses, model experimentation and tuning, error analysis, reproducibility review, and presentation of their own section.
Both members must make meaningful commits under their own GitHub accounts. Do not share credentials or make commits on behalf of one another.
Data
- train.csv: 8,693 rows × 14 columns, including target.
- test.csv: 4,277 rows × 13 columns.
- Target distribution: False = 4,315 (49.6%); True = 4,378 (50.4%).
- Predictor groups: identifiers (PassengerId), categorical (HomePlanet, CryoSleep, Cabin, Destination, VIP), numeric (Age, five amenity spending fields), and name (Name).
Feature meanings are documented on the official Kaggle data page.
Method
1. Stratified 80/20 holdout split (random_state=42).
2. Fit imputers, scaling and one-hot encoding on training fold only; apply fitted transformations to validation fold.
3. Baseline: most-frequent class.
4. Compare logistic regression, random forest and gradient boosting using the same validation split and accuracy.
5. Feature engineering: passenger group size, passenger number, cabin deck/number/side, total spend, any/no-spend flags, log total spend, age bands and surname group count.
6. Tune random-forest hyperparameters with 3-fold stratified cross-validation (recorded in the progress report). The tuned candidate did not improve the selected holdout score, so the simpler RF configuration is retained pending further validation.
7. Refit selected RF on all labeled training rows and generate submission.csv.
Current results
See reports/model_comparison.csv and reports/intermediate_report.md. Validation accuracy is a local estimate; Kaggle leaderboard score must be recorded after uploading submission.csv.
Run locally
pip install -r requirements.txt
python src/train_and_submit.py --train data/train.csv --test data/test.csv --output submission.csv
Place the three Kaggle CSV files in data/. The current generated submission.csv was produced from the supplied data.
Repository layout
- src/train_and_submit.py — reproducible preprocessing, validation, model comparison, tuning and submission generation.
- reports/figures/ — EDA plots.
- reports/model_comparison.csv — validation comparison.
- reports/intermediate_report.md — checkpoint narrative and next steps.
- submission.csv — generated Kaggle-format predictions.
Academic integrity
Use this repository as your team's own implementation. Cite any external notebooks, papers or code you consult. Do not copy public notebooks blindly. Keep a clear commit history showing each member's actual contribution.
