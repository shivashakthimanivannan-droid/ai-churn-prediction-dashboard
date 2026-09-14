import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shiva@2003",
    database="telco_churn"
)
df = pd.read_sql("SELECT * FROM customers;", conn)
conn.close()

sns.set_style("whitegrid")

plt.figure(figsize=(7,5))
sns.histplot(data=df, x="tenure", hue="Churn", multiple="stack", bins=30, palette=["#2E75B6", "#C00000"])
plt.title("Customer Tenure Distribution by Churn Status")
plt.xlabel("Tenure (months)")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()