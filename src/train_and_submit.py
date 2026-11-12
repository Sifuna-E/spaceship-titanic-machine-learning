import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score

def build_features(df, group_counts, surname_counts):
    x = df.copy()
    parts = x["PassengerId"].str.split("_", expand=True)
    x["PassengerNumber"] = pd.to_numeric(parts[1], errors="coerce")
    x["GroupSize"] = parts[0].map(group_counts)
    cabin = x["Cabin"].fillna("").str.split("/", expand=True)
    x["CabinDeck"] = cabin[0].replace("", np.nan)
    x["CabinNumber"] = pd.to_numeric(cabin[1], errors="coerce")
    x["CabinSide"] = cabin[2].replace("", np.nan)
    spend = ["RoomService","FoodCourt","ShoppingMall","Spa","VRDeck"]
    x["TotalSpend"] = x[spend].sum(axis=1, min_count=1).fillna(0)
    x["AnySpend"] = (x["TotalSpend"] > 0).astype(int)
    x["NoSpend"] = (x["TotalSpend"] == 0).astype(int)
    x["LogTotalSpend"] = np.log1p(x["TotalSpend"])
    x["AgeGroup"] = pd.cut(x["Age"], [-np.inf,12,18,30,50,np.inf],
        labels=["Child","Teen","YoungAdult","Adult","Senior"]).astype("object")
    surname = x["Name"].fillna("").str.split().str[-1].replace("", np.nan)
    x["SurnameCount"] = surname.map(surname_counts)
    return x.drop(columns=["PassengerId","Cabin","Name","Transported"], errors="ignore")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/train.csv")
    ap.add_argument("--test", default="data/test.csv")
    ap.add_argument("--output", default="submission.csv")
    args = ap.parse_args()
    train, test = pd.read_csv(args.train), pd.read_csv(args.test)
    combined = pd.concat([train.drop(columns="Transported"), test], ignore_index=True)
    group_counts = combined["PassengerId"].str.split("_").str[0].value_counts()
    surname_counts = combined["Name"].fillna("").str.split().str[-1].replace("",np.nan).value_counts()
    X = build_features(train, group_counts, surname_counts)
    X_test = build_features(test, group_counts, surname_counts)
    y = train["Transported"].astype(int)
    cats = X.select_dtypes(include=["object","category"]).columns.tolist()
    nums = X.select_dtypes(exclude=["object","category"]).columns.tolist()
    prep = ColumnTransformer([
        ("num", Pipeline([("imputer",SimpleImputer(strategy="median",add_indicator=True)),
                          ("scale",StandardScaler())]), nums),
        ("cat", Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),
                          ("onehot",OneHotEncoder(handle_unknown="ignore"))]), cats)
    ])
    Xa, Xv, ya, yv = train_test_split(X,y,test_size=.2,random_state=42,stratify=y)
    Z_a, Z_v = prep.fit_transform(Xa), prep.transform(Xv)
    models = {
        "Majority baseline": DummyClassifier(strategy="most_frequent"),
        "Logistic regression": LogisticRegression(max_iter=2000,C=1.0),
        "Random forest": RandomForestClassifier(n_estimators=250,min_samples_leaf=2,
            max_features="sqrt",n_jobs=-1,random_state=42),
        "Gradient boosting": GradientBoostingClassifier(n_estimators=100,learning_rate=.05,
            max_depth=2,min_samples_leaf=10,random_state=42)
    }
    for name, model in models.items():
        a = Z_a.toarray() if name == "Gradient boosting" and hasattr(Z_a,"toarray") else Z_a
        v = Z_v.toarray() if name == "Gradient boosting" and hasattr(Z_v,"toarray") else Z_v
        model.fit(a,ya)
        print(f"{name}: {accuracy_score(yv,model.predict(v)):.4f}")
    # Tune RF using training partition only; retain holdout score for transparent model selection.
    search = RandomizedSearchCV(
        RandomForestClassifier(n_jobs=-1,random_state=42),
        {"n_estimators":[200,300,400],"max_depth":[None,10,16,22],
         "min_samples_leaf":[1,2,3,4],"max_features":["sqrt",.8]},
        n_iter=6,scoring="accuracy",
        cv=StratifiedKFold(3,shuffle=True,random_state=42),
        random_state=42,n_jobs=1
    )
    search.fit(Z_a,ya)
    print("Tuned RF best CV accuracy:", round(search.best_score_,4))
    print("Tuned RF params:",search.best_params_)
    # Refit selected, simpler RF on all labeled data and predict test.
    final_prep = ColumnTransformer([
        ("num", Pipeline([("imputer",SimpleImputer(strategy="median",add_indicator=True)),
                          ("scale",StandardScaler())]), nums),
        ("cat", Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),
                          ("onehot",OneHotEncoder(handle_unknown="ignore"))]), cats)
    ])
    Z_all = final_prep.fit_transform(X)
    Z_test = final_prep.transform(X_test)
    final = RandomForestClassifier(n_estimators=250,min_samples_leaf=2,
        max_features="sqrt",n_jobs=-1,random_state=42).fit(Z_all,y)
    pred = final.predict(Z_test).astype(bool)
    pd.DataFrame({"PassengerId":test["PassengerId"],"Transported":pred}).to_csv(args.output,index=False)
    print("Wrote",args.output,"with",len(pred),"predictions")
if __name__ == "__main__":
    main()
