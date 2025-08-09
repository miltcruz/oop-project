import os
import sqlite3
import os
import pandas as pd
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "oop.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create Customer table
cursor.execute('''
	CREATE TABLE IF NOT EXISTS Customer (
		CustomerID INTEGER PRIMARY KEY,
		Gender TEXT,
		Age INTEGER,
		Tenure INTEGER,
		Balance REAL,
		NumOfProducts INTEGER,
		IsActiveMember INTEGER,
		EstimatedSalary REAL,
		Exited BOOLEAN
	)
''')
conn.commit()

# Load data from CSV
csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "customer_churn.csv")
df = pd.read_csv(csv_path)

# Insert data into Customer table
df.to_sql('Customer', conn, if_exists='replace', index=False)
conn.commit()

print("Customer table created and data loaded successfully.")



