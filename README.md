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


## 📊 Dataset
[IBM Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) — 7,043 customers, 21 features (contract type, tenure, monthly charges, services, churn status).

## 🔑 Key Findings
| Finding | Detail |
|---|---|
| Contract type | Month-to-month customers churn at **42.71%** vs. **2.83%** for two-year contracts (~15x) |
| Tenure | First-year customers churn at **47.44%**, dropping to **9.51%** after 4+ years |
| Revenue impact | **$2.86M (17.83%)** of total revenue is tied to churned customers |

## 🤖 Model Performance
| Model | ROC-AUC | Recall (Churn) | Precision (Churn) |
|---|---|---|---|
| Logistic Regression | 0.835 | 0.80 | 0.49 |
| XGBoost | 0.828 | 0.78 | 0.51 |

Class imbalance handled via `class_weight="balanced"` (Logistic Regression) and `scale_pos_weight` (XGBoost). Recall was prioritized over precision, since missing an actual churner is costlier than a false alarm in a retention context.

## 🧠 AI Explainability Layer
Every high-risk customer (churn probability ≥ 0.7) gets a GPT-generated explanation and a specific retention action, e.g.:

> *"This customer has only been with the company for one month and is on a month-to-month plan with no tech support, making them highly vulnerable to churn."*
> **Retention action:** *Offer a discounted 12-month contract and a free one-month trial of tech support.*

## 📈 Dashboard
**Page 1 — Executive Overview:** KPI cards, risk distribution, tenure churn trend, revenue breakdown
**Page 2 — Risk Segments:** churn by contract type & monthly charges, interactive filters
**Page 3 — High-Risk Customer Explorer:** searchable table with AI-generated explanations

📹 [Watch the walkthrough video](#) *(add your link here)*

## 🛠️ Tech Stack
`MySQL` · `Python` (Pandas, scikit-learn, XGBoost) · `Groq API` (GPT-oss-20b) · `Power BI` · `SQLAlchemy`

## 📂 Repo Structure


## 🚀 How to Run
1. Load the dataset into MySQL using `sql/churn_setup_and_analysis.sql`
2. Run `python/churn_eda.py` → `churn_model.py` → `churn_explainer.py` in order
3. Open `dashboard/churn_dashboard.pbix` in Power BI Desktop and refresh the data source

---
*Built by Shiva Shakthi Manivannan as part of a Data Analyst → AI/Gen AI  portfolio transition.*
