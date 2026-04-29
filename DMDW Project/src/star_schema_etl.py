"""
============================================================================
  STAR SCHEMA & ETL PIPELINE MODULE
============================================================================
  Purpose:
    Demonstrates Data Warehousing concepts by simulating:
      1. A Star Schema design with Fact and Dimension tables
      2. An ETL (Extract, Transform, Load) pipeline

  Star Schema Design:
  ┌─────────────────┐     ┌─────────────────┐
  │  DIM_TIME        │     │  DIM_LOCATION    │
  │─────────────────│     │─────────────────│
  │  time_key (PK)   │     │  location_key    │
  │  hour             │     │  urban_or_rural  │
  │  day_of_week      │     │  latitude        │
  │  is_weekend       │     │  longitude       │
  │  time_of_day      │     │  area_type       │
  └────────┬──────────┘     └────────┬──────────┘
           │                         │
           ▼                         ▼
  ┌────────────────────────────────────────────┐
  │              FACT_ACCIDENTS                 │
  │────────────────────────────────────────────│
  │  accident_key (PK)                          │
  │  time_key (FK)  → DIM_TIME                  │
  │  location_key (FK) → DIM_LOCATION           │
  │  weather_key (FK) → DIM_WEATHER             │
  │  road_key (FK) → DIM_ROAD                   │
  │  severity                                   │
  │  num_vehicles (measure)                     │
  │  num_casualties (measure)                   │
  │  speed_limit (measure)                      │
  └────────────────────────────────────────────┘
           ▲                         ▲
           │                         │
  ┌────────┴──────────┐     ┌────────┴──────────┐
  │  DIM_WEATHER      │     │  DIM_ROAD          │
  │─────────────────│     │─────────────────│
  │  weather_key (PK) │     │  road_key (PK)     │
  │  weather_condition │     │  road_type         │
  │  is_bad_weather    │     │  road_surface      │
  │  weather_category  │     │  surface_category  │
  └───────────────────┘     └───────────────────┘

  This module also includes:
    - OLAP-style queries (slice, dice, roll-up, drill-down)
    - Simple aggregation examples
============================================================================
"""

import pandas as pd
import numpy as np
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# ─── Setup ───────────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
WAREHOUSE_DIR = os.path.join(DATA_DIR, 'warehouse')
os.makedirs(WAREHOUSE_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 1: EXTRACT — Load raw data from source
# ═══════════════════════════════════════════════════════════════════════════════

def extract(filepath=None):
    """
    EXTRACT phase of ETL pipeline.
    Loads raw data from the source CSV file.

    In a real-world scenario, this would:
      - Connect to operational databases (OLTP systems)
      - Read from APIs, flat files, or streaming sources
      - Handle multiple data sources

    Parameters:
        filepath (str): Path to the raw data file.

    Returns:
        pd.DataFrame: Raw extracted data.
    """
    print("📥 EXTRACT: Loading raw data from source...")

    if filepath is None:
        filepath = os.path.join(DATA_DIR, 'road_accidents.csv')

    if not os.path.exists(filepath):
        print("   ⚠️  Source data not found. Generating synthetic dataset...")
        sys.path.insert(0, DATA_DIR)
        from generate_dataset import generate_dataset
        df = generate_dataset()
        df.to_csv(filepath, index=False)
    else:
        df = pd.read_csv(filepath)

    print(f"   ✅ Extracted {df.shape[0]:,} records from source")
    return df


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 2: TRANSFORM — Clean and reshape data for the warehouse
# ═══════════════════════════════════════════════════════════════════════════════

def transform(df):
    """
    TRANSFORM phase of ETL pipeline.
    Cleans, enriches, and reshapes data into dimension and fact tables.

    Transformations applied:
      1. Handle missing values
      2. Create surrogate keys for dimension tables
      3. Derive calculated fields (time_of_day, weather_category, etc.)
      4. Normalize data into star schema structure

    Parameters:
        df (pd.DataFrame): Raw extracted data.

    Returns:
        dict: Dictionary of dimension and fact DataFrames.
    """
    print("\n🔄 TRANSFORM: Cleaning and reshaping data...")

    df = df.copy()

    # ── Handle missing values ──
    df['Weather_Conditions'] = df['Weather_Conditions'].fillna('Unknown')
    df['Road_Surface_Conditions'] = df['Road_Surface_Conditions'].fillna('Unknown')
    df['Light_Conditions'] = df['Light_Conditions'].fillna('Unknown')
    df['Road_Type'] = df['Road_Type'].fillna('Unknown')

    # ── Extract hour from Time ──
    if 'Time' in df.columns:
        df['Hour'] = df['Time'].apply(
            lambda x: int(str(x).split(':')[0]) if pd.notna(x) and ':' in str(x) else 12
        )

    # ──────────────────────────────────────────────────────────────
    #  DIMENSION TABLE 1: DIM_TIME
    # ──────────────────────────────────────────────────────────────
    print("   📅 Creating DIM_TIME...")

    # Create unique time dimension entries
    time_df = df[['Day_of_Week', 'Hour']].drop_duplicates().reset_index(drop=True)
    time_df['time_key'] = range(1, len(time_df) + 1)

    # Derived attributes
    day_names = {1: 'Sunday', 2: 'Monday', 3: 'Tuesday', 4: 'Wednesday',
                 5: 'Thursday', 6: 'Friday', 7: 'Saturday'}
    time_df['day_name'] = time_df['Day_of_Week'].map(day_names)
    time_df['is_weekend'] = time_df['Day_of_Week'].apply(lambda x: 1 if x in [1, 7] else 0)

    # Time of day categories
    def time_of_day(hour):
        if 6 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'

    time_df['time_of_day'] = time_df['Hour'].apply(time_of_day)

    # Reorder columns
    dim_time = time_df[['time_key', 'Hour', 'Day_of_Week', 'day_name',
                         'is_weekend', 'time_of_day']]

    # ──────────────────────────────────────────────────────────────
    #  DIMENSION TABLE 2: DIM_LOCATION
    # ──────────────────────────────────────────────────────────────
    print("   📍 Creating DIM_LOCATION...")

    # For simplicity, create location dimension based on Urban/Rural
    # In a full implementation, this would include geographic details
    area_map = {1: 'Urban', 2: 'Rural'}

    location_df = df[['Urban_or_Rural_Area']].drop_duplicates().reset_index(drop=True)
    location_df['location_key'] = range(1, len(location_df) + 1)
    location_df['area_type'] = location_df['Urban_or_Rural_Area'].map(area_map)

    # Add sample coordinates (centroids for urban/rural)
    location_df['avg_latitude'] = location_df['Urban_or_Rural_Area'].map({1: 51.5, 2: 53.0})
    location_df['avg_longitude'] = location_df['Urban_or_Rural_Area'].map({1: -0.12, 2: -1.5})

    dim_location = location_df[['location_key', 'Urban_or_Rural_Area',
                                 'area_type', 'avg_latitude', 'avg_longitude']]

    # ──────────────────────────────────────────────────────────────
    #  DIMENSION TABLE 3: DIM_WEATHER
    # ──────────────────────────────────────────────────────────────
    print("   🌦️  Creating DIM_WEATHER...")

    weather_df = df[['Weather_Conditions']].drop_duplicates().reset_index(drop=True)
    weather_df['weather_key'] = range(1, len(weather_df) + 1)

    # Categorize weather
    def categorize_weather(w):
        if 'Fine' in str(w):
            return 'Clear'
        elif 'Rain' in str(w):
            return 'Precipitation'
        elif 'Snow' in str(w):
            return 'Precipitation'
        elif 'Fog' in str(w):
            return 'Low Visibility'
        else:
            return 'Other'

    weather_df['weather_category'] = weather_df['Weather_Conditions'].apply(categorize_weather)
    bad_terms = ['Raining', 'Snowing', 'Fog', 'high winds']
    weather_df['is_bad_weather'] = weather_df['Weather_Conditions'].apply(
        lambda x: 1 if any(t in str(x) for t in bad_terms) else 0
    )

    dim_weather = weather_df[['weather_key', 'Weather_Conditions',
                               'weather_category', 'is_bad_weather']]

    # ──────────────────────────────────────────────────────────────
    #  DIMENSION TABLE 4: DIM_ROAD
    # ──────────────────────────────────────────────────────────────
    print("   🛣️  Creating DIM_ROAD...")

    road_df = df[['Road_Type', 'Road_Surface_Conditions']].drop_duplicates().reset_index(drop=True)
    road_df['road_key'] = range(1, len(road_df) + 1)

    # Categorize surface
    def categorize_surface(s):
        if s in ['Dry']:
            return 'Good'
        elif s in ['Wet or damp']:
            return 'Moderate'
        else:
            return 'Poor'

    road_df['surface_category'] = road_df['Road_Surface_Conditions'].apply(categorize_surface)

    dim_road = road_df[['road_key', 'Road_Type', 'Road_Surface_Conditions',
                         'surface_category']]

    # ──────────────────────────────────────────────────────────────
    #  FACT TABLE: FACT_ACCIDENTS
    # ──────────────────────────────────────────────────────────────
    print("   📊 Creating FACT_ACCIDENTS...")

    # Merge dimension keys back to create the fact table
    fact = df.copy()
    fact['accident_key'] = range(1, len(fact) + 1)

    # Map time keys
    time_key_map = dim_time.set_index(['Hour', 'Day_of_Week'])['time_key']
    fact['time_key'] = fact.apply(
        lambda r: time_key_map.get((r['Hour'], r['Day_of_Week']), -1), axis=1
    )

    # Map location keys
    loc_key_map = dim_location.set_index('Urban_or_Rural_Area')['location_key']
    fact['location_key'] = fact['Urban_or_Rural_Area'].map(loc_key_map)

    # Map weather keys
    wth_key_map = dim_weather.set_index('Weather_Conditions')['weather_key']
    fact['weather_key'] = fact['Weather_Conditions'].map(wth_key_map)

    # Map road keys
    road_key_map = dim_road.set_index(['Road_Type', 'Road_Surface_Conditions'])['road_key']
    fact['road_key'] = fact.apply(
        lambda r: road_key_map.get((r['Road_Type'], r['Road_Surface_Conditions']), -1), axis=1
    )

    # Select fact table columns (keys + measures)
    fact_accidents = fact[['accident_key', 'time_key', 'location_key',
                           'weather_key', 'road_key', 'Accident_Severity',
                           'Number_of_Vehicles', 'Number_of_Casualties',
                           'Speed_limit']].copy()

    fact_accidents.columns = ['accident_key', 'time_key', 'location_key',
                              'weather_key', 'road_key', 'severity',
                              'num_vehicles', 'num_casualties', 'speed_limit']

    print(f"\n   ✅ Transformation complete!")
    print(f"      DIM_TIME:      {len(dim_time):>6,} rows")
    print(f"      DIM_LOCATION:  {len(dim_location):>6,} rows")
    print(f"      DIM_WEATHER:   {len(dim_weather):>6,} rows")
    print(f"      DIM_ROAD:      {len(dim_road):>6,} rows")
    print(f"      FACT_ACCIDENTS:{len(fact_accidents):>6,} rows")

    return {
        'dim_time': dim_time,
        'dim_location': dim_location,
        'dim_weather': dim_weather,
        'dim_road': dim_road,
        'fact_accidents': fact_accidents
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  PHASE 3: LOAD — Persist to the data warehouse
# ═══════════════════════════════════════════════════════════════════════════════

def load(tables):
    """
    LOAD phase of ETL pipeline.
    Saves all dimension and fact tables to the warehouse directory.

    In a real-world scenario, this would:
      - Write to a data warehouse (Snowflake, Redshift, BigQuery)
      - Update slowly changing dimensions (SCD Type 1/2)
      - Create indexes and partitions for query performance

    Parameters:
        tables (dict): Dictionary of DataFrames to save.
    """
    print(f"\n📤 LOAD: Saving to data warehouse ({WAREHOUSE_DIR})...")

    for name, df in tables.items():
        path = os.path.join(WAREHOUSE_DIR, f'{name}.csv')
        df.to_csv(path, index=False)
        print(f"   💾 {name}.csv ({len(df):,} rows)")

    print(f"   ✅ All tables loaded to warehouse!")


# ═══════════════════════════════════════════════════════════════════════════════
#  OLAP QUERIES — Demonstrating Data Warehouse Operations
# ═══════════════════════════════════════════════════════════════════════════════

def demonstrate_olap_queries(tables):
    """
    Demonstrate common OLAP operations on the star schema.

    OLAP Operations:
      1. SLICE: Select a single dimension value (e.g., only 'Morning' accidents)
      2. DICE: Select multiple dimension values (e.g., Urban + Rainy)
      3. ROLL-UP: Aggregate from fine to coarse grain (hour → time_of_day)
      4. DRILL-DOWN: Disaggregate from coarse to fine (time_of_day → hour)
    """
    fact = tables['fact_accidents']
    dim_time = tables['dim_time']
    dim_weather = tables['dim_weather']
    dim_location = tables['dim_location']

    print("\n" + "═" * 60)
    print("  📊 OLAP QUERY DEMONSTRATIONS")
    print("═" * 60)

    # ── SLICE: Filter by a single dimension ──
    print("\n🔪 SLICE: Morning accidents only")
    morning_keys = dim_time[dim_time['time_of_day'] == 'Morning']['time_key']
    morning_facts = fact[fact['time_key'].isin(morning_keys)]
    print(f"   Total morning accidents: {len(morning_facts):,}")
    print(f"   Average casualties: {morning_facts['num_casualties'].mean():.2f}")

    # ── DICE: Filter by multiple dimensions ──
    print("\n🎲 DICE: Urban + Bad Weather accidents")
    urban_keys = dim_location[dim_location['area_type'] == 'Urban']['location_key']
    bad_weather_keys = dim_weather[dim_weather['is_bad_weather'] == 1]['weather_key']
    dice_facts = fact[
        (fact['location_key'].isin(urban_keys)) &
        (fact['weather_key'].isin(bad_weather_keys))
    ]
    print(f"   Urban bad-weather accidents: {len(dice_facts):,}")
    severity_dist = dice_facts['severity'].value_counts().sort_index()
    for s, c in severity_dist.items():
        print(f"   Severity {s}: {c:,}")

    # ── ROLL-UP: Aggregate from hour to time_of_day ──
    print("\n📈 ROLL-UP: Casualties by Time of Day")
    merged = fact.merge(dim_time[['time_key', 'time_of_day']], on='time_key')
    rollup = merged.groupby('time_of_day').agg(
        total_accidents=('accident_key', 'count'),
        total_casualties=('num_casualties', 'sum'),
        avg_speed=('speed_limit', 'mean')
    ).round(2)
    print(rollup.to_string())

    # ── DRILL-DOWN: From time_of_day to specific hours ──
    print("\n🔍 DRILL-DOWN: Night accidents by hour")
    night_keys = dim_time[dim_time['time_of_day'] == 'Night']['time_key']
    night_merged = fact[fact['time_key'].isin(night_keys)].merge(
        dim_time[['time_key', 'Hour']], on='time_key'
    )
    drill = night_merged.groupby('Hour').agg(
        accidents=('accident_key', 'count'),
        avg_casualties=('num_casualties', 'mean')
    ).round(2)
    print(drill.to_string())


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN ETL PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_etl_pipeline(filepath=None):
    """
    Execute the complete ETL pipeline.

    Parameters:
        filepath (str): Path to source data.

    Returns:
        dict: All warehouse tables.
    """
    print("\n" + "═" * 60)
    print("  🏭 ETL PIPELINE & STAR SCHEMA")
    print("═" * 60)

    # Phase 1: Extract
    raw_data = extract(filepath)

    # Phase 2: Transform
    tables = transform(raw_data)

    # Phase 3: Load
    load(tables)

    # Demonstrate OLAP queries
    demonstrate_olap_queries(tables)

    print("\n" + "═" * 60)
    print("  ✅ ETL PIPELINE COMPLETE!")
    print("═" * 60)

    return tables


if __name__ == "__main__":
    run_etl_pipeline()
