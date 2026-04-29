# 🚦 Road Accident Severity Prediction

## DMDW (Data Mining & Data Warehousing) Project

An end-to-end machine learning pipeline for predicting the severity of road accidents using the UK Road Accident dataset.

---

## 📁 Project Structure

```
DMDW Project/
├── data/
│   ├── generate_dataset.py         # Synthetic dataset generator
│   ├── road_accidents.csv          # Generated dataset (50K records)
│   └── warehouse/                  # Star schema tables (ETL output)
│       ├── dim_time.csv
│       ├── dim_location.csv
│       ├── dim_weather.csv
│       ├── dim_road.csv
│       └── fact_accidents.csv
├── src/
│   ├── data_preprocessing.py       # Data cleaning & transformation
│   ├── eda.py                      # Exploratory Data Analysis
│   ├── model_training.py           # ML model training & CV
│   ├── evaluation.py               # Model evaluation & metrics
│   ├── predict.py                  # Prediction interface
│   └── star_schema_etl.py          # Data warehouse ETL pipeline
├── models/                         # Saved trained models (.joblib)
├── plots/                          # Generated visualization plots
├── Road_Accident_Severity_Prediction.ipynb  # Master Jupyter Notebook
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate dataset
python data/generate_dataset.py

# 3. Run the full pipeline
python -c "
import sys; sys.path.insert(0, 'src')
from data_preprocessing import preprocess_pipeline
from eda import run_eda
from model_training import run_training
from evaluation import run_evaluation
from star_schema_etl import run_etl_pipeline

data = preprocess_pipeline()
run_eda(data['raw_df'])
results = run_training(data)
run_evaluation(results['trained_models'], data['X_test'], data['y_test'],
               data['feature_names'], results['cv_results'])
run_etl_pipeline()
"

# 4. Interactive prediction
python src/predict.py
```

## 📊 Models Implemented

| Model | Type | Key Advantage |
|-------|------|---------------|
| Decision Tree | Tree-based | Interpretable, simple |
| Random Forest | Ensemble (Bagging) | Reduces overfitting |
| XGBoost | Ensemble (Boosting) | State-of-the-art accuracy |
| KNN | Distance-based | Non-parametric |
| Naive Bayes | Probabilistic | Fast, works with small data |

## 🎯 Target Variable

- **1 = Fatal** (life-threatening)
- **2 = Serious** (significant injuries)
- **3 = Slight** (minor injuries)

## 📦 Dataset

Synthetic dataset modeled after the **UK DfT Road Accident Dataset**.
For real data: https://www.kaggle.com/datasets/silicon99/dft-accident-data
