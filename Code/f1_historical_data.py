import fastf1
import pandas as pd
from tqdm import tqdm
import warnings
import os
import logging

# Set up logging
logging.basicConfig(filename='f1_data_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Suppress warnings for cleaner console output
warnings.filterwarnings('ignore')

# Create fresh cache directory
cache_dir = 'f1_cache_2000_2025'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
    logging.info(f"Created cache directory: {cache_dir}")

# Enable caching
fastf1.Cache.enable_cache(cache_dir)
logging.info("Cache enabled")

# Initialize list to store driver data
all_driver_data = []

# Loop through years 2000 to 2025
for year in tqdm(range(2000, 2026), desc="Processing years"):
    try:
        # Get event schedule
        schedule = fastf1.get_event_schedule(year)
        logging.info(f"Loaded schedule for {year}: {len(schedule)} events")
        
        # Filter for race events
        races = schedule[schedule['Session5'] == 'Race']
        logging.info(f"Found {len(races)} races for {year}")
        
        # Loop through each race
        for _, race in races.iterrows():
            try:
                # Load race session (minimal data)
                session = fastf1.get_session(year, race['EventName'], 'R')
                session.load(telemetry=False, laps=False, weather=False)
                logging.info(f"Loaded {year} {race['EventName']}")
                
                # Get race results
                results = session.results
                
                # Extract driver data
                for _, driver in results.iterrows():
                    driver_info = {
                        'Year': year,
                        'RaceName': race['EventName'],
                        'DriverName': driver.get('FullName', driver.get('DriverId', 'Unknown')).title(),
                        'DriverId': driver.get('DriverId', ''),
                        'Team': driver.get('TeamName', ''),
                        'Position': int(driver.get('Position', -1)),
                        'Points': float(driver.get('Points', 0)),
                        'GridPosition': int(driver.get('GridPosition', -1)),
                        'Status': driver.get('Status', ''),
                        'Nationality': driver.get('Nationality', '')
                    }
                    all_driver_data.append(driver_info)
            except Exception as e:
                logging.error(f"Failed to load {year} {race['EventName']}: {str(e)}")
                print(f"Error loading {year} {race['EventName']}: {str(e)}")
                continue
    except Exception as e:
        logging.error(f"Failed to process year {year}: {str(e)}")
        print(f"Error processing year {year}: {str(e)}")
        continue

# Create DataFrame
driver_df = pd.DataFrame(all_driver_data)

# Clean data
driver_df = driver_df.drop_duplicates()
driver_df['Points'] = driver_df['Points'].fillna(0)
driver_df['Position'] = driver_df['Position'].fillna(-1).astype(int)
driver_df['GridPosition'] = driver_df['GridPosition'].fillna(-1).astype(int)
logging.info(f"Created DataFrame with {len(driver_df)} rows")

# Save to CSV
driver_df.to_csv('f1_driver_data_2000_2025.csv', index=False)
print("Data saved to f1_driver_data_2000_2025.csv")
logging.info("Data saved to f1_driver_data_2000_2025.csv")

# Summary
print("\nTop 5 drivers by total points:")
print(driver_df.groupby('DriverName')['Points'].sum().sort_values(ascending=False).head())
print("\nNumber of races per driver:")
print(driver_df.groupby('DriverName')['RaceName'].count().sort_values(ascending=False).head())
logging.info("Printed summary statistics")