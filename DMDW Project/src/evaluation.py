"""
============================================================================
  MODEL EVALUATION MODULE
============================================================================
  Purpose:
    Comprehensive evaluation of all trained models using multiple metrics.
    Generates detailed reports and visualizations.

  Metrics:
    - Accuracy, Precision, Recall, F1-Score
    - Confusion Matrix
    - ROC-AUC Curve (multi-class, One-vs-Rest)
    - Feature Importance plots
    - Final comparison table

  Output:
    - Evaluation plots saved to plots/ directory
    - Comparison table printed and returned
============================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_curve, auc
)
from sklearn.preprocessing import label_binarize

# ─── Setup ───────────────────────────────────────────────────────────────────────
PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plots')
os.makedirs(PLOTS_DIR, exist_ok=True)

SEVERITY_LABELS = {1: 'Fatal', 2: 'Serious', 3: 'Slight'}
PALETTE = ['#e74c3c', '#f39c12', '#2ecc71']


def save_plot(fig, filename):
    path = os.path.join(PLOTS_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"   💾 Saved: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
#  METRICS COMPUTATION
# ═══════════════════════════════════════════════════════════════════════════════

def compute_metrics(y_true, y_pred, model_name="Model"):
    """
    Compute classification metrics for a single model.

    Parameters:
        y_true: True labels
        y_pred: Predicted labels
        model_name: Name for display

    Returns:
        dict: Dictionary of computed metrics
    """
    metrics = {
        'Model': model_name,
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision (macro)': precision_score(y_true, y_pred, average='macro', zero_division=0),
        'Recall (macro)': recall_score(y_true, y_pred, average='macro', zero_division=0),
        'F1-Score (macro)': f1_score(y_true, y_pred, average='macro', zero_division=0),
        'Precision (weighted)': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'Recall (weighted)': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'F1-Score (weighted)': f1_score(y_true, y_pred, average='weighted', zero_division=0),
    }
    return metrics


# ═══════════════════════════════════════════════════════════════════════════════
#  CONFUSION MATRIX
# ═══════════════════════════════════════════════════════════════════════════════

def plot_confusion_matrices(trained_models, X_test, y_test):
    """
    Plot confusion matrices for all models in a grid layout.
    """
    n_models = len(trained_models)
    cols = 3
    rows = (n_models + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(6*cols, 5*rows))
    fig.suptitle('Confusion Matrices — All Models', fontsize=18, fontweight='bold', y=1.02)

    axes_flat = axes.flatten() if n_models > 1 else [axes]
    classes = sorted(y_test.unique())
    class_labels = [SEVERITY_LABELS.get(c, str(c)) for c in classes]

    for idx, (name, model) in enumerate(trained_models.items()):
        ax = axes_flat[idx]

        if name == 'XGBoost':
            y_pred = model.predict(X_test) + 1
        else:
            y_pred = model.predict(X_test)

        cm = confusion_matrix(y_test, y_pred, labels=classes)

        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax,
                    xticklabels=class_labels, yticklabels=class_labels,
                    linewidths=0.5)
        ax.set_xlabel('Predicted')
        ax.set_ylabel('Actual')
        ax.set_title(name, fontsize=13, fontweight='bold')

    # Hide empty subplots
    for idx in range(n_models, len(axes_flat)):
        axes_flat[idx].set_visible(False)

    plt.tight_layout()
    save_plot(fig, '11_confusion_matrices.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  ROC-AUC CURVES (Multi-class, One-vs-Rest)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_roc_curves(trained_models, X_test, y_test):
    """
    Plot ROC curves for each model using One-vs-Rest strategy.
    Multi-class ROC is computed by binarizing the output.
    """
    classes = sorted(y_test.unique())
    n_classes = len(classes)
    y_test_bin = label_binarize(y_test, classes=classes)

    fig, axes = plt.subplots(1, len(trained_models), figsize=(6*len(trained_models), 5))
    fig.suptitle('ROC-AUC Curves (One-vs-Rest)', fontsize=18, fontweight='bold')

    if len(trained_models) == 1:
        axes = [axes]

    colors = ['#e74c3c', '#f39c12', '#2ecc71']

    for idx, (name, model) in enumerate(trained_models.items()):
        ax = axes[idx]

        # Get probability predictions
        try:
            if name == 'XGBoost':
                y_proba = model.predict_proba(X_test)
            else:
                y_proba = model.predict_proba(X_test)
        except AttributeError:
            ax.text(0.5, 0.5, 'No probability\nestimates available',
                    ha='center', va='center', fontsize=12)
            ax.set_title(name)
            continue

        # Compute ROC for each class
        for i, cls in enumerate(classes):
            fpr, tpr, _ = roc_curve(y_test_bin[:, i], y_proba[:, i])
            roc_auc = auc(fpr, tpr)
            ax.plot(fpr, tpr, color=colors[i % len(colors)], linewidth=2,
                    label=f'{SEVERITY_LABELS.get(cls, cls)} (AUC={roc_auc:.3f})')

        ax.plot([0, 1], [0, 1], 'k--', alpha=0.5, linewidth=1)
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title(name, fontsize=13, fontweight='bold')
        ax.legend(fontsize=9, loc='lower right')
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1.05])

    plt.tight_layout()
    save_plot(fig, '12_roc_curves.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  FEATURE IMPORTANCE
# ═══════════════════════════════════════════════════════════════════════════════

def plot_feature_importance(trained_models, feature_names):
    """
    Plot feature importance for tree-based models.
    Only applicable to Decision Tree, Random Forest, and XGBoost.
    """
    tree_models = {k: v for k, v in trained_models.items()
                   if k in ['Decision Tree', 'Random Forest', 'XGBoost']}

    if not tree_models:
        print("   ⚠️  No tree-based models found for feature importance.")
        return

    fig, axes = plt.subplots(1, len(tree_models), figsize=(7*len(tree_models), 6))
    fig.suptitle('Feature Importance Comparison', fontsize=18, fontweight='bold')

    if len(tree_models) == 1:
        axes = [axes]

    for idx, (name, model) in enumerate(tree_models.items()):
        ax = axes[idx]
        importances = model.feature_importances_

        # Sort by importance
        sorted_idx = np.argsort(importances)
        sorted_features = [feature_names[i] for i in sorted_idx]
        sorted_importances = importances[sorted_idx]

        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(sorted_features)))
        ax.barh(range(len(sorted_features)), sorted_importances,
                color=colors, edgecolor='white', linewidth=0.5)
        ax.set_yticks(range(len(sorted_features)))
        ax.set_yticklabels(sorted_features, fontsize=9)
        ax.set_xlabel('Importance', fontsize=11)
        ax.set_title(name, fontsize=13, fontweight='bold')

    plt.tight_layout()
    save_plot(fig, '13_feature_importance.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  MODEL COMPARISON TABLE
# ═══════════════════════════════════════════════════════════════════════════════

def generate_comparison_table(trained_models, X_test, y_test, cv_results=None):
    """
    Generate a comprehensive comparison table of all models.

    Returns:
        pd.DataFrame: Comparison table with all metrics
    """
    all_metrics = []

    for name, model in trained_models.items():
        if name == 'XGBoost':
            y_pred = model.predict(X_test) + 1
        else:
            y_pred = model.predict(X_test)

        metrics = compute_metrics(y_test, y_pred, name)

        # Add CV results if available
        if cv_results is not None:
            cv_row = cv_results[cv_results['Model'] == name]
            if len(cv_row) > 0:
                metrics['CV Accuracy (mean)'] = cv_row.iloc[0]['Mean Accuracy']
                metrics['CV Accuracy (std)'] = cv_row.iloc[0]['Std Accuracy']

        all_metrics.append(metrics)

    comparison_df = pd.DataFrame(all_metrics)
    comparison_df = comparison_df.sort_values('F1-Score (macro)', ascending=False)

    return comparison_df


def plot_comparison_chart(comparison_df):
    """Visualize model comparison as a grouped bar chart."""
    fig, ax = plt.subplots(figsize=(12, 6))

    metrics_to_plot = ['Accuracy', 'Precision (macro)', 'Recall (macro)', 'F1-Score (macro)']
    x = np.arange(len(comparison_df))
    width = 0.2
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#9b59b6']

    for i, metric in enumerate(metrics_to_plot):
        if metric in comparison_df.columns:
            bars = ax.bar(x + i*width, comparison_df[metric].values,
                         width, label=metric, color=colors[i], edgecolor='white')

    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(comparison_df['Model'].values, fontsize=11)
    ax.set_ylabel('Score', fontsize=12)
    ax.set_title('Model Performance Comparison', fontsize=16, fontweight='bold')
    ax.legend(fontsize=10, loc='lower right')
    ax.set_ylim(0, 1.1)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    save_plot(fig, '14_model_comparison.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN EVALUATION PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_evaluation(trained_models, X_test, y_test, feature_names, cv_results=None):
    """
    Execute the complete evaluation pipeline.

    Parameters:
        trained_models (dict): Trained model objects
        X_test, y_test: Test data
        feature_names (list): Feature column names
        cv_results (pd.DataFrame): Cross-validation results

    Returns:
        pd.DataFrame: Final comparison table
    """
    print("\n" + "═" * 60)
    print("  📈 MODEL EVALUATION PIPELINE")
    print("═" * 60)

    # Step 1: Classification reports
    print("\n📋 Detailed Classification Reports:")
    for name, model in trained_models.items():
        if name == 'XGBoost':
            y_pred = model.predict(X_test) + 1
        else:
            y_pred = model.predict(X_test)

        print(f"\n{'─'*45}")
        print(f"   {name}")
        print(f"{'─'*45}")
        target_names = [SEVERITY_LABELS.get(c, str(c)) for c in sorted(y_test.unique())]
        print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))

    # Step 2: Confusion matrices
    print("\n📊 Generating confusion matrices...")
    plot_confusion_matrices(trained_models, X_test, y_test)

    # Step 3: ROC curves
    print("\n📊 Generating ROC-AUC curves...")
    plot_roc_curves(trained_models, X_test, y_test)

    # Step 4: Feature importance
    print("\n📊 Generating feature importance plots...")
    plot_feature_importance(trained_models, feature_names)

    # Step 5: Comparison table
    print("\n📊 Generating model comparison...")
    comparison_df = generate_comparison_table(trained_models, X_test, y_test, cv_results)
    plot_comparison_chart(comparison_df)

    # Print final table
    print("\n" + "═" * 80)
    print("  🏆 FINAL MODEL COMPARISON TABLE")
    print("═" * 80)
    display_cols = ['Model', 'Accuracy', 'Precision (macro)', 'Recall (macro)',
                    'F1-Score (macro)']
    if 'CV Accuracy (mean)' in comparison_df.columns:
        display_cols.append('CV Accuracy (mean)')
    print(comparison_df[display_cols].to_string(index=False, float_format='%.4f'))

    best = comparison_df.iloc[0]
    print(f"\n   🏆 Best Model: {best['Model']} (F1-Score: {best['F1-Score (macro)']:.4f})")

    return comparison_df


if __name__ == "__main__":
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from data_preprocessing import preprocess_pipeline
    from model_training import run_training

    preprocessed = preprocess_pipeline()
    training_results = run_training(preprocessed)

    comparison = run_evaluation(
        trained_models=training_results['trained_models'],
        X_test=preprocessed['X_test'],
        y_test=preprocessed['y_test'],
        feature_names=preprocessed['feature_names'],
        cv_results=training_results['cv_results']
    )
