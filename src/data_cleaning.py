import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'Uts_Data.csv')
CLEANED_DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'cleaned_uts_data.csv')

def clean_data():
    print("Loading raw UTS data...")
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Raw shape: {df.shape}")

    # Remove duplicate transactions
    df = df.drop_duplicates(subset=['Booking_ID'])
    print(f"Shape after removing duplicates: {df.shape}")

    # Standardize Dates and Times
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Day_Name'] = df['Date'].dt.day_name()
    df['Is_Weekend'] = df['Date'].dt.dayofweek.isin([5, 6]).astype(int)

    # Derive Hour from Time
    time_series = pd.to_datetime(df['Time'].astype(str), format='%H:%M:%S', errors='coerce')
    df['Hour'] = time_series.dt.hour.fillna(0).astype(int)

    # Numeric formatting and validation
    df['Passengers'] = pd.to_numeric(df['Passengers'], errors='coerce').fillna(1).astype(int)
    df['Total_Fare'] = pd.to_numeric(df['Total_Fare'], errors='coerce').fillna(0.0)
    df['Fare_Per_Passenger'] = np.where(df['Passengers'] > 0, (df['Total_Fare'] / df['Passengers']).round(2), 0.0)

    # Clean text columns
    text_cols = ['Ticket_Type', 'Booking_Mode', 'From_Station', 'To_Station', 'Payment_Type', 'Railway_Line', 'City']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    df.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"Cleaned dataset saved: {CLEANED_DATA_PATH}")

if __name__ == "__main__":
    clean_data()