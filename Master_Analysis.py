import pandas as pd 
import matplotlib.pyplot as plt
import os
## ===================================================================
#   RAVVION INDIA TRADE ANALYSIS 
#   Load and Inspect Master Data
##=====================================================================

# Load Master CSV

file_path = "MASTER_TABLE_2020-2025.CSV.csv"

df = pd.read_csv(file_path)

# Basic Inspection
print("===========DATASET SHAPE=============")
print(df.shape)

print("\n============COLUMN NAMES=================")
print(df.columns.tolist())

print("===========First---> 5 ----> RAW===========")
print(df.head)

print("\n============DATA_TYPES==============")
print(df.dtypes)

print("\n=============MISSING_VALUES====================")
print(df.isnull().sum())



# ============================================================
# STEP 2: DATA CLEANING
# Business Question:
# "Is our Master Trade dataset clean and ready for analysis?"
# ============================================================

# Remove completely empty rows
df = df.dropna(how="all")

# Clean column names
df.columns = df.columns.str.strip()

# Clean text columns
text_columns = [
    "Financial_Year",
    "Trade_Type",
    "HS_Code",
    "Commodity",
    "Source_File"
]

for col in text_columns:
    df[col] = df[col].astype("string").str.strip()

# Convert numeric columns
numeric_columns = [
    "Trade_Value_Crore",
    "Market_share_Pct",
    "YoY_Growth_Pct"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Check cleaned structure
print("\n========== CLEANED DATASET ==========")
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n========== DATA TYPES AFTER CLEANING ==========")
print(df.dtypes)

print("\n========== MISSING VALUES AFTER CLEANING ==========")
print(df.isnull().sum())

print("\n========== LAST 5 RECORDS ==========")
print(df.tail())


# ============================================================
# STEP 3: DATA VALIDATION
# Business Question:
# "Does the Master Trade dataset contain valid and unique
# records for analysis?"
# ============================================================

print("\n========== UNIQUE FINANCIAL YEARS ==========")
print(df["Financial_Year"].dropna().unique())

print("\n========== UNIQUE TRADE TYPES ==========")
print(df["Trade_Type"].dropna().unique())

print("\n========== HS CODE COUNT ==========")
print(df["HS_Code"].nunique())

print("\n========== DUPLICATE RECORDS ==========")
print(df.duplicated().sum())

print("\n========== NUMERIC SUMMARY ==========")
print(df[
    ["Trade_Value_Crore", "Market_share_Pct", "YoY_Growth_Pct"]
].describe())

yearly_trade = (
    df.groupby("Financial_Year")["Trade_Value_Crore"]
      .sum()
      .reset_index()
      .sort_values("Financial_Year")
)

print("\n========== BUSINESS QUESTION 1 ==========")
print("How did India's Export Trade Value change by Financial Year?")

print(yearly_trade)

hs_trade = (
    df.groupby(["HS_Code", "Commodity"])["Trade_Value_Crore"]
      .sum()
      .reset_index()
      .sort_values("Trade_Value_Crore", ascending=False)
)

print("\n========== BUSINESS QUESTION 2 ==========")
print("Which HS Chapter generated the highest Export Trade Value?")

print(hs_trade.head(10))

growth = (
    df[["Financial_Year", "HS_Code", "Commodity", "YoY_Growth_Pct"]]
    .dropna()
    .sort_values("YoY_Growth_Pct", ascending=False)
)

print("\n========== BUSINESS QUESTION 3 ==========")
print("Which commodity had the highest YoY Growth?")

print(growth.head(10))

# ============================================================
# Q4: TOP 10 COMMODITIES BY EXPORT TRADE VALUE
# ============================================================

top_commodities = (
    df.groupby(["HS_Code", "Commodity"])["Trade_Value_Crore"]
      .sum()
      .reset_index()
      .sort_values("Trade_Value_Crore", ascending=False)
      .head(10)
)
print("\n========== Q4: TOP 10 COMMODITIES BY EXPORT VALUE ==========")
print(top_commodities)


# ============================================================
# Q5: MARKET SHARE ANALYSIS
# ============================================================

market_share = (
    df.groupby(["HS_Code", "Commodity"])["Market_share_Pct"]
      .mean()
      .reset_index()
      .sort_values("Market_share_Pct", ascending=False)
      .head(10)
)

print("\n========== Q5: TOP 10 COMMODITIES BY MARKET SHARE ==========")
print(market_share)






# ==============================
# LOAD MASTER DATA
# ==============================

file_path = "MASTER_TABLE_2020-2025.CSV.csv"

df = pd.read_csv(file_path)

# Convert numeric columns
df["Trade_Value_Crore"] = pd.to_numeric(
    df["Trade_Value_Crore"], errors="coerce"
)

df["Market_share_Pct"] = pd.to_numeric(
    df["Market_share_Pct"], errors="coerce"
)

df["YoY_Growth_Pct"] = pd.to_numeric(
    df["YoY_Growth_Pct"], errors="coerce"
)

# Remove incomplete rows
df = df.dropna(subset=["Financial_Year", "Trade_Value_Crore"])

# Create charts folder
os.makedirs("charts", exist_ok=True)


# ==================================================
# CHART 1 — TOTAL EXPORT VALUE BY FINANCIAL YEAR
# Business Question:
# Which financial year generated the highest export value?
# ==================================================

yearly_export = (
    df.groupby("Financial_Year")["Trade_Value_Crore"]
      .sum()
      .sort_index()
)

plt.figure(figsize=(10, 6))

plt.plot(
    yearly_export.index,
    yearly_export.values,
    marker="o"
)

plt.title("India Export Value by Financial Year")
plt.xlabel("Financial Year")
plt.ylabel("Total Export Value (₹ Crore)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "charts/01_export_value_by_year.png",
    dpi=300
)

plt.show()


# ==================================================
# CHART 2 — TOP 10 COMMODITIES BY EXPORT VALUE
# Business Question:
# Which commodities contribute the most to India's exports?
# ==================================================

top_10 = (
    df.groupby("Commodity")["Trade_Value_Crore"]
      .sum()
      .sort_values(ascending=False)
      .head(10)
      .sort_values()
)

plt.figure(figsize=(10, 7))

plt.barh(
    top_10.index,
    top_10.values
)

plt.title("Top 10 Export Commodities by Trade Value")
plt.xlabel("Total Export Value (₹ Crore)")
plt.ylabel("Commodity")

plt.tight_layout()

plt.savefig(
    "charts/02_top_10_export_commodities.png",
    dpi=300
)

plt.show()


# ==================================================
# CHART 3 — MARKET SHARE BY FINANCIAL YEAR
# Business Question:
# How does India's export market share change over time?
# ==================================================

market_share = (
    df.groupby("Financial_Year")["Market_share_Pct"]
      .mean()
      .sort_index()
)

plt.figure(figsize=(10, 6))

plt.plot(
    market_share.index,
    market_share.values,
    marker="o"
)

plt.title("Average Export Market Share by Financial Year")
plt.xlabel("Financial Year")
plt.ylabel("Market Share (%)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "charts/03_market_share_by_year.png",
    dpi=300
)

plt.show()


# ==================================================
# FINAL BUSINESS INSIGHTS
# ==================================================

highest_year = yearly_export.idxmax()
highest_value = yearly_export.max()

highest_commodity = top_10.idxmax()
highest_commodity_value = top_10.max()

highest_market_share_year = market_share.idxmax()
highest_market_share = market_share.max()

print("\n================ BUSINESS INSIGHTS ================\n")

print(
    f"1. Highest export value was recorded in "
    f"{highest_year}: ₹{highest_value:,.2f} Crore"
)

print(
    f"2. Top export commodity was "
    f"{highest_commodity}: ₹{highest_commodity_value:,.2f} Crore"
)

print(
    f"3. Highest average market share was recorded in "
    f"{highest_market_share_year}: {highest_market_share:.2f}%"
)

print("\n====================================================")
print("MASTER ANALYSIS COMPLETED SUCCESSFULLY")
print("====================================================")

# ============================================================
# FINAL CLEANING - RELOAD RAW MASTER CSV
# ============================================================

# Reload ORIGINAL CSV
df = pd.read_csv("MASTER_TABLE_2020-2025.CSV.csv")

# Clean column names
df.columns = df.columns.str.strip()


# ------------------------------------------------------------
# 1. Remove repeated header rows
# ------------------------------------------------------------

df = df[
    df["Financial_Year"].astype(str).str.strip() != "Financial_Year"
]


# ------------------------------------------------------------
# 2. Remove completely blank rows
# ------------------------------------------------------------

df = df.dropna(how="all")


# ------------------------------------------------------------
# 3. Clean text columns
# ------------------------------------------------------------

text_columns = [
    "Financial_Year",
    "Trade_Type",
    "HS_Code",
    "Commodity",
    "Source_File"
]

for col in text_columns:
    df[col] = (
        df[col]
        .astype("string")
        .str.strip()
    )


# ------------------------------------------------------------
# 4. IMPORTANT:
# Clean comma from Trade Value BEFORE numeric conversion
# ------------------------------------------------------------

df["Trade_Value_Crore"] = (
    df["Trade_Value_Crore"]
    .astype("string")
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["Trade_Value_Crore"] = pd.to_numeric(
    df["Trade_Value_Crore"],
    errors="coerce"
)


# ------------------------------------------------------------
# 5. Convert Market Share
# ------------------------------------------------------------

df["Market_share_Pct"] = pd.to_numeric(
    df["Market_share_Pct"],
    errors="coerce"
)


# ------------------------------------------------------------
# 6. Convert YoY Growth
# ------------------------------------------------------------

df["YoY_Growth_Pct"] = pd.to_numeric(
    df["YoY_Growth_Pct"],
    errors="coerce"
)


# ------------------------------------------------------------
# 7. Keep only our 5 Financial Years
# ------------------------------------------------------------

valid_years = [
    "2020-2021",
    "2021-2022",
    "2022-2023",
    "2023-2024",
    "2024-2025"
]

df = df[
    df["Financial_Year"].isin(valid_years)
]


# ------------------------------------------------------------
# 8. Keep only Export
# ------------------------------------------------------------

df["Trade_Type"] = (
    df["Trade_Type"]
    .astype("string")
    .str.strip()
)

df = df[
    df["Trade_Type"] == "Export"
]


# ------------------------------------------------------------
# 9. Remove incomplete records
# ------------------------------------------------------------

df = df.dropna(
    subset=[
        "Financial_Year",
        "HS_Code",
        "Commodity",
        "Trade_Value_Crore"
    ]
)


# ------------------------------------------------------------
# 10. Remove exact duplicates
# ------------------------------------------------------------

df = df.drop_duplicates()


# ------------------------------------------------------------
# 11. Save CLEAN CSV
# ------------------------------------------------------------

clean_file = "Clean_Master_2020_2025.csv"

df.to_csv(
    clean_file,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("\n========== CLEAN CSV CREATED ==========")
print("File:", clean_file)
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n========== RECORDS BY YEAR ==========")
print(
    df.groupby("Financial_Year").size()
)

print("\n========== TRADE TYPES ==========")
print(
    df["Trade_Type"].unique()
)

print("\n========== MISSING VALUES ==========")
print(
    df.isnull().sum()
)


# ============================================================
# FINAL CLEANING - RELOAD RAW MASTER CSV
# ============================================================

# Reload ORIGINAL CSV
df = pd.read_csv("MASTER_TABLE_2020-2025.CSV.csv")

# Clean column names
df.columns = df.columns.str.strip()


# ------------------------------------------------------------
# 1. Remove repeated header rows
# ------------------------------------------------------------

df = df[
    df["Financial_Year"].astype(str).str.strip() != "Financial_Year"
]


# ------------------------------------------------------------
# 2. Remove completely blank rows
# ------------------------------------------------------------

df = df.dropna(how="all")


# ------------------------------------------------------------
# 3. Clean text columns
# ------------------------------------------------------------

text_columns = [
    "Financial_Year",
    "Trade_Type",
    "HS_Code",
    "Commodity",
    "Source_File"
]

for col in text_columns:
    df[col] = (
        df[col]
        .astype("string")
        .str.strip()
    )


# ------------------------------------------------------------
# 4. IMPORTANT:
# Clean comma from Trade Value BEFORE numeric conversion
# ------------------------------------------------------------

df["Trade_Value_Crore"] = (
    df["Trade_Value_Crore"]
    .astype("string")
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["Trade_Value_Crore"] = pd.to_numeric(
    df["Trade_Value_Crore"],
    errors="coerce"
)


# ------------------------------------------------------------
# 5. Convert Market Share
# ------------------------------------------------------------

df["Market_share_Pct"] = pd.to_numeric(
    df["Market_share_Pct"],
    errors="coerce"
)


# ------------------------------------------------------------
# 6. Convert YoY Growth
# ------------------------------------------------------------

df["YoY_Growth_Pct"] = pd.to_numeric(
    df["YoY_Growth_Pct"],
    errors="coerce"
)


# ------------------------------------------------------------
# 7. Keep only our 5 Financial Years
# ------------------------------------------------------------

valid_years = [
    "2020-2021",
    "2021-2022",
    "2022-2023",
    "2023-2024",
    "2024-2025"
]

df = df[
    df["Financial_Year"].isin(valid_years)
]


# ------------------------------------------------------------
# 8. Keep only Export
# ------------------------------------------------------------

df["Trade_Type"] = (
    df["Trade_Type"]
    .astype("string")
    .str.strip()
)

df = df[
    df["Trade_Type"] == "Export"
]


# ------------------------------------------------------------
# 9. Remove incomplete records
# ------------------------------------------------------------

df = df.dropna(
    subset=[
        "Financial_Year",
        "HS_Code",
        "Commodity",
        "Trade_Value_Crore"
    ]
)


# ------------------------------------------------------------
# 10. Remove exact duplicates
# ------------------------------------------------------------

df = df.drop_duplicates()


# ------------------------------------------------------------
# 11. Save CLEAN CSV
# ------------------------------------------------------------

clean_file = "Clean_Master_2020_2025.csv"

df.to_csv(
    clean_file,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("\n========== CLEAN CSV CREATED ==========")
print("File:", clean_file)
print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\n========== RECORDS BY YEAR ==========")
print(
    df.groupby("Financial_Year").size()
)

print("\n========== TRADE TYPES ==========")
print(
    df["Trade_Type"].unique()
)

print("\n========== MISSING VALUES ==========")
print(
    df.isnull().sum()
)
