import pandas as pd

# -----------------------------
# 1. Load raw data
# -----------------------------
input_file = "../data/raw/money_dashboard_raw_transactions.csv"

df = pd.read_csv(input_file)

print("Original rows:", len(df))
print("\nColumn information:")
print(df.info())

# -----------------------------
# 2. Check missing values
# -----------------------------
print("\nMissing values:")
print(df.isnull().sum())

# -----------------------------
# 3. Check duplicate transactions
# -----------------------------
print("\nDuplicate transaction IDs:", df["Transaction_ID"].duplicated().sum())

# Remove duplicate Transaction_ID records
df = df.drop_duplicates(subset="Transaction_ID", keep="first")

print("Rows after removing duplicates:", len(df))

# -----------------------------
# 4. Convert date column
# -----------------------------
df["Transaction_Date"] = pd.to_datetime(
    df["Transaction_Date"],
    errors="coerce"
)

# -----------------------------
# 5. Handle missing categories
# -----------------------------
df["Category"] = df["Category"].fillna("Unknown")

# -----------------------------
# 6. Handle missing payment methods
# -----------------------------
df["Payment_Method"] = df["Payment_Method"].fillna("Unknown")

# -----------------------------
# 7. Handle blank descriptions
# -----------------------------
df["Description"] = df["Description"].fillna("")

df["Description"] = df["Description"].replace(
    "",
    "Not Provided"
)

# -----------------------------
# 8. Check invalid amounts
# -----------------------------
negative_amounts = (df["Amount"] < 0).sum()

print("\nNegative amounts found:", negative_amounts)

# Convert invalid negative amounts to missing
df.loc[df["Amount"] < 0, "Amount"] = pd.NA

# Fill invalid amounts using the median
median_amount = df["Amount"].median()

df["Amount"] = df["Amount"].fillna(median_amount)

# -----------------------------
# 9. Validate payment status
# -----------------------------
valid_statuses = [
    "Paid",
    "Pending",
    "Partially Paid"
]

df.loc[
    ~df["Payment_Status"].isin(valid_statuses),
    "Payment_Status"
] = "Unknown"

# -----------------------------
# 10. Validate amount
# -----------------------------
df["Amount"] = pd.to_numeric(
    df["Amount"],
    errors="coerce"
)

# Remove records where amount is still invalid
df = df.dropna(subset=["Amount"])

# -----------------------------
# 11. Sort data
# -----------------------------
df = df.sort_values("Transaction_Date")

# -----------------------------
# 12. Final data-quality check
# -----------------------------
print("\nFinal missing values:")
print(df.isnull().sum())

print("\nFinal rows:", len(df))

print("\nFinal duplicate IDs:",
      df["Transaction_ID"].duplicated().sum())

# -----------------------------
# 13. Save cleaned dataset
# -----------------------------
output_file = "../data/cleaned/clean_transactions.csv"

df.to_csv(output_file, index=False)

print("\nCleaned dataset saved to:")
print(output_file) 