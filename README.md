# ai-churn-prediction-dashboard

# AI-Augmented Customer Churn Prediction Dashboard

An end-to-end churn analytics project combining SQL, Python (ML), and Power BI with a GPT-based explainability layer — built to identify at-risk customers, quantify revenue exposure, and generate automated, plain-English retention recommendations.

## 🎯 Problem
Predict which telecom customers are likely to churn, quantify the revenue impact, and give retention teams clear, actionable reasons — not just a risk score — for each high-risk customer.

## 🧱 Architecture
MySQL (data storage & cleaning)
→ Python EDA (Pandas, Seaborn/Matplotlib)
→ Feature Engineering + ML (Logistic Regression, XGBoost)
→ Risk Scoring (all 7,032 customers)
→ GPT-oss-20b via Groq (explainability layer for high-risk customers)
→ Power BI Dashboard (3-page interactive report)
