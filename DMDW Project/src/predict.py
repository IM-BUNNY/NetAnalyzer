"""
============================================================================
  PREDICTION MODULE
============================================================================
  Purpose:
    Provides a simple interface to make predictions using the trained model.
    Loads the saved model bundle and handles all preprocessing automatically.

  Usage:
    python predict.py
    (Interactive mode — prompts user for input values)

    Or import and use programmatically:
      from predict import predict_severity
      result = predict_severity(day=3, hour=14, road_type='Single carriageway', ...)
============================================================================
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# ─── Setup ───────────────────────────────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
MODEL_PATH = os.path.join(MODELS_DIR, 'best_model.joblib')

SEVERITY_MAP = {1: 'Fatal', 2: 'Serious', 3: 'Slight'}
SEVERITY_DESC = {
    1: '⚠️  FATAL — Life-threatening accident expected',
    2: '🟠 SERIOUS — Significant injuries likely',
    3: '🟢 SLIGHT — Minor injuries expected'
}


def load_model():
    """
    Load the saved model bundle (model + scaler + encoders).

    Returns:
        dict: Model bundle with all preprocessing components.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}.\n"
            f"Please run model_training.py first to train and save the model."
        )

    bundle = joblib.load(MODEL_PATH)
    print(f"✅ Loaded model: {bundle['model_name']} "
          f"(Test Accuracy: {bundle['test_accuracy']:.4f})")
    return bundle


def predict_severity(day_of_week=2, hour=14, road_type='Single carriageway',
                     speed_limit=30, weather='Fine no high winds',
                     road_surface='Dry', light='Daylight',
                     num_vehicles=2, num_casualties=1,
                     urban_rural=1, model_bundle=None):
    """
    Predict accident severity given input features.

    Parameters:
        day_of_week (int): 1=Sunday, 2=Monday, ..., 7=Saturday
        hour (int): Hour of day (0-23)
        road_type (str): Type of road
        speed_limit (int): Speed limit in mph
        weather (str): Weather conditions
        road_surface (str): Road surface conditions
        light (str): Light conditions
        num_vehicles (int): Number of vehicles involved
        num_casualties (int): Number of casualties
        urban_rural (int): 1=Urban, 2=Rural
        model_bundle (dict): Pre-loaded model bundle (optional)

    Returns:
        dict: Prediction result with severity and probability
    """
    # Load model if not provided
    if model_bundle is None:
        model_bundle = load_model()

    model = model_bundle['model']
    scaler = model_bundle['scaler']
    encoders = model_bundle['encoders']
    feature_names = model_bundle['feature_names']
    model_name = model_bundle['model_name']

    # ── Build input feature vector ──
    # Derived features
    is_weekend = 1 if day_of_week in [1, 7] else 0
    is_dark = 1 if 'Darkness' in str(light) else 0
    bad_weather_terms = ['Raining', 'Snowing', 'Fog', 'high winds']
    is_bad_weather = 1 if any(w in str(weather) for w in bad_weather_terms) else 0

    # Encode categorical features
    cat_values = {
        'Road_Type': road_type,
        'Weather_Conditions': weather,
        'Road_Surface_Conditions': road_surface,
        'Light_Conditions': light
    }

    encoded_cats = {}
    for col, val in cat_values.items():
        if col in encoders:
            le = encoders[col]
            if val in le.classes_:
                encoded_cats[col] = le.transform([val])[0]
            else:
                encoded_cats[col] = -1  # Unknown category
        else:
            encoded_cats[col] = 0

    # Build feature dictionary
    feature_dict = {
        'Road_Type': encoded_cats.get('Road_Type', 0),
        'Weather_Conditions': encoded_cats.get('Weather_Conditions', 0),
        'Road_Surface_Conditions': encoded_cats.get('Road_Surface_Conditions', 0),
        'Light_Conditions': encoded_cats.get('Light_Conditions', 0),
        'Day_of_Week': day_of_week,
        'Hour': hour,
        'Speed_limit': speed_limit,
        'Number_of_Vehicles': num_vehicles,
        'Number_of_Casualties': num_casualties,
        'Urban_or_Rural_Area': urban_rural,
        'Is_Weekend': is_weekend,
        'Is_Dark': is_dark,
        'Is_Bad_Weather': is_bad_weather,
    }

    # Create DataFrame with correct feature order
    input_df = pd.DataFrame([{f: feature_dict.get(f, 0) for f in feature_names}])

    # Scale numerical features
    if scaler is not None:
        num_cols = ['Day_of_Week', 'Hour', 'Speed_limit', 'Number_of_Vehicles',
                    'Number_of_Casualties', 'Urban_or_Rural_Area']
        cols_to_scale = [c for c in num_cols if c in input_df.columns]
        input_df[cols_to_scale] = scaler.transform(input_df[cols_to_scale])

    # Make prediction
    prediction = model.predict(input_df)[0]

    # Adjust for XGBoost (0-indexed labels)
    if model_name == 'XGBoost':
        prediction = prediction + 1

    # Get probability if available
    try:
        probabilities = model.predict_proba(input_df)[0]
        if model_name == 'XGBoost':
            prob_dict = {str(i+1): float(round(p, 4)) for i, p in enumerate(probabilities)}
        else:
            classes = model.classes_
            prob_dict = {str(int(c)): float(round(p, 4)) for c, p in zip(classes, probabilities)}
    except AttributeError:
        prob_dict = {}

    result = {
        'predicted_severity': int(prediction),
        'severity_label': SEVERITY_MAP.get(int(prediction), 'Unknown'),
        'description': SEVERITY_DESC.get(int(prediction), ''),
        'probabilities': prob_dict,
        'model_used': model_name
    }

    return result


def interactive_prediction():
    """Run an interactive prediction session with user input."""
    print("\n" + "═" * 60)
    print("  🔮 ROAD ACCIDENT SEVERITY PREDICTOR")
    print("═" * 60)

    bundle = load_model()

    while True:
        print("\n📝 Enter accident details (or 'quit' to exit):\n")

        try:
            day = input("   Day of Week (1=Sun, 2=Mon, ..., 7=Sat) [2]: ").strip()
            if day.lower() == 'quit':
                break
            day = int(day) if day else 2

            hour = input("   Hour of Day (0-23) [14]: ").strip()
            hour = int(hour) if hour else 14

            print("\n   Road Types: Single carriageway, Dual carriageway, Roundabout,")
            print("               One way street, Slip road")
            road = input("   Road Type [Single carriageway]: ").strip()
            road = road if road else 'Single carriageway'

            speed = input("   Speed Limit (mph) [30]: ").strip()
            speed = int(speed) if speed else 30

            print("\n   Weather: Fine no high winds, Raining no high winds,")
            print("           Snowing no high winds, Fog or mist, etc.")
            weather = input("   Weather Conditions [Fine no high winds]: ").strip()
            weather = weather if weather else 'Fine no high winds'

            print("\n   Road Surface: Dry, Wet or damp, Snow, Frost or ice")
            surface = input("   Road Surface [Dry]: ").strip()
            surface = surface if surface else 'Dry'

            print("\n   Light: Daylight, Darkness - lights lit, Darkness - no lighting")
            light = input("   Light Conditions [Daylight]: ").strip()
            light = light if light else 'Daylight'

            vehicles = input("   Number of Vehicles [2]: ").strip()
            vehicles = int(vehicles) if vehicles else 2

            casualties = input("   Number of Casualties [1]: ").strip()
            casualties = int(casualties) if casualties else 1

            area = input("   Area (1=Urban, 2=Rural) [1]: ").strip()
            area = int(area) if area else 1

        except (ValueError, EOFError):
            print("   ⚠️  Invalid input. Using defaults.")
            day, hour, road, speed = 2, 14, 'Single carriageway', 30
            weather, surface, light = 'Fine no high winds', 'Dry', 'Daylight'
            vehicles, casualties, area = 2, 1, 1

        # Make prediction
        result = predict_severity(
            day_of_week=day, hour=hour, road_type=road,
            speed_limit=speed, weather=weather, road_surface=surface,
            light=light, num_vehicles=vehicles, num_casualties=casualties,
            urban_rural=area, model_bundle=bundle
        )

        # Display result
        print("\n" + "─" * 45)
        print(f"   🎯 PREDICTION RESULT")
        print("─" * 45)
        print(f"   Severity: {result['severity_label']} (Class {result['predicted_severity']})")
        print(f"   {result['description']}")
        if result['probabilities']:
            print(f"\n   📊 Class Probabilities:")
            for cls, prob in sorted(result['probabilities'].items()):
                bar = '█' * int(prob * 30)
                print(f"      {SEVERITY_MAP.get(cls, cls):>8s}: {prob:.4f} {bar}")
        print(f"\n   🤖 Model: {result['model_used']}")
        print("─" * 45)


if __name__ == "__main__":
    interactive_prediction()
