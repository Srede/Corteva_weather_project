import pandas as pd
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

# Logging setup
logging.basicConfig(filename='data_analysis.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# PostgreSQL connection setup
engine = create_engine('postgresql://postgres:corteva@localhost:5432/weather_data')

def calculate_statistics():
    query = """
    SELECT station_id, EXTRACT(YEAR FROM date) AS year, max_temp, min_temp, precipitation
    FROM weather_data
    WHERE max_temp IS NOT NULL OR min_temp IS NOT NULL OR precipitation IS NOT NULL
    """
    
    # Load the data from PostgreSQL into a DataFrame
    df = pd.read_sql(query, engine)

    # Group by station and year, and calculate statistics
    stats_df = df.groupby(['station_id', 'year']).agg(
        avg_max_temp=('max_temp', lambda x: round(x.mean() / 10, 2) if not x.isnull().all() else None),
        avg_min_temp=('min_temp', lambda x: round(x.mean() / 10, 2) if not x.isnull().all() else None),
        total_precipitation=('precipitation', lambda x: round(x.sum() / 100, 2) if not x.isnull().all() else None)
    ).reset_index()

    # Insert the calculated stats into weather_stats table
    insert_query = text("""
        INSERT INTO weather_stats (station_id, year, avg_max_temp, avg_min_temp, total_precipitation)
        VALUES (:station_id, :year, :avg_max_temp, :avg_min_temp, :total_precipitation)
        ON CONFLICT (station_id, year) DO NOTHING;
    """)
    
    # Insert into PostgreSQL
    with engine.begin() as connection:
        for index, row in stats_df.iterrows():
            connection.execute(insert_query, {
                'station_id': row['station_id'],
                'year': row['year'],
                'avg_max_temp': row['avg_max_temp'],
                'avg_min_temp': row['avg_min_temp'],
                'total_precipitation': row['total_precipitation']
            })
    
    logging.info(f'Successfully inserted {len(stats_df)} records into weather_stats table.')

# Run the function
calculate_statistics()
