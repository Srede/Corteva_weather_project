import os
import pandas as pd
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='ingestion.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL connection setup
engine = create_engine('postgresql://postgres:corteva@localhost:5432/weather_data')

# Function to ingest weather data from a text file
def ingest_weather_data(file_path, station_id):
    start_time = datetime.now()
    logging.info(f'Starting ingestion for {file_path}')
    
    # Load the file into a DataFrame
    df = pd.read_csv(file_path, sep='\t', header=None, names=['date', 'max_temp', 'min_temp', 'precipitation'])
    
    # Replace missing values (-9999) with None
    df.replace(-9999, None, inplace=True)
    
    # Convert the 'date' column to the proper format
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
    
    # Add the station ID to the data
    df['station_id'] = station_id

    # Remove duplicates based on station_id and date
    df.drop_duplicates(subset=['station_id', 'date'], inplace=True)

    # Create list of tuples for batch insertion
    values = [
        {
            'station_id': row['station_id'],
            'date': row['date'],
            'max_temp': row['max_temp'],
            'min_temp': row['min_temp'],
            'precipitation': row['precipitation']
        }
        for index, row in df.iterrows()
    ]
    
    # Insert the data into PostgreSQL using text()
    insert_query = text("""
        INSERT INTO weather_data (station_id, date, max_temp, min_temp, precipitation)
        VALUES (:station_id, :date, :max_temp, :min_temp, :precipitation)
        ON CONFLICT (station_id, date) DO NOTHING;
    """)
    
    with engine.begin() as connection:
        connection.execute(insert_query, values)
    
    end_time = datetime.now()
    logging.info(f'Finished ingestion for {file_path}. Total records ingested: {len(df)}. Duration: {end_time - start_time}')

# Loop through the files in the wx_data directory
data_dir = 'code-challenge-template/wx_data'
for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        station_id = filename.split('.')[0]  # Extract station ID from file name
        file_path = os.path.join(data_dir, filename)
        ingest_weather_data(file_path, station_id)