import pandas as pd
import sqlite3

# Load cleaned data
input_file = "../data/cleaned/clean_transactions.csv"

df = pd.read_csv(input_file)

# Connect to SQLite database
database_file = "../database/money_dashboard.db"

connection = sqlite3.connect(database_file)

# Create transactions table
df.to_sql(
    "transactions",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("Database created successfully!")
print("Rows loaded:", len(df))
print("Table created: transactions")
print("Database:", database_file)