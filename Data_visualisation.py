"""RideMate - Data visualisation. Run: python Data_visualisation.py"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "clean_dataset.csv"
OUTPUT_DIR = BASE_DIR / "visualisations"
OUTPUT_DIR.mkdir(exist_ok=True)

def save_bar(series, title, xlabel, ylabel, filename, rotate=25):
    ax = series.plot(kind="bar")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=rotate, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=150)
    plt.close()

def main():
    df = pd.read_csv(DATA_FILE)

    save_bar(df["Status"].value_counts(), "Booking Status", "Status", "Number of bookings",
             "booking_status.png", 0)
    save_bar(df["Pickup_Location"].value_counts().head(10), "Top Pickup Locations",
             "Pickup location", "Bookings", "pickup_locations.png")
    save_bar(df["Destination"].value_counts().head(10), "Popular Destinations",
             "Destination", "Bookings", "popular_destinations.png")
    save_bar(df.groupby("College")["Request_ID"].count().sort_values(ascending=False),
             "Bookings by College", "College", "Bookings", "college_bookings.png")

    plt.figure()
    plt.hist(df["Estimated_Cab_Fare_INR"], bins=10)
    plt.title("Distribution of Estimated Cab Fares")
    plt.xlabel("Estimated fare (INR)")
    plt.ylabel("Number of bookings")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "fare_distribution.png", dpi=150)
    plt.close()

    print(f"Visualisations saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
