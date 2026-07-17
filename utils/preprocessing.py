"""
preprocessing.py — Smart Auto-Fill & Feature Engineering
IBM AI Event Demand Analysis System

Handles intelligent feature retrieval from the dataset and
prepares model-ready input vectors.
"""

import pandas as pd
import numpy as np
import os
import joblib
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_dataset(file_path=None):
    """Loads, cleans, and returns the master dataset with engineered Demand Score."""
    if file_path is None:
        file_path = os.path.join(BASE_DIR, 'output', 'master_combined_dataset.csv')
    df = pd.read_csv(file_path)

    # --- Data Cleaning (mirrors training pipeline) ---
    df['performer2Id'] = df['performer2Id'].fillna('None')
    df['performer2_name'] = df['performer2_name'].fillna('No Second Performer')
    df['performer2_performer_score'] = df['performer2_performer_score'].fillna(0)
    df['performer2_performer_popularity'] = df['performer2_performer_popularity'].fillna(0)
    df['performer2_divisionName'] = df['performer2_divisionName'].fillna('No Division')
    df['performer2_divisionShortName'] = df['performer2_divisionShortName'].fillna('None')
    df['performer2_has_home_venue'] = df['performer2_has_home_venue'].fillna(0).astype(int)
    df = df.dropna(subset=['capacity'])

    # --- Engineer Demand Score (same formula as training) ---
    df['log_p1_pop'] = np.log1p(df['performer1_performer_popularity'])
    df['log_p2_pop'] = np.log1p(df['performer2_performer_popularity'])
    df['log_v_pop'] = np.log1p(df['venue_popularity'])

    base_score = (
        (df['log_p1_pop'] * 0.35) +
        (df['log_p2_pop'] * 0.15) +
        (df['log_v_pop'] * 0.25)
    )
    multiplier = np.ones(len(df))
    multiplier = np.where(df['is_playoff'] == 1, multiplier * 1.5, multiplier)
    multiplier = np.where(df['is_weekend'] == 1, multiplier * 1.1, multiplier)

    raw_demand = base_score * multiplier

    # Load the saved scaler for consistency with training, fallback to fresh fit
    scaler_path = os.path.join(BASE_DIR, 'output', 'demand_scaler.pkl')
    if os.path.exists(scaler_path):
        scaler = joblib.load(scaler_path)
        df['Demand_Score'] = scaler.transform(raw_demand.values.reshape(-1, 1))
    else:
        scaler = MinMaxScaler(feature_range=(0, 100))
        df['Demand_Score'] = scaler.fit_transform(raw_demand.values.reshape(-1, 1))

    def _level(s):
        if s >= 66:
            return 'High Demand'
        elif s >= 33:
            return 'Medium Demand'
        return 'Low Demand'
    df['Demand_Level'] = df['Demand_Score'].apply(_level)

    # Engineered features
    df['total_performer_score'] = df['performer1_performer_score'] + df['performer2_performer_score']
    df['pop_to_capacity_ratio'] = df['performer1_performer_popularity'] / (df['capacity'] + 1)
    df['is_prime_time'] = ((df['is_weekend'] == 1) & (df['is_evening'] == 1)).astype(int)

    # Drop temp columns
    df = df.drop(columns=['log_p1_pop', 'log_p2_pop', 'log_v_pop'], errors='ignore')

    return df


def get_unique_options(df):
    """Returns sorted unique values for all dropdown selectors."""
    return {
        'categories': sorted(df['sport_type'].dropna().unique().tolist()),
        'venues': sorted(df['venue_name'].dropna().unique().tolist()),
        'performers_p1': sorted(df['performer1_name'].dropna().unique().tolist()),
        'performers_p2': sorted(
            ['No Second Performer'] +
            [p for p in df['performer2_name'].dropna().unique().tolist() if p != 'No Second Performer']
        ),
    }


def smart_autofill(category, venue, performer1, performer2, event_date, event_time, is_playoff, df):
    """
    SMART AUTO-FILL: Given only 7 natural user inputs, retrieves all remaining
    features from the master dataset automatically.

    Returns:
        features_dict: Complete feature dictionary ready for model input
        display_dict: Human-readable dictionary for UI display
    """
    # --- Lookup venue attributes ---
    venue_rows = df[df['venue_name'] == venue]
    if not venue_rows.empty:
        vr = venue_rows.iloc[0]
        v_capacity = int(vr['capacity'])
        v_cap_level = vr['capacity_level']
        v_score = float(vr['venue_score'])
        v_popularity = int(vr['venue_popularity'])
        v_pop_level = vr['venue_popularity_level']
        v_city = vr['city']
        v_state = vr['state']
        v_isGa = bool(vr['isGa'])
        v_seatSel = bool(vr['seatSelectionEnabled'])
    else:
        v_capacity, v_cap_level = 20000, 'Medium'
        v_score, v_popularity, v_pop_level = 0.5, 5000, 'Medium'
        v_city, v_state = 'Unknown', 'Unknown'
        v_isGa, v_seatSel = False, True

    # --- Lookup Performer 1 attributes ---
    p1_rows = df[df['performer1_name'] == performer1]
    if not p1_rows.empty:
        p1r = p1_rows.iloc[0]
        p1_score = float(p1r['performer1_performer_score'])
        p1_pop = int(p1r['performer1_performer_popularity'])
        p1_pop_level = p1r['performer1_performer_popularity_level']
        p1_division = p1r['performer1_divisionName']
        p1_div_short = p1r['performer1_divisionShortName']
        p1_home = int(p1r['performer1_has_home_venue'])
    else:
        p1_score, p1_pop, p1_pop_level = 0.5, 100, 'Low'
        p1_division, p1_div_short, p1_home = 'Unknown', 'Unknown', 0

    # --- Lookup Performer 2 attributes ---
    has_p2 = (performer2 != 'No Second Performer')
    if has_p2:
        p2_rows = df[df['performer2_name'] == performer2]
        if not p2_rows.empty:
            p2r = p2_rows.iloc[0]
            p2_score = float(p2r['performer2_performer_score'])
            p2_pop = float(p2r['performer2_performer_popularity'])
            p2_pop_level = p2r['performer2_performer_popularity_level']
            p2_division = p2r['performer2_divisionName']
            p2_div_short = p2r['performer2_divisionShortName']
            p2_home = int(p2r['performer2_has_home_venue']) if not pd.isna(p2r['performer2_has_home_venue']) else 0
        else:
            p2_score, p2_pop, p2_pop_level = 0.5, 100, 'Low'
            p2_division, p2_div_short, p2_home = 'Unknown', 'Unknown', 0
    else:
        p2_score, p2_pop, p2_pop_level = 0.0, 0.0, 'N/A'
        p2_division, p2_div_short, p2_home = 'No Division', 'None', 0

    # --- Derive temporal features ---
    e_month = event_date.month
    e_day = event_date.day
    e_hour = event_time.hour
    day_name = event_date.strftime('%A')
    is_weekend = 1 if event_date.weekday() >= 5 else 0
    is_evening = 1 if e_hour >= 17 else 0
    num_performers = 2 if has_p2 else 1

    # --- Engineered features (same as training) ---
    total_performer_score = p1_score + p2_score
    pop_to_cap_ratio = p1_pop / (v_capacity + 1)
    is_prime_time = 1 if (is_weekend == 1 and is_evening == 1) else 0

    # --- Build feature dict (all columns the model's preprocessing expects) ---
    features_dict = {
        'sport_type': category,
        'taxonomyName': 'sports',
        'isGa': v_isGa,
        'seatSelectionEnabled': v_seatSel,
        'event_date': str(event_date),
        'event_day_name': day_name,
        'city': v_city,
        'state': v_state,
        'venue_name': venue,
        'capacity': v_capacity,
        'capacity_level': v_cap_level,
        'addressCountry': 'US',
        'performer1_name': performer1,
        'performer1_performer_score': p1_score,
        'performer1_divisionName': p1_division,
        'performer1_divisionShortName': p1_div_short,
        'performer1_has_home_venue': p1_home,
        'performer2_name': performer2,
        'performer2_performer_score': p2_score,
        'performer2_divisionName': p2_division,
        'performer2_divisionShortName': p2_div_short,
        'performer2_has_home_venue': p2_home,
        'event_month': e_month,
        'event_day': e_day,
        'event_hour': e_hour,
        'is_weekend': is_weekend,
        'is_evening': is_evening,
        'is_playoff': is_playoff,
        'num_performers': num_performers,
        'total_performer_score': total_performer_score,
        'pop_to_capacity_ratio': pop_to_cap_ratio,
        'is_prime_time': is_prime_time,
    }

    # --- Build display dict for UI transparency ---
    display_dict = {
        'Venue': {
            'Capacity': f"{v_capacity:,}",
            'Capacity Level': v_cap_level,
            'Venue Score': f"{v_score:.2f}",
            'Venue Popularity': f"{v_popularity:,}",
            'Popularity Level': v_pop_level,
            'City': v_city,
            'State': v_state,
            'General Admission': '✅' if v_isGa else '❌',
            'Seat Selection': '✅' if v_seatSel else '❌',
        },
        'Performer 1': {
            'Score': f"{p1_score:.2f}",
            'Popularity': f"{p1_pop:,}",
            'Popularity Level': p1_pop_level,
            'Division': p1_division,
            'Has Home Venue': '✅' if p1_home else '❌',
        },
        'Performer 2': {
            'Score': f"{p2_score:.2f}" if has_p2 else 'N/A',
            'Popularity': f"{p2_pop:,.0f}" if has_p2 else 'N/A',
            'Popularity Level': p2_pop_level,
            'Division': p2_division if has_p2 else 'N/A',
            'Has Home Venue': ('✅' if p2_home else '❌') if has_p2 else 'N/A',
        },
        'Temporal': {
            'Month': e_month,
            'Day': e_day,
            'Day Name': day_name,
            'Hour': f"{e_hour}:00",
            'Weekend': '✅' if is_weekend else '❌',
            'Evening': '✅' if is_evening else '❌',
            'Prime Time': '✅' if is_prime_time else '❌',
        },
        'Engineered': {
            'Total Performer Score': f"{total_performer_score:.2f}",
            'Pop-to-Capacity Ratio': f"{pop_to_cap_ratio:.4f}",
            'Number of Performers': num_performers,
            'Is Playoff': '✅' if is_playoff else '❌',
        },
    }

    return features_dict, display_dict


def prepare_model_input(features_dict, preprocessor_data):
    """
    Converts the raw features dictionary into the exact dummy-encoded
    DataFrame shape expected by the trained Random Forest model.
    """
    input_df = pd.DataFrame([features_dict])

    # One-hot encode categorical columns
    cat_cols = preprocessor_data['cat_cols']
    cols_present = [c for c in cat_cols if c in input_df.columns]
    encoded_df = pd.get_dummies(input_df, columns=cols_present)

    # Reindex to match training columns exactly
    model_columns = preprocessor_data['features']
    for col in model_columns:
        if col not in encoded_df.columns:
            encoded_df[col] = 0

    encoded_df = encoded_df[model_columns]
    return encoded_df
