"""
============================================================================
  MODEL TRAINING MODULE
============================================================================
  Purpose:
    Trains multiple classification models for accident severity prediction.
    Implements K-Fold Cross Validation and saves the best model.

  Models:
    1. Decision Tree Classifier
    2. Random Forest Classifier
    3. Gradient Boosting (XGBoost)
    4. K-Nearest Neighbors (KNN)
    5. Gaussian Naive Bayes

  Output:
    - Trained model objects
    - Cross-validation results
    - Best model saved to models/ directory
============================================================================
"""

import numpy as np
import pandas as pd
import os
import sys
import joblib
import time
import warnings
warnings.filterwarnings('ignore')

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import cross_val_score, StratifiedKFold
from xgboost import XGBClassifier

# ─── Setup ───────────────────────────────────────────────────────────────────────
MODELS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
os.makedirs(MODELS_DIR, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MODEL DEFINITIONS
# ═══════════════════════════════════════════════════════════════════════════════

def get_models():
    """
    Define and return all classification models with tuned hyperparameters.

    Returns:
        dict: Model name → (model instance, description)
    """
    models = {
        'Decision Tree': (
            DecisionTreeClassifier(
                max_depth=10,           # Limit depth to prevent overfitting
                min_samples_split=20,   # Minimum samples to split a node
                min_samples_leaf=10,    # Minimum samples in a leaf
                class_weight='balanced',# Handle imbalanced classes
                random_state=42
            ),
            "A tree-based model that splits data based on feature thresholds. "
            "Simple, interpretable, but prone to overfitting."
        ),
        'Random Forest': (
            RandomForestClassifier(
                n_estimators=200,       # Number of trees in the forest
                max_depth=15,           # Maximum tree depth
                min_samples_split=10,
                min_samples_leaf=5,
                class_weight='balanced',
                n_jobs=-1,              # Use all CPU cores
                random_state=42
            ),
            "Ensemble of decision trees using bagging. Reduces overfitting "
            "and improves generalization over single trees."
        ),
        'XGBoost': (
            XGBClassifier(
                n_estimators=200,       # Number of boosting rounds
                max_depth=8,            # Maximum tree depth
                learning_rate=0.1,      # Step size shrinkage
                subsample=0.8,          # Fraction of samples per tree
                colsample_bytree=0.8,   # Fraction of features per tree
                reg_alpha=0.1,          # L1 regularization
                reg_lambda=1.0,         # L2 regularization
                use_label_encoder=False,
                eval_metric='mlogloss', # Multi-class log loss
                random_state=42,
                verbosity=0
            ),
            "Gradient boosting algorithm that builds trees sequentially, "
            "each correcting errors of the previous. State-of-the-art performance."
        ),
        'KNN': (
            KNeighborsClassifier(
                n_neighbors=7,          # Number of neighbors to consider
                weights='distance',     # Weight by inverse distance
                metric='minkowski',     # Distance metric
                n_jobs=-1
            ),
            "Classifies based on majority vote of K nearest neighbors. "
            "Simple but effective; performance depends on feature scaling."
        ),
        'Naive Bayes': (
            GaussianNB(
                var_smoothing=1e-9      # Smoothing parameter
            ),
            "Probabilistic classifier based on Bayes' theorem with "
            "independence assumption. Fast and works well with small datasets."
        )
    }
    return models


# ═══════════════════════════════════════════════════════════════════════════════
#  K-FOLD CROSS VALIDATION
# ═══════════════════════════════════════════════════════════════════════════════

def cross_validate_models(X_train, y_train, models=None, k_folds=5):
    """
    Perform Stratified K-Fold Cross Validation on all models.

    Stratified K-Fold ensures each fold has approximately the same
    proportion of each class, which is crucial for imbalanced datasets.

    Parameters:
        X_train: Training features
        y_train: Training labels
        models (dict): Model definitions
        k_folds (int): Number of folds

    Returns:
        pd.DataFrame: Cross-validation results for each model
    """
    if models is None:
        models = get_models()

    print(f"\n📊 Performing {k_folds}-Fold Stratified Cross Validation...")
    print("─" * 55)

    cv = StratifiedKFold(n_splits=k_folds, shuffle=True, random_state=42)
    cv_results = []

    for name, (model, desc) in models.items():
        start = time.time()
        # XGBoost requires 0-indexed labels (0, 1, 2) instead of (1, 2, 3)
        y_cv = y_train - 1 if name == 'XGBoost' else y_train
        scores = cross_val_score(model, X_train, y_cv, cv=cv,
                                 scoring='accuracy', n_jobs=-1)
        elapsed = time.time() - start

        result = {
            'Model': name,
            'Mean Accuracy': scores.mean(),
            'Std Accuracy': scores.std(),
            'Min Accuracy': scores.min(),
            'Max Accuracy': scores.max(),
            'Time (s)': round(elapsed, 2)
        }
        cv_results.append(result)

        print(f"   {name:>15s}: {scores.mean():.4f} (±{scores.std():.4f})  [{elapsed:.1f}s]")

    cv_df = pd.DataFrame(cv_results).sort_values('Mean Accuracy', ascending=False)
    print("─" * 55)
    print(f"   🏆 Best CV: {cv_df.iloc[0]['Model']} ({cv_df.iloc[0]['Mean Accuracy']:.4f})")

    return cv_df


# ═══════════════════════════════════════════════════════════════════════════════
#  TRAIN ALL MODELS
# ═══════════════════════════════════════════════════════════════════════════════

def train_all_models(X_train, y_train, X_test, y_test, models=None):
    """
    Train all models on the full training set and evaluate on test set.

    Parameters:
        X_train, y_train: Training data
        X_test, y_test: Test data
        models (dict): Model definitions

    Returns:
        dict: Trained model objects keyed by name
    """
    if models is None:
        models = get_models()

    print(f"\n🏋️  Training {len(models)} models on full training set...")
    print("─" * 55)

    trained_models = {}

    for name, (model, desc) in models.items():
        start = time.time()

        # For XGBoost, adjust labels to start from 0
        if name == 'XGBoost':
            y_tr = y_train - 1  # XGBoost expects 0-indexed labels
            model.fit(X_train, y_tr)
        else:
            model.fit(X_train, y_train)

        elapsed = time.time() - start

        # Calculate training and test accuracy
        if name == 'XGBoost':
            train_acc = (model.predict(X_train) == y_tr).mean()
            test_acc = (model.predict(X_test) == (y_test - 1)).mean()
        else:
            train_acc = model.score(X_train, y_train)
            test_acc = model.score(X_test, y_test)

        trained_models[name] = model

        print(f"   {name:>15s}: Train={train_acc:.4f}  Test={test_acc:.4f}  [{elapsed:.1f}s]")

    print("─" * 55)
    return trained_models


# ═══════════════════════════════════════════════════════════════════════════════
#  SAVE BEST MODEL
# ═══════════════════════════════════════════════════════════════════════════════

def save_best_model(trained_models, X_test, y_test, scaler=None, encoders=None,
                    feature_names=None):
    """
    Identify and save the best model along with preprocessing artifacts.

    Parameters:
        trained_models (dict): Trained model objects
        X_test, y_test: Test data for evaluation
        scaler: Fitted StandardScaler
        encoders: Fitted LabelEncoders
        feature_names: List of feature column names

    Returns:
        str: Name of the best model
    """
    print(f"\n💾 Saving best model...")

    # Find best model by test accuracy
    best_name = None
    best_acc = 0

    for name, model in trained_models.items():
        if name == 'XGBoost':
            acc = (model.predict(X_test) == (y_test - 1)).mean()
        else:
            acc = model.score(X_test, y_test)
        if acc > best_acc:
            best_acc = acc
            best_name = name

    best_model = trained_models[best_name]

    # Save model and preprocessing artifacts as a bundle
    model_bundle = {
        'model': best_model,
        'model_name': best_name,
        'scaler': scaler,
        'encoders': encoders,
        'feature_names': feature_names,
        'test_accuracy': best_acc
    }

    model_path = os.path.join(MODELS_DIR, 'best_model.joblib')
    joblib.dump(model_bundle, model_path)
    print(f"   🏆 Best Model: {best_name} (Accuracy: {best_acc:.4f})")
    print(f"   📁 Saved to: {model_path}")

    # Also save all models individually
    for name, model in trained_models.items():
        path = os.path.join(MODELS_DIR, f'{name.lower().replace(" ", "_")}.joblib')
        joblib.dump(model, path)

    print(f"   ✅ All {len(trained_models)} models saved to: {os.path.abspath(MODELS_DIR)}")
    return best_name


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN TRAINING PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_training(preprocessed_data):
    """
    Execute the full training pipeline.

    Parameters:
        preprocessed_data (dict): Output from preprocess_pipeline()

    Returns:
        dict: Training results including models and CV scores
    """
    print("\n" + "═" * 60)
    print("  🤖 MODEL TRAINING PIPELINE")
    print("═" * 60)

    X_train = preprocessed_data['X_train']
    X_test = preprocessed_data['X_test']
    y_train = preprocessed_data['y_train']
    y_test = preprocessed_data['y_test']

    # Step 1: Define models
    models = get_models()

    # Step 2: Cross validation
    cv_results = cross_validate_models(X_train, y_train, models)

    # Step 3: Train on full training set
    trained_models = train_all_models(X_train, y_train, X_test, y_test, models)

    # Step 4: Save best model
    best_name = save_best_model(
        trained_models, X_test, y_test,
        scaler=preprocessed_data.get('scaler'),
        encoders=preprocessed_data.get('encoders'),
        feature_names=preprocessed_data.get('feature_names')
    )

    return {
        'trained_models': trained_models,
        'cv_results': cv_results,
        'best_model_name': best_name
    }


if __name__ == "__main__":
    # Import preprocessing module
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_preprocessing import preprocess_pipeline

    preprocessed = preprocess_pipeline()
    results = run_training(preprocessed)

    print("\n📊 Cross-Validation Results:")
    print(results['cv_results'].to_string(index=False))
