"""
Week 1 Internship Project: Logistics Data Analytics
This script demonstrates the planned KPI analysis and a simple late-delivery
classification workflow. It uses a public/simulated CSV named
"logistics_data.csv" when available.
"""

import pandas as pd

DATA_FILE = "logistics_data.csv"


def load_data(path=DATA_FILE):
    return pd.read_csv(path)


def calculate_kpis(df):
    results = {}

    if "on_time" in df.columns:
        results["on_time_delivery_rate_pct"] = df["on_time"].mean() * 100

    if "delivery_days" in df.columns:
        results["average_delivery_time_days"] = df["delivery_days"].mean()

    if {"transport_cost", "order_id"}.issubset(df.columns):
        results["transport_cost_per_delivery"] = (
            df["transport_cost"].sum() / df["order_id"].nunique()
        )

    return results


def prepare_dates(df):
    for column in ["order_date", "delivery_date"]:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    if {"order_date", "delivery_date"}.issubset(df.columns):
        df["delivery_days"] = (
            df["delivery_date"] - df["order_date"]
        ).dt.days

    return df


def main():
    print("Logistics Data Analytics - Week 1")
    try:
        df = load_data()
    except FileNotFoundError:
        print(f"Place your dataset as '{DATA_FILE}' in this folder to run the analysis.")
        return

    print("Rows, columns:", df.shape)
    print("Duplicate rows:", df.duplicated().sum())
    print("\nMissing values:")
    print(df.isna().sum())

    df = df.drop_duplicates()
    df = prepare_dates(df)

    print("\nKPI results:")
    for name, value in calculate_kpis(df).items():
        print(f"{name}: {value:.2f}")


if __name__ == "__main__":
    main()
