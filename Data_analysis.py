"""RideMate - Basic data analysis. Run: python Data_analysis.py"""
from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent / "clean_dataset.csv"

def main():
    df = pd.read_csv(DATA_FILE)
    print("\nRIDE MATE - DATA ANALYSIS")
    print("=" * 40)
    print(f"Total booking requests: {len(df)}")
    print(f"Unique students: {df['Student_ID'].nunique()}")
    print(f"Total seats requested: {df['Seats_Needed'].sum()}")
    print(f"Average estimated cab fare: Rs. {df['Estimated_Cab_Fare_INR'].mean():.2f}")
    print("\nBookings by status:")
    print(df["Status"].value_counts().to_string())
    print("\nTop pickup locations:")
    print(df["Pickup_Location"].value_counts().head(5).to_string())
    print("\nTop destinations:")
    print(df["Destination"].value_counts().head(5).to_string())
    print("\nBookings by college:")
    print(df["College"].value_counts().to_string())

if __name__ == "__main__":
    main()
