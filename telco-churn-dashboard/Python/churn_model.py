import mysql.connector
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shiva@2003",
    database="telco_churn"
)
df = pd.read_sql("SELECT * FROM customers;", conn)
conn.close()

# Drop columns we don't need for modeling
df_model = df.drop(columns=["customerID", "TotalCharges"])
df_model = df_model.rename(columns={"TotalCharges_clean": "TotalCharges"})

# Drop the 11 rows with missing TotalCharges (new customers, 0 tenure)
df_model = df_model.dropna(subset=["TotalCharges"])

# Encode target variable
df_model["Churn"] = df_model["Churn"].map({"Yes": 1, "No": 0})

# One-hot encode remaining categorical columns
categorical_cols = df_model.select_dtypes(include=["object", "str"]).columns.tolist()
df_model = pd.get_dummies(df_model, columns=categorical_cols, drop_first=True)

print(df_model.shape)
print(df_model["Churn"].value_counts())

X = df_model.drop(columns=["Churn"])
y = df_model["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Train shape:", X_train.shape)
print("Test shape:", X_test.shape)

# Scale features (needed for Logistic Regression only)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Baseline: Logistic Regression
log_model = LogisticRegression(max_iter=1000, class_weight="balanced")
log_model.fit(X_train_scaled, y_train)
log_preds = log_model.predict(X_test_scaled)
log_probs = log_model.predict_proba(X_test_scaled)[:, 1]

print("=== Logistic Regression ===")
print(classification_report(y_test, log_preds))
print("ROC-AUC:", roc_auc_score(y_test, log_probs))

# Main model: XGBoost (no scaling needed)
xgb_model = XGBClassifier(
    n_estimators=200, max_depth=4, learning_rate=0.1,
    scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1]),
    eval_metric="logloss", random_state=42
)
xgb_model.fit(X_train, y_train)
xgb_preds = xgb_model.predict(X_test)
xgb_probs = xgb_model.predict_proba(X_test)[:, 1]

print("\n=== XGBoost ===")
print(classification_report(y_test, xgb_preds))
print("ROC-AUC:", roc_auc_score(y_test, xgb_probs))


import numpy as np
from sqlalchemy import create_engine

# Score the FULL dataset
full_probs = xgb_model.predict_proba(X)[:, 1]

results = df.loc[df_model.index, ["customerID"]].copy()
results["churn_probability"] = full_probs

def risk_tier(p):
    if p >= 0.7:
        return "High"
    elif p >= 0.4:
        return "Medium"
    else:
        return "Low"

results["risk_tier"] = results["churn_probability"].apply(risk_tier)

print(results.head())
print(results["risk_tier"].value_counts())

# Connect and write to MySQL
engine = create_engine("mysql+mysqlconnector://root:Shiva%402003@localhost/telco_churn")
results.to_sql("churn_predictions", con=engine, if_exists="replace", index=False)

print("Saved churn_predictions table to MySQL.")