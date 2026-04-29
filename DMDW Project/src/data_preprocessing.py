"""
============================================================================
  DATA PREPROCESSING MODULE
============================================================================
  Purpose:
    Handles all data cleaning, transformation, and preparation steps
    required before model training. This module implements:
      1. Loading and initial inspection of the dataset
      2. Missing value imputation
      3. Feature engineering (extracting hour from time, etc.)
      4. Categorical variable encoding (Label Encoding)
      5. Numerical feature normalization (StandardScaler)
      6. Handling class imbalance using SMOTE
      7. Train-test split

  Input:  data/road_accidents.csv
  Output: Preprocessed feature matrices (X_train, X_test, y_train, y_test)
============================================================================
"""

import pandas as pd
import numpy as np
import os
import sys
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

# ─── Constants ───────────────────────────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
RAW_DATA_PATH = os.path.join(DATA_DIR, 'road_accidents.csv')

# Severity mapping for display purposes
SEVERITY_MAP = {1: 'Fatal', 2: 'Serious', 3: 'Slight'}

# Features to use for modeling
CATEGORICAL_FEATURES = [
    'Road_Type', 'Weather_Conditions', 'Road_Surface_Conditions',
    'Light_Conditions'
]
NUMERICAL_FEATURES = [
    'Day_of_Week', 'Hour', 'Speed_limit', 'Number_of_Vehicles',
    'Number_of_Casualties', 'Urban_or_Rural_Area'
]
TARGET = 'Accident_Severity'


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 1: DATA LOADING
# ═════════════════════════════════════════════════════════════════════════════════

def load_data(filepath=None):
    """
    Load the road accident dataset from CSV file.

    Parameters:
        filepath (str): Path to the CSV file. Defaults to RAW_DATA_PATH.

    Returns:
        pd.DataFrame: Raw accident dataset.
    """
    if filepath is None:
        filepath = RAW_DATA_PATH

    if not os.path.exists(filepath):
        print(f"⚠️  Dataset not found at: {filepath}")
        print("   Running dataset generator...")
        # Generate the synthetic dataset if it doesn't exist
        sys.path.insert(0, DATA_DIR)
        from generate_dataset import generate_dataset
        df = generate_dataset()
        df.to_csv(filepath, index=False)
        print(f"   ✅ Generated and saved to {filepath}")
    else:
        df = pd.read_csv(filepath)
        print(f"✅ Dataset loaded: {df.shape[0]:,} records, {df.shape[1]} columns")

    return df


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 2: INITIAL DATA INSPECTION
# ═════════════════════════════════════════════════════════════════════════════════

def inspect_data(df):
    """
    Perform initial data inspection to understand the dataset structure,
    data types, missing values, and basic statistics.

    Parameters:
        df (pd.DataFrame): The raw dataset.

    Returns:
        dict: Dictionary containing inspection results.
    """
    print("\n" + "=" * 60)
    print("  📋 DATA INSPECTION REPORT")
    print("=" * 60)

    # Shape
    print(f"\n📐 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    # Data types
    print(f"\n📊 Data Types:")
    for dtype, count in df.dtypes.value_counts().items():
        print(f"   {dtype}: {count} columns")

    # Missing values
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct})
    missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values(
        'Missing Count', ascending=False
    )

    if len(missing_df) > 0:
        print(f"\n⚠️  Missing Values:")
        for col, row in missing_df.iterrows():
            print(f"   {col:>30s}: {int(row['Missing Count']):>5,} ({row['Missing %']:.2f}%)")
    else:
        print(f"\n✅ No missing values found!")

    # Target distribution
    print(f"\n🎯 Target Variable Distribution (Accident_Severity):")
    for sev, count in df[TARGET].value_counts().sort_index().items():
        pct = count / len(df) * 100
        bar = '█' * int(pct / 2)
        print(f"   {SEVERITY_MAP.get(sev, sev):>8s} ({sev}): {count:>6,} ({pct:5.1f}%) {bar}")

    inspection_results = {
        'shape': df.shape,
        'dtypes': df.dtypes,
        'missing': missing_df,
        'target_dist': df[TARGET].value_counts()
    }

    return inspection_results


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 3: FEATURE ENGINEERING
# ═════════════════════════════════════════════════════════════════════════════════

def engineer_features(df):
    """
    Create new features from existing ones to improve model performance.

    Transformations:
      - Extract 'Hour' from 'Time' column (HH:MM → integer hour)
      - Create 'Is_Weekend' flag from Day_of_Week
      - Create 'Is_Dark' flag from Light_Conditions
      - Create 'Is_Bad_Weather' flag from Weather_Conditions

    Parameters:
        df (pd.DataFrame): Dataset with raw features.

    Returns:
        pd.DataFrame: Dataset with engineered features added.
    """
    df = df.copy()

    # Extract hour from Time column (handles 'HH:MM' format)
    if 'Time' in df.columns:
        df['Hour'] = df['Time'].apply(
            lambda x: int(str(x).split(':')[0]) if pd.notna(x) and ':' in str(x) else 12
        )
        print("   ✅ Extracted 'Hour' from 'Time'")

    # Weekend flag: Sunday (1) and Saturday (7) are weekends
    if 'Day_of_Week' in df.columns:
        df['Is_Weekend'] = df['Day_of_Week'].apply(lambda x: 1 if x in [1, 7] else 0)
        print("   ✅ Created 'Is_Weekend' flag")

    # Darkness flag
    if 'Light_Conditions' in df.columns:
        df['Is_Dark'] = df['Light_Conditions'].apply(
            lambda x: 1 if pd.notna(x) and 'Darkness' in str(x) else 0
        )
        print("   ✅ Created 'Is_Dark' flag")

    # Bad weather flag
    if 'Weather_Conditions' in df.columns:
        bad_weather = ['Raining', 'Snowing', 'Fog', 'high winds']
        df['Is_Bad_Weather'] = df['Weather_Conditions'].apply(
            lambda x: 1 if pd.notna(x) and any(w in str(x) for w in bad_weather) else 0
        )
        print("   ✅ Created 'Is_Bad_Weather' flag")

    return df


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 4: HANDLE MISSING VALUES
# ═════════════════════════════════════════════════════════════════════════════════

def handle_missing_values(df):
    """
    Handle missing values using appropriate strategies:
      - Categorical features: Fill with mode (most frequent value)
      - Numerical features: Fill with median

    This approach is chosen because:
      - Mode imputation preserves the most common pattern for categorical data
      - Median imputation is robust to outliers for numerical data

    Parameters:
        df (pd.DataFrame): Dataset with potential missing values.

    Returns:
        pd.DataFrame: Dataset with missing values imputed.
    """
    df = df.copy()
    initial_missing = df.isnull().sum().sum()

    # Impute categorical features with mode
    for col in CATEGORICAL_FEATURES:
        if col in df.columns and df[col].isnull().any():
            mode_val = df[col].mode()[0]
            n_missing = df[col].isnull().sum()
            df[col].fillna(mode_val, inplace=True)
            print(f"   📌 {col}: Filled {n_missing} missing → '{mode_val}' (mode)")

    # Impute numerical features with median
    for col in NUMERICAL_FEATURES:
        if col in df.columns and df[col].isnull().any():
            median_val = df[col].median()
            n_missing = df[col].isnull().sum()
            df[col].fillna(median_val, inplace=True)
            print(f"   📌 {col}: Filled {n_missing} missing → {median_val} (median)")

    final_missing = df.isnull().sum().sum()
    print(f"\n   ✅ Missing values: {initial_missing} → {final_missing}")

    return df


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 5: ENCODE CATEGORICAL VARIABLES
# ═════════════════════════════════════════════════════════════════════════════════

def encode_categorical(df, encoders=None):
    """
    Encode categorical variables using Label Encoding.

    Label Encoding is used here instead of One-Hot Encoding because:
      - Tree-based models (Decision Tree, Random Forest, XGBoost) handle
        label-encoded features well
      - Reduces dimensionality compared to One-Hot Encoding
      - Simplifies the feature space for faster training

    Parameters:
        df (pd.DataFrame): Dataset with categorical columns.
        encoders (dict): Pre-fitted encoders (for transforming new data).

    Returns:
        tuple: (encoded DataFrame, dictionary of fitted LabelEncoders)
    """
    df = df.copy()
    if encoders is None:
        encoders = {}
        fit_new = True
    else:
        fit_new = False

    for col in CATEGORICAL_FEATURES:
        if col in df.columns:
            if fit_new:
                le = LabelEncoder()
                # Add 'Unknown' to handle unseen categories during prediction
                unique_vals = df[col].dropna().unique().tolist()
                le.fit(unique_vals)
                encoders[col] = le

            df[col] = df[col].apply(
                lambda x: encoders[col].transform([x])[0]
                if x in encoders[col].classes_ else -1
            )
            print(f"   🔢 {col}: Encoded ({len(encoders[col].classes_)} categories)")

    return df, encoders


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 6: SCALE NUMERICAL FEATURES
# ═════════════════════════════════════════════════════════════════════════════════

def scale_features(X_train, X_test, numerical_cols=None):
    """
    Standardize numerical features using StandardScaler (z-score normalization).

    StandardScaler transforms features to have mean=0 and std=1:
      z = (x - mean) / std

    This is important because:
      - Prevents features with larger scales from dominating
      - Improves convergence for gradient-based algorithms
      - Required for distance-based algorithms (KNN)

    Parameters:
        X_train (pd.DataFrame): Training features.
        X_test (pd.DataFrame): Test features.
        numerical_cols (list): Columns to scale.

    Returns:
        tuple: (scaled X_train, scaled X_test, fitted StandardScaler)
    """
    if numerical_cols is None:
        numerical_cols = NUMERICAL_FEATURES

    # Only scale columns that exist in the dataframe
    cols_to_scale = [c for c in numerical_cols if c in X_train.columns]

    scaler = StandardScaler()
    X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
    X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

    print(f"   📏 Scaled {len(cols_to_scale)} numerical features (StandardScaler)")

    return X_train, X_test, scaler


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 7: HANDLE CLASS IMBALANCE (SMOTE)
# ═════════════════════════════════════════════════════════════════════════════════

def apply_smote(X_train, y_train):
    """
    Apply SMOTE (Synthetic Minority Over-sampling Technique) to balance classes.

    SMOTE works by:
      1. Selecting a minority class sample
      2. Finding its k nearest neighbors (default k=5)
      3. Creating a synthetic sample along the line between the sample
         and one of its neighbors

    This is preferred over simple oversampling because:
      - Creates NEW synthetic samples rather than duplicating existing ones
      - Reduces overfitting risk compared to random oversampling
      - Helps the model learn better decision boundaries for minority classes

    Parameters:
        X_train (pd.DataFrame or np.ndarray): Training features.
        y_train (pd.Series or np.ndarray): Training labels.

    Returns:
        tuple: (resampled X_train, resampled y_train)
    """
    print(f"\n   📊 Class distribution BEFORE SMOTE:")
    for cls, count in pd.Series(y_train).value_counts().sort_index().items():
        pct = count / len(y_train) * 100
        print(f"      {SEVERITY_MAP.get(cls, cls):>8s} ({cls}): {count:>6,} ({pct:.1f}%)")

    smote = SMOTE(random_state=42, k_neighbors=5)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

    print(f"\n   📊 Class distribution AFTER SMOTE:")
    for cls, count in pd.Series(y_resampled).value_counts().sort_index().items():
        pct = count / len(y_resampled) * 100
        print(f"      {SEVERITY_MAP.get(cls, cls):>8s} ({cls}): {count:>6,} ({pct:.1f}%)")

    print(f"\n   ✅ Dataset size: {len(X_train):,} → {len(X_resampled):,} samples")

    return X_resampled, y_resampled


# ═════════════════════════════════════════════════════════════════════════════════
#  STEP 8: COMPLETE PREPROCESSING PIPELINE
# ═════════════════════════════════════════════════════════════════════════════════

def preprocess_pipeline(filepath=None, test_size=0.2, apply_smote_flag=True):
    """
    Execute the complete preprocessing pipeline.

    Pipeline Steps:
      1. Load data
      2. Inspect data
      3. Engineer features
      4. Handle missing values
      5. Encode categorical variables
      6. Select features for modeling
      7. Split into train/test sets
      8. Scale numerical features
      9. Apply SMOTE (optional)

    Parameters:
        filepath (str): Path to the CSV file.
        test_size (float): Proportion of data for testing (default: 0.2).
        apply_smote_flag (bool): Whether to apply SMOTE oversampling.

    Returns:
        dict: Dictionary containing all preprocessed components.
    """
    print("\n" + "═" * 60)
    print("  🔧 DATA PREPROCESSING PIPELINE")
    print("═" * 60)

    # Step 1: Load data
    print("\n📦 Step 1: Loading data...")
    df = load_data(filepath)

    # Step 2: Inspect data
    print("\n🔍 Step 2: Inspecting data...")
    inspection = inspect_data(df)

    # Step 3: Feature engineering
    print("\n⚙️  Step 3: Engineering features...")
    df = engineer_features(df)

    # Step 4: Handle missing values
    print("\n🩹 Step 4: Handling missing values...")
    df = handle_missing_values(df)

    # Step 5: Encode categorical variables
    print("\n🔤 Step 5: Encoding categorical variables...")
    df, encoders = encode_categorical(df)

    # Step 6: Select features for modeling
    print("\n🎯 Step 6: Selecting features...")
    all_features = CATEGORICAL_FEATURES + NUMERICAL_FEATURES + [
        'Is_Weekend', 'Is_Dark', 'Is_Bad_Weather'
    ]
    feature_cols = [col for col in all_features if col in df.columns]
    X = df[feature_cols].copy()
    y = df[TARGET].copy()
    print(f"   Selected {len(feature_cols)} features: {feature_cols}")

    # Step 7: Train-test split
    print(f"\n✂️  Step 7: Splitting data (test_size={test_size})...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42, stratify=y
    )
    print(f"   Training set: {X_train.shape[0]:,} samples")
    print(f"   Test set:     {X_test.shape[0]:,} samples")

    # Step 8: Scale features
    print(f"\n📏 Step 8: Scaling features...")
    X_train, X_test, scaler = scale_features(X_train.copy(), X_test.copy())

    # Step 9: Apply SMOTE
    if apply_smote_flag:
        print(f"\n⚖️  Step 9: Applying SMOTE for class balance...")
        X_train_smote, y_train_smote = apply_smote(X_train, y_train)
    else:
        X_train_smote, y_train_smote = X_train, y_train
        print(f"\n⏭️  Step 9: SMOTE skipped")

    print("\n" + "═" * 60)
    print("  ✅ PREPROCESSING COMPLETE!")
    print("═" * 60)

    # Return all components needed for downstream tasks
    return {
        'X_train': X_train_smote,
        'X_test': X_test,
        'y_train': y_train_smote,
        'y_test': y_test,
        'X_train_original': X_train,  # Before SMOTE
        'y_train_original': y_train,  # Before SMOTE
        'feature_names': feature_cols,
        'encoders': encoders,
        'scaler': scaler,
        'raw_df': df,
        'inspection': inspection
    }


# ─── Main Execution ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = preprocess_pipeline()

    print(f"\n📋 Final Training Data Shape: {result['X_train'].shape}")
    print(f"📋 Final Test Data Shape:     {result['X_test'].shape}")
    print(f"📋 Features Used: {result['feature_names']}")
