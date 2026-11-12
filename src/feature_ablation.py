"""Reproduce the controlled Spaceship Titanic feature-ablation experiment.

Run from the repository root after installing requirements.txt:
    python src/feature_ablation.py --train data/train.csv --test data/test.csv

This experiment uses the same stratified 80/20 holdout indices and the same
Random Forest settings for both feature sets. Passenger group/surname counts
are target-free aggregates from train+test passenger metadata; this is a
transductive feature construction and should be evaluated with group-aware
validation before final model selection.
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

SPEND = ["RoomService", "FoodCourt", "ShoppingMall", "Spa", "VRDeck"]


def build_engineered_features(frame, group_counts, surname_counts):
    x = frame.copy()
    x["TotalSpend"] = x[SPEND].sum(axis=1, min_count=1)
    x["LogTotalSpend"] = np.log1p(x["TotalSpend"])
    x["SpendObservedCount"] = x[SPEND].notna().sum(axis=1)
    x["AnySpend"] = np.where(x["TotalSpend"].notna(), (x["TotalSpend"] > 0).astype(float), np.nan)
    x["NoSpend"] = np.where(x["TotalSpend"].notna(), (x["TotalSpend"] == 0).astype(float), np.nan)
    parts = x["PassengerId"].str.split("_", expand=True)
    x["PassengerNumber"] = pd.to_numeric(parts[1], errors="coerce")
    x["GroupSize"] = parts[0].map(group_counts)
    cabin = x["Cabin"].fillna("").str.split("/", expand=True)
    x["CabinDeck"] = cabin[0].replace("", np.nan)
    x["CabinNumber"] = pd.to_numeric(cabin[1], errors="coerce")
    x["CabinSide"] = cabin[2].replace("", np.nan)
    x["AgeGroup"] = pd.cut(
        x["Age"], [-np.inf, 12, 18, 30, 50, np.inf],
        labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"]
    ).astype("object")
    last_name = x["Name"].fillna("").str.split().str[-1].replace("", np.nan)
    x["SurnameCount"] = last_name.map(surname_counts)
    return x


def evaluate(x_train, x_valid, y_train, y_valid):
    categorical = x_train.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric = x_train.select_dtypes(exclude=["object", "category"]).columns.tolist()
    prep = ColumnTransformer([
        ("num", SimpleImputer(strategy="median", add_indicator=True), numeric),
        ("cat", Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore"))
        ]), categorical)
    ])
    model = Pipeline([
        ("preprocess", prep),
        ("random_forest", RandomForestClassifier(
            n_estimators=250, min_samples_leaf=2, max_features="sqrt",
            n_jobs=-1, random_state=42
        ))
    ])
    model.fit(x_train, y_train)
    pred = model.predict(x_valid)
    return {
        "accuracy": float(accuracy_score(y_valid, pred)),
        "precision": float(precision_score(y_valid, pred)),
        "recall": float(recall_score(y_valid, pred)),
        "f1": float(f1_score(y_valid, pred)),
        "confusion_matrix": confusion_matrix(y_valid, pred).tolist()
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", default="data/train.csv")
    parser.add_argument("--test", default="data/test.csv")
    parser.add_argument("--output-dir", default="reports")
    args = parser.parse_args()
    train = pd.read_csv(args.train)
    test = pd.read_csv(args.test)
    y = train["Transported"].astype(int)

    # Counts use only unlabeled metadata; target labels are never included.
    combined = pd.concat([train.drop(columns="Transported"), test], ignore_index=True)
    group_counts = combined["PassengerId"].str.split("_").str[0].value_counts()
    surname = combined["Name"].fillna("").str.split().str[-1].replace("", np.nan)
    surname_counts = surname.value_counts()
    engineered = build_engineered_features(train, group_counts, surname_counts)

    core_columns = ["HomePlanet", "CryoSleep", "Destination", "Age", "VIP"] + SPEND
    engineered_columns = core_columns + [
        "TotalSpend", "LogTotalSpend", "SpendObservedCount", "AnySpend", "NoSpend",
        "PassengerNumber", "GroupSize", "CabinDeck", "CabinNumber", "CabinSide",
        "AgeGroup", "SurnameCount"
    ]
    x_core = train[core_columns].copy()
    x_engineered = engineered[engineered_columns].copy()
    core_train, core_valid, y_train, y_valid = train_test_split(
        x_core, y, test_size=0.2, random_state=42, stratify=y
    )
    eng_train, eng_valid, y_train_eng, y_valid_eng = train_test_split(
        x_engineered, y, test_size=0.2, random_state=42, stratify=y
    )
    assert y_train.index.equals(y_train_eng.index) and y_valid.index.equals(y_valid_eng.index)

    results = {
        "Core original predictors": evaluate(core_train, core_valid, y_train, y_valid),
        "Core + engineered predictors": evaluate(eng_train, eng_valid, y_train_eng, y_valid_eng)
    }
    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, metrics in results.items():
        rows.append({"Feature_Set": name, **{k: metrics[k] for k in ["accuracy", "precision", "recall", "f1"]}})
    pd.DataFrame(rows).to_csv(outdir / "feature_ablation.csv", index=False)
    (outdir / "feature_ablation_details.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))
    print(f"Saved ablation results to {outdir.resolve()}")


if __name__ == "__main__":
    main()
