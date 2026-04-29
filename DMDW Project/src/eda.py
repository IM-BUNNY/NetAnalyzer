"""
============================================================================
  EXPLORATORY DATA ANALYSIS (EDA) MODULE
============================================================================
  Purpose:
    Generates comprehensive visualizations to understand patterns in the
    road accident dataset. Saves all plots to the plots/ directory.

  Visualizations:
    1. Accident severity distribution (bar + pie)
    2. Correlation heatmap
    3. Accidents by hour of day
    4. Accidents by day of week
    5. Weather conditions analysis
    6. Road type analysis
    7. Speed limit distribution
    8. Light conditions analysis
    9. Urban vs Rural comparison
   10. Multi-feature severity breakdown
============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
import warnings
warnings.filterwarnings('ignore')

# ─── Setup ───────────────────────────────────────────────────────────────────────
PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'plots')
os.makedirs(PLOTS_DIR, exist_ok=True)

# Style configuration for professional-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
SEVERITY_COLORS = {1: '#e74c3c', 2: '#f39c12', 3: '#2ecc71'}
SEVERITY_LABELS = {1: 'Fatal', 2: 'Serious', 3: 'Slight'}
PALETTE = ['#e74c3c', '#f39c12', '#2ecc71']


def save_plot(fig, filename):
    """Save figure to plots directory."""
    path = os.path.join(PLOTS_DIR, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"   💾 Saved: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 1: Severity Distribution (Bar + Pie)
# ═══════════════════════════════════════════════════════════════════════════════

def plot_severity_distribution(df):
    """Bar chart and pie chart showing accident severity distribution."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Accident Severity Distribution', fontsize=16, fontweight='bold')

    counts = df['Accident_Severity'].value_counts().sort_index()
    labels = [SEVERITY_LABELS[i] for i in counts.index]
    colors = [SEVERITY_COLORS[i] for i in counts.index]

    # Bar chart
    bars = axes[0].bar(labels, counts.values, color=colors, edgecolor='white', linewidth=1.5)
    axes[0].set_ylabel('Number of Accidents', fontsize=12)
    axes[0].set_title('Count by Severity', fontsize=13)
    for bar, val in zip(bars, counts.values):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 200,
                     f'{val:,}', ha='center', fontsize=11, fontweight='bold')

    # Pie chart
    axes[1].pie(counts.values, labels=labels, colors=colors, autopct='%1.1f%%',
                startangle=90, textprops={'fontsize': 12},
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    axes[1].set_title('Proportion by Severity', fontsize=13)

    plt.tight_layout()
    save_plot(fig, '01_severity_distribution.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 2: Correlation Heatmap
# ═══════════════════════════════════════════════════════════════════════════════

def plot_correlation_heatmap(df):
    """Heatmap showing correlations between numerical features."""
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    # Remove ID-like columns
    exclude = ['Latitude', 'Longitude', 'Year', 'Month']
    num_cols = [c for c in num_cols if c not in exclude]

    corr = df[num_cols].corr()

    fig, ax = plt.subplots(figsize=(12, 9))
    mask = np.triu(np.ones_like(corr, dtype=bool))
    sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlBu_r',
                center=0, linewidths=0.5, ax=ax, vmin=-1, vmax=1,
                annot_kws={'size': 9})
    ax.set_title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    save_plot(fig, '02_correlation_heatmap.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 3: Accidents by Hour of Day
# ═══════════════════════════════════════════════════════════════════════════════

def plot_accidents_by_hour(df):
    """Line plot showing accident frequency by hour, colored by severity."""
    if 'Hour' not in df.columns and 'Time' in df.columns:
        df = df.copy()
        df['Hour'] = df['Time'].apply(
            lambda x: int(str(x).split(':')[0]) if pd.notna(x) and ':' in str(x) else 12
        )

    fig, ax = plt.subplots(figsize=(12, 5))

    for sev in sorted(df['Accident_Severity'].unique()):
        subset = df[df['Accident_Severity'] == sev]
        hourly = subset.groupby('Hour').size()
        ax.plot(hourly.index, hourly.values, marker='o', linewidth=2,
                color=SEVERITY_COLORS.get(sev, 'gray'),
                label=SEVERITY_LABELS.get(sev, str(sev)), markersize=5)

    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('Number of Accidents', fontsize=12)
    ax.set_title('Accidents by Hour of Day (by Severity)', fontsize=16, fontweight='bold')
    ax.set_xticks(range(24))
    ax.legend(title='Severity', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    save_plot(fig, '03_accidents_by_hour.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 4: Accidents by Day of Week
# ═══════════════════════════════════════════════════════════════════════════════

def plot_accidents_by_day(df):
    """Grouped bar plot showing accidents by day of week and severity."""
    day_names = {1: 'Sun', 2: 'Mon', 3: 'Tue', 4: 'Wed', 5: 'Thu', 6: 'Fri', 7: 'Sat'}
    fig, ax = plt.subplots(figsize=(10, 5))

    pivot = df.groupby(['Day_of_Week', 'Accident_Severity']).size().unstack(fill_value=0)
    pivot.index = [day_names.get(d, d) for d in pivot.index]
    pivot.columns = [SEVERITY_LABELS.get(c, c) for c in pivot.columns]

    pivot.plot(kind='bar', ax=ax, color=PALETTE, edgecolor='white', linewidth=0.8)
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Number of Accidents', fontsize=12)
    ax.set_title('Accidents by Day of Week', fontsize=16, fontweight='bold')
    ax.legend(title='Severity')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
    plt.tight_layout()
    save_plot(fig, '04_accidents_by_day.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 5: Weather Conditions
# ═══════════════════════════════════════════════════════════════════════════════

def plot_weather_conditions(df):
    """Horizontal bar plot of accidents by weather conditions."""
    fig, ax = plt.subplots(figsize=(12, 6))

    weather_severity = df.groupby(['Weather_Conditions', 'Accident_Severity']).size().unstack(fill_value=0)
    weather_severity.columns = [SEVERITY_LABELS.get(c, c) for c in weather_severity.columns]
    weather_severity = weather_severity.sort_values(weather_severity.columns[-1], ascending=True)

    weather_severity.plot(kind='barh', stacked=True, ax=ax, color=PALETTE, edgecolor='white')
    ax.set_xlabel('Number of Accidents', fontsize=12)
    ax.set_title('Accidents by Weather Conditions', fontsize=16, fontweight='bold')
    ax.legend(title='Severity', loc='lower right')
    plt.tight_layout()
    save_plot(fig, '05_weather_conditions.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 6: Road Type Analysis
# ═══════════════════════════════════════════════════════════════════════════════

def plot_road_type(df):
    """Bar plot of accidents by road type."""
    fig, ax = plt.subplots(figsize=(10, 5))

    road_counts = df['Road_Type'].value_counts()
    colors = sns.color_palette('viridis', len(road_counts))
    bars = ax.bar(range(len(road_counts)), road_counts.values, color=colors, edgecolor='white')
    ax.set_xticks(range(len(road_counts)))
    ax.set_xticklabels(road_counts.index, rotation=30, ha='right')
    ax.set_ylabel('Number of Accidents', fontsize=12)
    ax.set_title('Accidents by Road Type', fontsize=16, fontweight='bold')

    for bar, val in zip(bars, road_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                f'{val:,}', ha='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    save_plot(fig, '06_road_type.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 7: Speed Limit Distribution
# ═══════════════════════════════════════════════════════════════════════════════

def plot_speed_limit(df):
    """Box plot and count plot for speed limit by severity."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Speed Limit Analysis', fontsize=16, fontweight='bold')

    # Box plot
    severity_labels_list = [SEVERITY_LABELS.get(s, s) for s in df['Accident_Severity']]
    sns.boxplot(x=severity_labels_list, y=df['Speed_limit'], ax=axes[0],
                palette=PALETTE, order=['Fatal', 'Serious', 'Slight'])
    axes[0].set_title('Speed Limit by Severity', fontsize=13)
    axes[0].set_ylabel('Speed Limit (mph)')

    # Count plot
    speed_sev = df.groupby(['Speed_limit', 'Accident_Severity']).size().unstack(fill_value=0)
    speed_sev.columns = [SEVERITY_LABELS.get(c, c) for c in speed_sev.columns]
    speed_sev.plot(kind='bar', ax=axes[1], color=PALETTE, edgecolor='white')
    axes[1].set_title('Accident Count by Speed Limit', fontsize=13)
    axes[1].set_ylabel('Count')
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
    axes[1].legend(title='Severity')

    plt.tight_layout()
    save_plot(fig, '07_speed_limit.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 8: Light Conditions
# ═══════════════════════════════════════════════════════════════════════════════

def plot_light_conditions(df):
    """Stacked bar plot showing severity proportions by light conditions."""
    fig, ax = plt.subplots(figsize=(12, 5))

    light_sev = df.groupby(['Light_Conditions', 'Accident_Severity']).size().unstack(fill_value=0)
    # Normalize to proportions
    light_pct = light_sev.div(light_sev.sum(axis=1), axis=0) * 100
    light_pct.columns = [SEVERITY_LABELS.get(c, c) for c in light_pct.columns]

    light_pct.plot(kind='bar', stacked=True, ax=ax, color=PALETTE, edgecolor='white')
    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_title('Severity Proportion by Light Conditions', fontsize=16, fontweight='bold')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=25, ha='right')
    ax.legend(title='Severity', bbox_to_anchor=(1.02, 1))
    ax.set_ylim(0, 100)
    plt.tight_layout()
    save_plot(fig, '08_light_conditions.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 9: Urban vs Rural
# ═══════════════════════════════════════════════════════════════════════════════

def plot_urban_rural(df):
    """Comparison of accident severity in urban vs rural areas."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle('Urban vs Rural Accident Comparison', fontsize=16, fontweight='bold')

    area_map = {1: 'Urban', 2: 'Rural'}
    df_temp = df.copy()
    df_temp['Area'] = df_temp['Urban_or_Rural_Area'].map(area_map)

    # Count by area
    area_counts = df_temp['Area'].value_counts()
    axes[0].pie(area_counts.values, labels=area_counts.index, autopct='%1.1f%%',
                colors=['#3498db', '#e67e22'], textprops={'fontsize': 12},
                wedgeprops={'edgecolor': 'white', 'linewidth': 2})
    axes[0].set_title('Total Accidents by Area', fontsize=13)

    # Severity proportion by area
    area_sev = df_temp.groupby(['Area', 'Accident_Severity']).size().unstack(fill_value=0)
    area_pct = area_sev.div(area_sev.sum(axis=1), axis=0) * 100
    area_pct.columns = [SEVERITY_LABELS.get(c, c) for c in area_pct.columns]
    area_pct.plot(kind='bar', ax=axes[1], color=PALETTE, edgecolor='white')
    axes[1].set_ylabel('Percentage (%)')
    axes[1].set_title('Severity % by Area Type', fontsize=13)
    axes[1].set_xticklabels(axes[1].get_xticklabels(), rotation=0)
    axes[1].legend(title='Severity')

    plt.tight_layout()
    save_plot(fig, '09_urban_rural.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  PLOT 10: Casualties & Vehicles Analysis
# ═══════════════════════════════════════════════════════════════════════════════

def plot_casualties_vehicles(df):
    """Scatter plot and distributions for casualties and vehicles."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('Casualties & Vehicles Analysis', fontsize=16, fontweight='bold')

    for sev in sorted(df['Accident_Severity'].unique()):
        subset = df[df['Accident_Severity'] == sev]
        axes[0].scatter(subset['Number_of_Vehicles'], subset['Number_of_Casualties'],
                        alpha=0.3, color=SEVERITY_COLORS.get(sev, 'gray'),
                        label=SEVERITY_LABELS.get(sev, str(sev)), s=10)
    axes[0].set_xlabel('Number of Vehicles')
    axes[0].set_ylabel('Number of Casualties')
    axes[0].set_title('Vehicles vs Casualties', fontsize=13)
    axes[0].legend(title='Severity')

    # Average casualties by severity
    avg_cas = df.groupby('Accident_Severity')['Number_of_Casualties'].mean()
    labels = [SEVERITY_LABELS.get(s, s) for s in avg_cas.index]
    colors = [SEVERITY_COLORS.get(s, 'gray') for s in avg_cas.index]
    bars = axes[1].bar(labels, avg_cas.values, color=colors, edgecolor='white')
    axes[1].set_ylabel('Avg. Casualties')
    axes[1].set_title('Average Casualties by Severity', fontsize=13)
    for bar, val in zip(bars, avg_cas.values):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                     f'{val:.2f}', ha='center', fontsize=11, fontweight='bold')

    plt.tight_layout()
    save_plot(fig, '10_casualties_vehicles.png')


# ═══════════════════════════════════════════════════════════════════════════════
#  RUN ALL EDA
# ═══════════════════════════════════════════════════════════════════════════════

def run_eda(df=None):
    """Execute all EDA visualizations."""
    print("\n" + "═" * 60)
    print("  📊 EXPLORATORY DATA ANALYSIS")
    print("═" * 60)

    if df is None:
        # Load data
        data_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'road_accidents.csv'
        )
        if not os.path.exists(data_path):
            print("⚠️  Dataset not found. Generating...")
            sys.path.insert(0, os.path.dirname(data_path))
            from generate_dataset import generate_dataset
            df = generate_dataset()
            df.to_csv(data_path, index=False)
        else:
            df = pd.read_csv(data_path)

    # Feature engineering for EDA
    if 'Hour' not in df.columns and 'Time' in df.columns:
        df['Hour'] = df['Time'].apply(
            lambda x: int(str(x).split(':')[0]) if pd.notna(x) and ':' in str(x) else 12
        )

    print(f"\n📈 Generating {10} visualizations...\n")

    plot_severity_distribution(df)
    plot_correlation_heatmap(df)
    plot_accidents_by_hour(df)
    plot_accidents_by_day(df)
    plot_weather_conditions(df)
    plot_road_type(df)
    plot_speed_limit(df)
    plot_light_conditions(df)
    plot_urban_rural(df)
    plot_casualties_vehicles(df)

    print(f"\n✅ All plots saved to: {os.path.abspath(PLOTS_DIR)}")
    return df


if __name__ == "__main__":
    run_eda()
