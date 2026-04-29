"""
============================================================================
  FLASK WEB APPLICATION — Road Accident Severity Prediction
============================================================================
  Backend server with MongoDB integration.
  
  Routes:
    /                   → Dashboard (stats, model comparison, key insights)
    /predict            → Interactive prediction form
    /eda                → EDA visualization gallery
    /warehouse          → Star schema & data warehouse view
    /api/predict        → JSON prediction endpoint
    /api/stats          → Dashboard statistics
    /api/predictions    → Prediction history
============================================================================
"""

import os
import sys
import json
import joblib
import base64
from datetime import datetime

from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
from bson import ObjectId

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# ─── Flask App Setup ─────────────────────────────────────────────────────────
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.secret_key = 'dmdw-road-accident-severity-2026'

# ─── MongoDB Setup ────────────────────────────────────────────────────────────
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = 'road_accident_db'

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    client.server_info()  # Test connection
    db = client[DB_NAME]
    MONGO_CONNECTED = True
    print(f"✅ MongoDB connected: {MONGO_URI}")
except Exception as e:
    db = None
    MONGO_CONNECTED = False
    print(f"⚠️  MongoDB not available: {e}")
    print("   App will run without database persistence.")

# ─── Load Model ──────────────────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model.joblib')
PLOTS_DIR = os.path.join(os.path.dirname(__file__), 'plots')

SEVERITY_MAP = {1: 'Fatal', 2: 'Serious', 3: 'Slight'}
SEVERITY_DESC = {
    1: 'Life-threatening accident — immediate emergency response needed',
    2: 'Significant injuries likely — medical attention required',
    3: 'Minor injuries expected — standard incident handling'
}

model_bundle = None
if os.path.exists(MODEL_PATH):
    model_bundle = joblib.load(MODEL_PATH)
    print(f"✅ Model loaded: {model_bundle['model_name']}")


# ─── Helper: JSON serializer for MongoDB ObjectId ────────────────────────────
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime):
            return o.isoformat()
        return super().default(o)

app.json_encoder = JSONEncoder


# ─── Initialize MongoDB Collections ──────────────────────────────────────────
def init_database():
    """Populate MongoDB with dataset and model results on first run."""
    if not MONGO_CONNECTED:
        return

    # Check if already initialized
    if db.accidents.count_documents({}) > 0:
        print("   📦 Database already initialized")
        return

    print("   📦 Initializing MongoDB collections...")
    import pandas as pd

    # Load raw data
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'road_accidents.csv')
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
        # Insert in batches (only first 10K for performance)
        records = df.head(10000).to_dict('records')
        db.accidents.insert_many(records)
        print(f"   ✅ Loaded {len(records)} accident records")

    # Load warehouse tables
    warehouse_dir = os.path.join(os.path.dirname(__file__), 'data', 'warehouse')
    for table_name in ['dim_time', 'dim_location', 'dim_weather', 'dim_road', 'fact_accidents']:
        path = os.path.join(warehouse_dir, f'{table_name}.csv')
        if os.path.exists(path):
            tdf = pd.read_csv(path)
            if table_name == 'fact_accidents':
                tdf = tdf.head(10000)  # Limit fact table size
            db[table_name].insert_many(tdf.to_dict('records'))
            print(f"   ✅ Loaded {table_name}: {len(tdf)} rows")

    # Store model comparison results
    if model_bundle:
        db.model_results.insert_one({
            'best_model': model_bundle['model_name'],
            'test_accuracy': model_bundle['test_accuracy'],
            'feature_names': model_bundle['feature_names'],
            'created_at': datetime.utcnow(),
            'models': [
                {'name': 'Decision Tree', 'accuracy': 0.7125, 'f1_macro': 0.4605, 'cv_accuracy': 0.6991},
                {'name': 'Random Forest', 'accuracy': 0.7629, 'f1_macro': 0.4559, 'cv_accuracy': 0.8415},
                {'name': 'XGBoost', 'accuracy': 0.8398, 'f1_macro': 0.4230, 'cv_accuracy': 0.9039},
                {'name': 'KNN', 'accuracy': 0.5950, 'f1_macro': 0.3692, 'cv_accuracy': 0.8304},
                {'name': 'Naive Bayes', 'accuracy': 0.3788, 'f1_macro': 0.2718, 'cv_accuracy': 0.4991},
            ]
        })
        print("   ✅ Stored model comparison results")

    # Create indexes for performance
    db.accidents.create_index('Accident_Severity')
    db.accidents.create_index('Weather_Conditions')
    db.predictions.create_index('created_at')
    print("   ✅ Database indexes created")


# ─── Initialize on startup ───────────────────────────────────────────────────
with app.app_context():
    init_database()


# ═══════════════════════════════════════════════════════════════════════════════
#  PAGE ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('dashboard.html')


@app.route('/predict')
def predict_page():
    """Prediction form page."""
    return render_template('predict.html')


@app.route('/eda')
def eda_page():
    """EDA visualization gallery."""
    return render_template('eda.html')


@app.route('/warehouse')
def warehouse_page():
    """Data warehouse / star schema page."""
    return render_template('warehouse.html')


# ═══════════════════════════════════════════════════════════════════════════════
#  API ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """Make a severity prediction from form/JSON data."""
    data = request.get_json() if request.is_json else request.form.to_dict()

    if model_bundle is None:
        return jsonify({'error': 'Model not loaded. Run model_training.py first.'}), 500

    from predict import predict_severity

    try:
        result = predict_severity(
            day_of_week=int(data.get('day_of_week', 2)),
            hour=int(data.get('hour', 14)),
            road_type=data.get('road_type', 'Single carriageway'),
            speed_limit=int(data.get('speed_limit', 30)),
            weather=data.get('weather', 'Fine no high winds'),
            road_surface=data.get('road_surface', 'Dry'),
            light=data.get('light', 'Daylight'),
            num_vehicles=int(data.get('num_vehicles', 2)),
            num_casualties=int(data.get('num_casualties', 1)),
            urban_rural=int(data.get('urban_rural', 1)),
            model_bundle=model_bundle
        )

        # Store prediction in MongoDB
        if MONGO_CONNECTED:
            prediction_record = {
                'input': data,
                'result': result,
                'created_at': datetime.utcnow()
            }
            db.predictions.insert_one(prediction_record)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def api_stats():
    """Get dashboard statistics."""
    stats = {
        'total_records': 50000,
        'severity_distribution': {'Fatal': 982, 'Serious': 7019, 'Slight': 41999},
        'models_trained': 5,
        'best_model': 'XGBoost',
        'best_accuracy': 0.8398,
        'features_used': 13,
        'mongo_connected': MONGO_CONNECTED
    }

    if MONGO_CONNECTED:
        stats['total_records'] = db.accidents.count_documents({})
        stats['total_predictions'] = db.predictions.count_documents({})

        # Get severity counts from DB
        pipeline = [
            {'$group': {'_id': '$Accident_Severity', '_count': {'$sum': 1}}}
        ]
        sev_counts = list(db.accidents.aggregate(pipeline))
        if sev_counts:
            stats['severity_distribution'] = {
                SEVERITY_MAP.get(s['_id'], str(s['_id'])): s['_count']
                for s in sev_counts
            }

    # Model results
    if MONGO_CONNECTED and db.model_results.count_documents({}) > 0:
        model_doc = db.model_results.find_one(sort=[('created_at', -1)])
        if model_doc:
            stats['model_comparison'] = model_doc.get('models', [])
            stats['best_model'] = model_doc.get('best_model', 'XGBoost')
    else:
        stats['model_comparison'] = [
            {'name': 'Decision Tree', 'accuracy': 0.7125, 'f1_macro': 0.4605, 'cv_accuracy': 0.6991},
            {'name': 'Random Forest', 'accuracy': 0.7629, 'f1_macro': 0.4559, 'cv_accuracy': 0.8415},
            {'name': 'XGBoost', 'accuracy': 0.8398, 'f1_macro': 0.4230, 'cv_accuracy': 0.9039},
            {'name': 'KNN', 'accuracy': 0.5950, 'f1_macro': 0.3692, 'cv_accuracy': 0.8304},
            {'name': 'Naive Bayes', 'accuracy': 0.3788, 'f1_macro': 0.2718, 'cv_accuracy': 0.4991},
        ]

    return jsonify(stats)


@app.route('/api/predictions')
def api_predictions():
    """Get prediction history from MongoDB."""
    if not MONGO_CONNECTED:
        return jsonify([])

    predictions = list(
        db.predictions.find({}, {'_id': 0})
        .sort('created_at', -1)
        .limit(20)
    )
    return jsonify(predictions)


@app.route('/api/warehouse/<table_name>')
def api_warehouse(table_name):
    """Get warehouse table data from MongoDB."""
    allowed = ['dim_time', 'dim_location', 'dim_weather', 'dim_road', 'fact_accidents']
    if table_name not in allowed:
        return jsonify({'error': 'Invalid table'}), 400

    if not MONGO_CONNECTED:
        import pandas as pd
        path = os.path.join(os.path.dirname(__file__), 'data', 'warehouse', f'{table_name}.csv')
        if os.path.exists(path):
            df = pd.read_csv(path)
            if table_name == 'fact_accidents':
                df = df.head(100)
            return jsonify(df.to_dict('records'))
        return jsonify([])

    limit = 100 if table_name == 'fact_accidents' else 0
    cursor = db[table_name].find({}, {'_id': 0})
    if limit:
        cursor = cursor.limit(limit)
    return jsonify(list(cursor))


@app.route('/api/eda/plots')
def api_eda_plots():
    """Get list of available EDA plots as base64 encoded images."""
    plots = []
    if os.path.exists(PLOTS_DIR):
        for fname in sorted(os.listdir(PLOTS_DIR)):
            if fname.endswith('.png'):
                filepath = os.path.join(PLOTS_DIR, fname)
                with open(filepath, 'rb') as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                # Create readable title from filename
                title = fname.replace('.png', '').split('_', 1)[-1].replace('_', ' ').title()
                plots.append({
                    'filename': fname,
                    'title': title,
                    'data': f'data:image/png;base64,{b64}'
                })
    return jsonify(plots)


@app.route('/plots/<path:filename>')
def serve_plot(filename):
    """Serve plot images directly."""
    return send_from_directory(PLOTS_DIR, filename)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n" + "═" * 60)
    print("  🚦 Road Accident Severity Prediction")
    print("  🌐 Web Application Starting...")
    print("═" * 60)
    print(f"  📡 MongoDB: {'Connected ✅' if MONGO_CONNECTED else 'Not available ⚠️'}")
    print(f"  🤖 Model:   {model_bundle['model_name'] if model_bundle else 'Not loaded ⚠️'}")
    print(f"  🌐 URL:     http://localhost:5050")
    print("═" * 60 + "\n")
    app.run(debug=True, port=5050, host='0.0.0.0')
