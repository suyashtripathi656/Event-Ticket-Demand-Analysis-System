import pandas as pd
import numpy as np
import warnings
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor

warnings.filterwarnings('ignore')

# 1. Load the Dataset
# Use a path relative to this script's directory for portability
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(BASE_DIR, 'output', 'master_combined_dataset.csv')

df = pd.read_csv(file_path)

# Handle missing values
df['performer2Id'] = df['performer2Id'].fillna('None')
df['performer2_name'] = df['performer2_name'].fillna('No Second Performer')
df['performer2_performer_score'] = df['performer2_performer_score'].fillna(0)
df['performer2_performer_popularity'] = df['performer2_performer_popularity'].fillna(0)
df['performer2_divisionName'] = df['performer2_divisionName'].fillna('No Division')
df['performer2_divisionShortName'] = df['performer2_divisionShortName'].fillna('None')
df['performer2_has_home_venue'] = df['performer2_has_home_venue'].fillna(False)
df = df.dropna(subset=['capacity'])

# Drop Unnecessary Columns
cols_to_drop = [
    'eventId', 'venueId', 'performerIds', 'performer1Id', 'performer2Id', 
    'url', 'event_name', 'shortName', 'datetimeUtc', 'taxonomySubName', 
    'addressPostalCode', 'status'
]
df_cleaned = df.drop(columns=[col for col in cols_to_drop if col in df.columns]).copy()

# 2. Demand Score Engineering
df_cleaned['log_p1_pop'] = np.log1p(df_cleaned['performer1_performer_popularity'])
df_cleaned['log_p2_pop'] = np.log1p(df_cleaned['performer2_performer_popularity'])
df_cleaned['log_v_pop'] = np.log1p(df_cleaned['venue_popularity'])

base_score = (
    (df_cleaned['log_p1_pop'] * 0.35) + 
    (df_cleaned['log_p2_pop'] * 0.15) + 
    (df_cleaned['log_v_pop'] * 0.25)
)

multiplier = np.ones(len(df_cleaned))
multiplier = np.where(df_cleaned['is_playoff'] == 1, multiplier * 1.5, multiplier)
multiplier = np.where(df_cleaned['is_weekend'] == 1, multiplier * 1.1, multiplier)

raw_demand = base_score * multiplier
scaler = MinMaxScaler(feature_range=(0, 100))
df_cleaned['Demand_Score'] = scaler.fit_transform(raw_demand.values.reshape(-1, 1))

def assign_demand_level(score):
    if score >= 66: return 'High Demand'
    elif score >= 33: return 'Medium Demand'
    else: return 'Low Demand'
df_cleaned['Demand_Level'] = df_cleaned['Demand_Score'].apply(assign_demand_level)
df_cleaned = df_cleaned.drop(columns=['log_p1_pop', 'log_p2_pop', 'log_v_pop'])

# 3. Feature Engineering
df_cleaned['total_performer_score'] = df_cleaned['performer1_performer_score'] + df_cleaned['performer2_performer_score']
df_cleaned['pop_to_capacity_ratio'] = df_cleaned['performer1_performer_popularity'] / (df_cleaned['capacity'] + 1)
df_cleaned['is_prime_time'] = ((df_cleaned['is_weekend'] == 1) & (df_cleaned['is_evening'] == 1)).astype(int)

# 4. Feature Selection
leakage_cols = [
    'performer1_performer_popularity', 'performer2_performer_popularity', 
    'venue_popularity', 'venue_score', 'performer1_performer_popularity_level',
    'performer2_performer_popularity_level', 'venue_popularity_level'
]

ml_df = df_cleaned.drop(columns=[c for c in leakage_cols if c in df_cleaned.columns])

# We need to save the distinct categories for the prediction system
# so we can rebuild the exact same one-hot encoded structure.
cat_cols = ml_df.select_dtypes(include=['object', 'bool']).columns.tolist()
if 'Demand_Level' in cat_cols:
    cat_cols.remove('Demand_Level')

ml_df_encoded = pd.get_dummies(ml_df, columns=cat_cols, drop_first=True)

X = ml_df_encoded.drop(columns=['Demand_Score', 'Demand_Level'])
y = ml_df_encoded['Demand_Score']
X = X.fillna(0)

# We use the top 30 features as done in the notebook
rf_selector = RandomForestRegressor(n_estimators=50, random_state=42, n_jobs=1)
rf_selector.fit(X, y)

importance_df = pd.DataFrame({'Feature': X.columns, 'Importance': rf_selector.feature_importances_})
importance_df = importance_df.sort_values(by='Importance', ascending=False)
top_features = importance_df['Feature'].head(30).tolist()
X_selected = X[top_features]

# 5. Train Final Model
print("Training final model...")
final_model = RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=1)
final_model.fit(X_selected, y)
print("Model trained successfully.")

# 6. Save Model, Preprocessor Data, and Demand Scaler
output_dir = os.path.join(BASE_DIR, 'output')
os.makedirs(output_dir, exist_ok=True)
joblib.dump(final_model, os.path.join(output_dir, 'trained_model.pkl'))
joblib.dump(scaler, os.path.join(output_dir, 'demand_scaler.pkl'))

preprocessor_data = {
    'features': top_features,
    'cat_cols': cat_cols,
    'dummy_columns': list(X.columns),
    'importance_df': importance_df.head(10).to_dict('records'),
}
joblib.dump(preprocessor_data, os.path.join(output_dir, 'preprocessor.pkl'))
print(f"Model, scaler, and preprocessor saved to {output_dir}/")
