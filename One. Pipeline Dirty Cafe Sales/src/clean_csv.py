import pandas as pd
import numpy as np
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "dirty_cafe_sales.csv"

df_cafe = pd.read_csv(DATA_PATH)
print(df_cafe)

# Mapping Price Per Unit and Item column with dict values discovered from data analysis.
df_coluna_nova_price_per_unit = df_cafe.copy()
df_coluna_nova_price_per_unit.drop("Price Per Unit", axis = 1)

preco_por_item = {
    "Coffee": 2.0,
    "Cake": 3.0,
    "Cookie": 1.0,
    "Salad": 5.0,
    "Smoothie": 4.0,
    "Sandwich": 4.0,
    "Juice": 3.0,
    "Tea": 1.5
}

df_coluna_nova_price_per_unit["Price Per Unit"] = df_coluna_nova_price_per_unit["Item"].map(preco_por_item)
df_coluna_nova_price_per_unit

df_coluna_nova_price_per_unit.loc[df_coluna_nova_price_per_unit["Item"] == "ERROR"]

df_coluna_nova_item = df_coluna_nova_price_per_unit.copy()
df_coluna_nova_item.drop("Item", axis = 1)

preco_por_item = {
    "Coffee": 2.0,
    "Cake": 3.0,
    "Cookie": 1.0,
    "Salad": 5.0,
    "Smoothie": 4.0,
    "Sandwich": 4.0,
    
    "Juice": 3.0,
    "Tea": 1.5
}

df_coluna_nova_item["Quantity"] = pd.to_numeric(
    df_coluna_nova_item["Quantity"], errors="coerce"
)

df_coluna_nova_item["Total Spent"] = pd.to_numeric(
    df_coluna_nova_item["Total Spent"], errors="coerce"
)

preco_para_item = defaultdict(list)

for item, preco in preco_por_item.items():
    preco_para_item[preco].append(item)


def inferir_item(row, tol=0.01):
    item = row["Item"]

    if pd.isna(item) or item in ["ERROR", "UNKNOWN"]:
        if row["Quantity"] > 0:
            preco_unit = row["Total Spent"] / row["Quantity"]

            for preco, itens in preco_para_item.items():
                if np.isclose(preco_unit, preco, atol=tol):
                    if len(itens) == 1:
                        return itens[0]
                    else:
                        return "AMBIGUOUS"

    return item

df_coluna_nova_item["Item"] = df_coluna_nova_item.apply(inferir_item, axis=1)
df_coluna_nova_item

# Filtering null values at column "Item"

df_coluna_nova_item_filtro = df_coluna_nova_item[
    df_coluna_nova_item["Item"].isna()
]
df_coluna_nova_item_filtro

## I certified it has values likeNAN, ERROR E UNKNOWN at column "ITEM", so how we can't tell what value fill, we can drop this lines.
df_coluna_nova_item.drop(
    df_coluna_nova_item[
        df_coluna_nova_item["Item"].isin(["UNKNOWN", "ERROR"]) |
        df_coluna_nova_item["Item"].isna()
    ].index,
    inplace=True
)
df_coluna_nova_item

df_coluna_nova_item["Quantity"] = (
    df_coluna_nova_item["Total Spent"] / df_coluna_nova_item["Price Per Unit"]
)
df_coluna_nova_item

df_coluna_nova_item["Price Per Unit"] = df_coluna_nova_item["Item"].map(preco_por_item)

#Localizing ambiguos itens 

df_coluna_nova_item.loc[
    df_coluna_nova_item["Item"] == "AMBIGUOUS",
    "Price Per Unit"
].value_counts(dropna=False)

filtro_ambiguo = df_coluna_nova_item[df_coluna_nova_item["Item"] == "AMBIGUOUS"]

## It has ambiguos price per unit information - cake e juice -> 3.0
                        #Smoothie e Sandwich -> 4.0

# To solve this, we need to create a mask for this. When module division by 2 of Total Spent column values equals to 0, then it will be filled with Sandwich.
# When differ for 0, then will be Cake!!

mask_amb = df_coluna_nova_item["Item"] == "AMBIGUOUS"

df_coluna_nova_item.loc[
    mask_amb & (df_coluna_nova_item["Total Spent"] % 2 == 0),
    "Item"
] = "Sandwich"

df_coluna_nova_item.loc[
    mask_amb & (df_coluna_nova_item["Total Spent"] % 2 != 0),
    "Item"
] = "Cake"


df_coluna_nova_item["Price Per Unit"] = df_coluna_nova_item["Item"].map(preco_por_item)

df_coluna_nova_item["Total Spent"] = pd.to_numeric(
    df_coluna_nova_item["Total Spent"], errors="coerce"
)

df_coluna_nova_item["Price Per Unit"] = pd.to_numeric(
    df_coluna_nova_item["Price Per Unit"], errors="coerce"
)

df_coluna_nova_item["Quantity"] = (
    df_coluna_nova_item["Total Spent"] / df_coluna_nova_item["Price Per Unit"]
)
df_coluna_nova_item

df_coluna_nova_item = df_coluna_nova_item.dropna(subset=["Quantity"])
df_coluna_nova_item
df_coluna_nova_item.isnull().sum()

# Column Quantity to int.
df_coluna_nova_item["Quantity"] = df_coluna_nova_item["Quantity"].astype(int)

# Filtering null values in Payment Method Column and filling with Credit Card"
df_ajustes_payment_method = df_coluna_nova_item[df_coluna_nova_item["Payment Method"].isna()]
df_ajustes_payment_method
df_coluna_nova_item["Payment Method"] = (
    df_coluna_nova_item["Payment Method"].fillna("Credit Card")
)
df_coluna_nova_item

#Replacing UNKNOWN AND ERROR VALUES WITH VALID VALUES AT DATASET.
df_coluna_nova_item["Payment Method"] = (
    df_coluna_nova_item["Payment Method"]
    .replace({
        "UNKNOWN": "Cash",
        "ERROR": "Digital Wallet"
    })
)

df_coluna_nova_item["Location"] = (
    df_coluna_nova_item["Location"].fillna("In-store")
)
df_coluna_nova_item

df_coluna_nova_item["Location"] = (
    df_coluna_nova_item["Location"]
    .replace({
        "UNKNOWN": "Takaway",
        "ERROR": "Takeaway"
    })
)
df_coluna_nova_item


df_ajustes_transaction_date = df_coluna_nova_item[df_coluna_nova_item["Transaction Date"].isna()]
df_ajustes_transaction_date

df_coluna_nova_item["Transaction Date"] = (
    df_coluna_nova_item["Transaction Date"].fillna("2025-12-22")
)

df_coluna_nova_item["Transaction Date"] = (
    df_coluna_nova_item["Transaction Date"]
    .replace({
        "UNKNOWN": "2025-12-22",
        "ERROR": "2025-12-22"
    })
)
df_coluna_nova_item

#Dataset adjusted and cleaned!!!

dirty_cafe_sales_adjusted = df_coluna_nova_item.copy()
dirty_cafe_sales_adjusted["Transaction Date"] = pd.to_datetime(dirty_cafe_sales_adjusted['Transaction Date'])
dirty_cafe_sales_adjusted.info()
dirty_cafe_sales_adjusted.to_excel("Dirty_Cafe_Sales_adjusted2.xlsx", index = False)
