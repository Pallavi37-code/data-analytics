"""
RideMate - Data Cleaning
Input : Dataset.csv (raw/original dataset)
Output: clean_dataset.csv

Run:
    python data_cleaning.py
"""
from pathlib import Path
import pandas as pd
import re

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "Dataset.csv"
OUTPUT_FILE = BASE_DIR / "clean_dataset.csv"

REQUIRED = [
    "Request_ID", "Student_ID", "College", "Pickup_Location", "Destination",
    "Travel_Date", "Travel_Time", "Seats_Needed",
    "Estimated_Cab_Fare_INR", "Status"
]

def clean_text(value):
    if pd.isna(value):
        return ""
    return re.sub(r"\s+", " ", str(value)).strip()

def parse_number(value):
    """Convert values such as '3 seats' and '₹1,000' into numbers."""
    if pd.isna(value):
        return pd.NA
    digits = re.sub(r"[^0-9.-]", "", str(value))
    if not digits:
        return pd.NA
    try:
        number = float(digits)
        return int(number) if number.is_integer() else number
    except ValueError:
        return pd.NA

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Could not find {INPUT_FILE.name}")

    df = pd.read_csv(INPUT_FILE, dtype=str)
    missing_columns = [c for c in REQUIRED if c not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df = df[REQUIRED].copy()

    # Standardize text fields and common inconsistent capitalization.
    text_cols = ["Request_ID", "Student_ID", "College", "Pickup_Location",
                 "Destination", "Travel_Time", "Status"]
    for col in text_cols:
        df[col] = df[col].map(clean_text)

    for col in ["College", "Pickup_Location", "Destination", "Status"]:
        df[col] = df[col].str.title()

    # Normalize dates and times. Mixed date formats are accepted.
    df["Travel_Date"] = pd.to_datetime(
        df["Travel_Date"], errors="coerce", dayfirst=True
    ).dt.strftime("%Y-%m-%d")

    parsed_time = pd.to_datetime(df["Travel_Time"], errors="coerce")
    df["Travel_Time"] = parsed_time.dt.strftime("%H:%M")

    # Convert numeric columns.
    df["Seats_Needed"] = df["Seats_Needed"].map(parse_number)
    df["Estimated_Cab_Fare_INR"] = df["Estimated_Cab_Fare_INR"].map(parse_number)

    # Remove rows that cannot represent a valid booking.
    df = df.dropna(subset=[
        "Request_ID", "Student_ID", "College", "Pickup_Location", "Destination",
        "Travel_Date", "Travel_Time", "Seats_Needed", "Estimated_Cab_Fare_INR", "Status"
    ])
    df = df[
        (df["Request_ID"] != "") &
        (df["Seats_Needed"] > 0) &
        (df["Estimated_Cab_Fare_INR"] >= 0)
    ]

    # Remove repeated booking IDs; keep the first valid occurrence.
    df = df.drop_duplicates(subset=["Request_ID"], keep="first")

    # Restore integer types and consistent column order.
    df["Seats_Needed"] = df["Seats_Needed"].astype(int)
    df["Estimated_Cab_Fare_INR"] = df["Estimated_Cab_Fare_INR"].astype(int)
    df = df[REQUIRED].reset_index(drop=True)

    df.to_csv(OUTPUT_FILE, index=False)
    print("Data cleaning completed successfully.")
    print(f"Rows in cleaned dataset: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
