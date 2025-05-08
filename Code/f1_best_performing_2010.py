import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV file
csv_file = 'f1_driver_data_2000_2025.csv'
try:
    df = pd.read_csv(csv_file)
except FileNotFoundError:
    print(f"Error: {csv_file} not found. Please ensure the file exists in the current directory.")
    exit(1)

# Filter for 2010 season
df_2000 = df[df['Year'] == 2000].copy()

# Check if data exists for 2010
if df_2000.empty:
    print("Error: No data found for the 2010 season in the CSV.")
    exit(1)

# Get unique circuits (RaceName)
circuits = df_2000['RaceName'].unique()

# Count wins (Position == 1) per driver and circuit
wins = df_2000[df_2000['Position'] == 1][['DriverName', 'RaceName']].groupby(['DriverName', 'RaceName']).size().unstack(fill_value=0)

# Get top 5 drivers by total wins
top_drivers = wins.sum(axis=1).sort_values(ascending=False).head(5).index
wins_top = wins.loc[top_drivers]

# Create heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(wins_top, annot=True, fmt='d', cmap='YlGnBu', cbar_kws={'label': 'Number of Wins'})
plt.title('Top 5 F1 Drivers by Wins per Circuit in 2000')
plt.xlabel('Circuit')
plt.ylabel('Driver')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save plot
plt.savefig('f1_2000_driver_performance.png')
plt.close()
print("Plot saved as f1_2000_driver_performance.png")