import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'cleaned_uts_data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'visualizations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")
df = pd.read_csv(DATA_PATH)

# 1. Peak Travel Hours
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="Hour", hue="Hour", palette="viridis", legend=False)
plt.title("Hourly Passenger Booking Volume (Peak Commute Windows)")
plt.xlabel("Hour of Day (24-hr)")
plt.ylabel("Bookings Count")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "peak_hours.png"))
plt.close()

# 2. Top 10 Busiest Routes
plt.figure(figsize=(10, 6))
df['Route'] = df['From_Station'] + " → " + df['To_Station']
top_routes = df['Route'].value_counts().head(10).reset_index()
top_routes.columns = ['Route', 'Count']
sns.barplot(data=top_routes, x='Count', y='Route', hue='Route', palette="mako", legend=False)
plt.title("Top 10 Busiest Commuter Routes")
plt.xlabel("Total Bookings")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "popular_routes.png"))
plt.close()

# 3. Booking Mode Breakdown
plt.figure(figsize=(6, 6))
df['Booking_Mode'].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#2196F3', '#FF9800'])
plt.title("Distribution of Booking Channels")
plt.ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "booking_mode_split.png"))
plt.close()

# 4. Railway Line Revenue
plt.figure(figsize=(8, 5))
line_rev = df.groupby("Railway_Line")["Total_Fare"].sum().reset_index()
sns.barplot(data=line_rev, x="Railway_Line", y="Total_Fare", hue="Railway_Line", palette="rocket", legend=False)
plt.title("Total Fare Revenue by Railway Line (INR)")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "line_revenue.png"))
plt.close()

print(f"Analysis visualizations saved cleanly to: {OUTPUT_DIR}")