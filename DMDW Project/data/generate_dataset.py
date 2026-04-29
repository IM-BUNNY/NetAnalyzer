"""
============================================================================
  SYNTHETIC UK ROAD ACCIDENT DATASET GENERATOR
============================================================================
  Purpose:
    Generates a realistic synthetic dataset modeled after the UK Department
    for Transport (DfT) road accident dataset. This allows the project to
    run without requiring a Kaggle download.

  Note:
    For the real dataset, visit:
    https://www.kaggle.com/datasets/silicon99/dft-accident-data
    Download 'Accidents0515.csv' and place it in the data/ folder.

  Output:
    data/road_accidents.csv — ~50,000 synthetic accident records
============================================================================
"""

import numpy as np
import pandas as pd
import os

# ─── Configuration ──────────────────────────────────────────────────────────────
np.random.seed(42)
N_RECORDS = 50000  # Number of synthetic accident records to generate

# ─── Define Feature Distributions ───────────────────────────────────────────────
# These distributions are modeled to approximate real-world UK accident patterns.

# Accident Severity: 1 = Fatal, 2 = Serious, 3 = Slight
# In reality, ~80% of reported accidents are "Slight"
SEVERITY_PROBS = {1: 0.02, 2: 0.14, 3: 0.84}

# Day of Week: 1=Sunday, 2=Monday, ..., 7=Saturday
DAY_OF_WEEK_PROBS = {
    1: 0.12, 2: 0.14, 3: 0.15, 4: 0.15,
    5: 0.15, 6: 0.16, 7: 0.13
}

# Road Type
ROAD_TYPES = {
    'Single carriageway': 0.60,
    'Dual carriageway': 0.18,
    'Roundabout': 0.10,
    'One way street': 0.05,
    'Slip road': 0.04,
    'Unknown': 0.03
}

# Speed Limits (mph)
SPEED_LIMITS = {20: 0.05, 30: 0.55, 40: 0.10, 50: 0.08, 60: 0.15, 70: 0.07}

# Weather Conditions
WEATHER_CONDITIONS = {
    'Fine no high winds': 0.65,
    'Raining no high winds': 0.15,
    'Fine + high winds': 0.05,
    'Raining + high winds': 0.04,
    'Snowing no high winds': 0.03,
    'Fog or mist': 0.03,
    'Other': 0.03,
    'Unknown': 0.02
}

# Road Surface Conditions
ROAD_SURFACE = {
    'Dry': 0.60,
    'Wet or damp': 0.30,
    'Snow': 0.03,
    'Frost or ice': 0.04,
    'Flood over 3cm deep': 0.01,
    'Oil or diesel': 0.01,
    'Mud': 0.01
}

# Light Conditions
LIGHT_CONDITIONS = {
    'Daylight': 0.65,
    'Darkness - lights lit': 0.20,
    'Darkness - lights unlit': 0.05,
    'Darkness - no lighting': 0.07,
    'Darkness - lighting unknown': 0.03
}

# Urban or Rural Area
URBAN_RURAL = {1: 0.65, 2: 0.35}  # 1 = Urban, 2 = Rural


def weighted_choice(choices_dict, size):
    """
    Draw random samples from a weighted distribution.

    Parameters:
        choices_dict (dict): Keys are choices, values are probabilities.
        size (int): Number of samples to draw.

    Returns:
        np.ndarray: Array of sampled choices.
    """
    keys = list(choices_dict.keys())
    probs = list(choices_dict.values())
    # Normalize probabilities to ensure they sum to 1.0
    probs = np.array(probs) / np.sum(probs)
    return np.random.choice(keys, size=size, p=probs)


def generate_time(n):
    """
    Generate random accident times (HH:MM format).
    Distribution is skewed towards rush hours (8-9 AM, 5-7 PM).

    Parameters:
        n (int): Number of time values to generate.

    Returns:
        list: List of time strings in 'HH:MM' format.
    """
    # Hour distribution weights — higher during rush hours
    hour_weights = np.array([
        2, 1, 1, 1, 1, 2,     # 00:00 - 05:00 (late night / early morning)
        4, 7, 10, 7, 6, 7,    # 06:00 - 11:00 (morning rush)
        8, 7, 7, 8, 9, 10,    # 12:00 - 17:00 (afternoon rush)
        9, 7, 5, 4, 3, 2      # 18:00 - 23:00 (evening)
    ], dtype=float)
    hour_weights /= hour_weights.sum()

    hours = np.random.choice(range(24), size=n, p=hour_weights)
    minutes = np.random.randint(0, 60, size=n)

    return [f"{h:02d}:{m:02d}" for h, m in zip(hours, minutes)]


def add_severity_correlations(df):
    """
    Introduce realistic correlations between features and accident severity.

    In real data, fatal accidents correlate with:
      - Higher speed limits
      - Rural areas
      - Poor weather / darkness
      - Fewer vehicles but more casualties

    Parameters:
        df (pd.DataFrame): The generated dataset.

    Returns:
        pd.DataFrame: Dataset with adjusted severity correlations.
    """
    # Fatal accidents (severity=1) more likely at high speeds
    fatal_mask = df['Accident_Severity'] == 1
    serious_mask = df['Accident_Severity'] == 2

    # Increase speed limits for fatal accidents
    high_speed_idx = df[fatal_mask].sample(frac=0.4, random_state=42).index
    df.loc[high_speed_idx, 'Speed_limit'] = np.random.choice([60, 70], size=len(high_speed_idx))

    # Fatal accidents more likely in rural areas
    rural_idx = df[fatal_mask].sample(frac=0.5, random_state=42).index
    df.loc[rural_idx, 'Urban_or_Rural_Area'] = 2

    # Increase casualties for fatal/serious accidents
    df.loc[fatal_mask, 'Number_of_Casualties'] = np.random.choice(
        range(1, 6), size=fatal_mask.sum(), p=[0.3, 0.3, 0.2, 0.1, 0.1]
    )
    df.loc[serious_mask, 'Number_of_Casualties'] = np.random.choice(
        range(1, 4), size=serious_mask.sum(), p=[0.5, 0.3, 0.2]
    )

    # More darkness for serious/fatal
    dark_idx = df[fatal_mask].sample(frac=0.35, random_state=42).index
    df.loc[dark_idx, 'Light_Conditions'] = np.random.choice(
        ['Darkness - lights lit', 'Darkness - lights unlit', 'Darkness - no lighting'],
        size=len(dark_idx), p=[0.5, 0.2, 0.3]
    )

    return df


def introduce_missing_values(df, frac=0.02):
    """
    Introduce realistic missing values into the dataset.
    In real-world data, some fields are often missing.

    Parameters:
        df (pd.DataFrame): Clean dataset.
        frac (float): Fraction of values to set as missing.

    Returns:
        pd.DataFrame: Dataset with NaN values introduced.
    """
    columns_with_missing = ['Weather_Conditions', 'Road_Surface_Conditions',
                            'Light_Conditions', 'Road_Type']

    for col in columns_with_missing:
        mask = np.random.random(len(df)) < frac
        df.loc[mask, col] = np.nan

    return df


def generate_dataset():
    """
    Main function to generate the complete synthetic dataset.

    Returns:
        pd.DataFrame: Complete synthetic road accident dataset.
    """
    print("🔧 Generating synthetic UK Road Accident dataset...")
    print(f"   Records: {N_RECORDS:,}")

    # ── Step 1: Generate independent features ────────────────────────────────
    data = {
        'Accident_Severity': weighted_choice(SEVERITY_PROBS, N_RECORDS).astype(int),
        'Day_of_Week': weighted_choice(DAY_OF_WEEK_PROBS, N_RECORDS).astype(int),
        'Time': generate_time(N_RECORDS),
        'Road_Type': weighted_choice(ROAD_TYPES, N_RECORDS),
        'Speed_limit': weighted_choice(SPEED_LIMITS, N_RECORDS).astype(int),
        'Weather_Conditions': weighted_choice(WEATHER_CONDITIONS, N_RECORDS),
        'Road_Surface_Conditions': weighted_choice(ROAD_SURFACE, N_RECORDS),
        'Light_Conditions': weighted_choice(LIGHT_CONDITIONS, N_RECORDS),
        'Number_of_Vehicles': np.random.choice(
            range(1, 6), size=N_RECORDS, p=[0.30, 0.50, 0.12, 0.05, 0.03]
        ),
        'Number_of_Casualties': np.random.choice(
            range(1, 5), size=N_RECORDS, p=[0.65, 0.20, 0.10, 0.05]
        ),
        'Urban_or_Rural_Area': weighted_choice(URBAN_RURAL, N_RECORDS).astype(int),
    }

    df = pd.DataFrame(data)

    # ── Step 2: Add Accident_Index (unique ID) ───────────────────────────────
    df.insert(0, 'Accident_Index', [f"ACC{i:06d}" for i in range(1, N_RECORDS + 1)])

    # ── Step 3: Add year and month for time-series analysis ──────────────────
    df['Year'] = np.random.choice(range(2005, 2016), size=N_RECORDS)
    df['Month'] = np.random.choice(range(1, 13), size=N_RECORDS)

    # ── Step 4: Add latitude/longitude (approximate UK coordinates) ──────────
    df['Latitude'] = np.round(np.random.uniform(50.0, 56.0, N_RECORDS), 6)
    df['Longitude'] = np.round(np.random.uniform(-5.0, 2.0, N_RECORDS), 6)

    # ── Step 5: Introduce realistic correlations ─────────────────────────────
    df = add_severity_correlations(df)

    # ── Step 6: Introduce missing values (simulating real-world data) ────────
    df = introduce_missing_values(df, frac=0.02)

    # ── Step 7: Shuffle the dataset ──────────────────────────────────────────
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    print(f"✅ Dataset generated: {df.shape[0]:,} records, {df.shape[1]} columns")
    print(f"\n📊 Severity Distribution:")
    severity_map = {1: 'Fatal', 2: 'Serious', 3: 'Slight'}
    for sev, count in df['Accident_Severity'].value_counts().sort_index().items():
        pct = count / len(df) * 100
        print(f"   {severity_map[sev]:>8s} (Severity {sev}): {count:>6,} ({pct:.1f}%)")

    return df


# ─── Main Execution ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    df = generate_dataset()

    # Save to CSV
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "road_accidents.csv")
    df.to_csv(output_path, index=False)

    print(f"\n💾 Dataset saved to: {output_path}")
    print(f"\n📋 Column Summary:")
    print(df.dtypes.to_string())
    print(f"\n🔍 Missing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0].to_string())
    print(f"\n📐 Sample Records:")
    print(df.head(3).to_string())
