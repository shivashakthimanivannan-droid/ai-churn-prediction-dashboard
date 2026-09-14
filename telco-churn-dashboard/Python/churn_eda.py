#Connection with the sql with vs code
import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shiva@2003",
    database="telco_churn"
)

query = "SELECT * FROM customers;"
df = pd.read_sql(query, conn)

print(df.shape)
print(df.head())

conn.close()

#Visualisation
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")

plt.figure(figsize=(7,5))
sns.countplot(data=df, x="Contract", hue="Churn", palette=["#2E75B6", "#C00000"])
plt.title("Customer Churn by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.show()