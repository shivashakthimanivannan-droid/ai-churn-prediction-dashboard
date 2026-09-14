import os
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

engine = create_engine("mysql+mysqlconnector://root:Shiva%402003@localhost/telco_churn")

# Join predictions with original features, keep only High risk customers
query = """
SELECT c.customerID, c.tenure, c.Contract, c.MonthlyCharges, c.TotalCharges_clean,
       c.InternetService, c.TechSupport, c.PaymentMethod,
       p.churn_probability, p.risk_tier
FROM customers c
JOIN churn_predictions p ON c.customerID = p.customerID
WHERE p.risk_tier = 'High';
"""
high_risk = pd.read_sql(query, engine)
print("High risk customers to explain:", high_risk.shape[0])
print(high_risk.head())


import json

def get_explanations_batch(batch_df):
    customer_list = []
    for _, row in batch_df.iterrows():
        customer_list.append({
            "customerID": row["customerID"],
            "tenure": int(row["tenure"]),
            "contract": row["Contract"],
            "monthly_charges": float(row["MonthlyCharges"]),
            "internet_service": row["InternetService"],
            "tech_support": row["TechSupport"],
            "payment_method": row["PaymentMethod"],
            "churn_probability": round(float(row["churn_probability"]), 2)
        })

    prompt = f"""
You are a churn analyst. For each customer below, write:
1. A 1-2 sentence plain-English reason they are at risk of churning
2. One specific, concrete retention action

Return ONLY a JSON array, one object per customer, with keys: customerID, reason, retention_action.
No markdown, no extra text.

Customers:
{json.dumps(customer_list, indent=2)}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    raw = response.choices[0].message.content
    raw = raw.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(raw)

# Test on just the first 5 customers before running all 1,666
test_batch = high_risk.head(5)
explanations = get_explanations_batch(test_batch)

for exp in explanations:
    print(exp["customerID"], "-", exp["reason"], "->", exp["retention_action"])


import time

all_explanations = []
batch_size = 10

for i in range(0, len(high_risk), batch_size):
    batch = high_risk.iloc[i:i+batch_size]
    try:
        batch_explanations = get_explanations_batch(batch)
        all_explanations.extend(batch_explanations)
        print(f"Processed {i+len(batch)} / {len(high_risk)}")
    except Exception as e:
        print(f"Batch {i} failed: {e}")
    time.sleep(1)  # small pause to stay within free-tier rate limits

# Save all explanations to a dataframe
explanations_df = pd.DataFrame(all_explanations)
print(explanations_df.shape)
print(explanations_df.head())

# Merge with churn_probability and risk_tier, write to MySQL
final = high_risk[["customerID", "churn_probability", "risk_tier"]].merge(
    explanations_df, on="customerID", how="left"
)
final.to_sql("churn_explanations", con=engine, if_exists="replace", index=False)
print("Saved churn_explanations table to MySQL.")