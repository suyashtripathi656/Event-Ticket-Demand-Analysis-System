"""
recommendation.py — Similarity Engine & Report Generation
IBM AI Event Demand Analysis System

Provides event/venue/performer similarity recommendations
using cosine similarity, and generates exportable reports.
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
import io
import datetime


def find_similar_events(features_dict, df, top_n=5):
    """
    Finds events from the dataset most similar to the user's simulated event
    using cosine similarity on numerical features.

    Returns a DataFrame of the top N most similar events.

    Note: For repeated predictions, consider wrapping with @st.cache_data
    using the features_dict as a hashable key for better performance.
    """
    num_cols = ['capacity', 'event_month', 'event_hour', 'is_weekend', 'is_evening',
                'is_playoff', 'num_performers', 'total_performer_score', 'pop_to_capacity_ratio']

    # Filter columns that exist
    available = [c for c in num_cols if c in df.columns]
    if not available:
        return pd.DataFrame()

    df_num = df[available].fillna(0).copy()

    # Build user vector
    user_vals = [features_dict.get(c, 0) for c in available]
    user_df = pd.DataFrame([user_vals], columns=available)

    # Combine for scaling
    combined = pd.concat([df_num, user_df], ignore_index=True)
    scaler = StandardScaler()
    scaled = scaler.fit_transform(combined)

    user_vec = scaled[-1:, :]
    data_vecs = scaled[:-1, :]

    # Cosine similarity
    sims = cosine_similarity(user_vec, data_vecs)[0]

    # Get top N indices
    top_idx = np.argsort(sims)[::-1][:top_n]

    # Select display columns, guarding against missing columns
    display_cols = ['event_name', 'sport_type', 'venue_name',
                    'performer1_name', 'Demand_Score', 'Demand_Level']
    available_display = [c for c in display_cols if c in df.columns]

    result = df.iloc[top_idx][available_display].copy()
    result['Similarity'] = [f"{sims[i]*100:.1f}%" for i in top_idx]
    return result.reset_index(drop=True)


def find_similar_venues(venue_name, df, top_n=5):
    """Finds venues similar to the selected one based on capacity and popularity."""
    venue_rows = df[df['venue_name'] == venue_name]
    if venue_rows.empty:
        return pd.DataFrame()

    ref = venue_rows.iloc[0]
    ref_cap = ref['capacity']
    ref_pop = ref['venue_popularity']

    venues = df.drop_duplicates('venue_name')[['venue_name', 'capacity', 'venue_popularity', 'city', 'state']].copy()
    venues = venues[venues['venue_name'] != venue_name]

    # Simple distance metric
    venues['distance'] = np.sqrt(
        ((venues['capacity'] - ref_cap) / (df['capacity'].max() + 1)) ** 2 +
        ((venues['venue_popularity'] - ref_pop) / (df['venue_popularity'].max() + 1)) ** 2
    )
    return venues.nsmallest(top_n, 'distance').drop(columns=['distance']).reset_index(drop=True)


def find_similar_performers(performer_name, df, top_n=5):
    """Finds performers similar to the selected one based on score and popularity."""
    p_rows = df[df['performer1_name'] == performer_name]
    if p_rows.empty:
        return pd.DataFrame()

    ref = p_rows.iloc[0]
    ref_score = ref['performer1_performer_score']
    ref_pop = ref['performer1_performer_popularity']

    perfs = df.drop_duplicates('performer1_name')[
        ['performer1_name', 'sport_type', 'performer1_performer_score',
         'performer1_performer_popularity']].copy()
    perfs = perfs[perfs['performer1_name'] != performer_name]

    perfs['distance'] = np.sqrt(
        ((perfs['performer1_performer_score'] - ref_score) / 1.0) ** 2 +
        ((perfs['performer1_performer_popularity'] - ref_pop) / (df['performer1_performer_popularity'].max() + 1)) ** 2
    )
    return perfs.nsmallest(top_n, 'distance').drop(columns=['distance']).reset_index(drop=True)


def find_higher_demand_events(current_score, df, top_n=5):
    """Finds events with higher predicted demand than the current simulation."""
    higher = df[df['Demand_Score'] > current_score].nlargest(top_n, 'Demand_Score')
    display_cols = ['event_name', 'sport_type', 'venue_name', 'performer1_name',
                    'Demand_Score', 'Demand_Level']
    available_display = [c for c in display_cols if c in higher.columns]
    return higher[available_display].reset_index(drop=True)


def generate_prediction_report(score, level, confidence, features_dict, display_dict,
                                explanations, recommendations):
    """
    Generates a formatted text report of the prediction for export.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("AI EVENT DEMAND PREDICTION REPORT")
    lines.append(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"DEMAND SCORE:  {score:.1f} / 100")
    lines.append(f"DEMAND LEVEL:  {level}")
    lines.append(f"CONFIDENCE:    {confidence:.1f}%")
    lines.append("")
    lines.append("-" * 40)
    lines.append("EVENT CONFIGURATION")
    lines.append("-" * 40)
    lines.append(f"Category:      {features_dict.get('sport_type', 'N/A')}")
    lines.append(f"Venue:         {features_dict.get('venue_name', 'N/A')}")
    lines.append(f"Performer 1:   {features_dict.get('performer1_name', 'N/A')}")
    lines.append(f"Performer 2:   {features_dict.get('performer2_name', 'N/A')}")
    lines.append(f"Date:          {features_dict.get('event_date', 'N/A')}")
    lines.append(f"Playoff:       {'Yes' if features_dict.get('is_playoff') else 'No'}")
    lines.append("")

    for section, items in display_dict.items():
        lines.append(f"--- {section.upper()} ---")
        for k, v in items.items():
            lines.append(f"  {k}: {v}")
        lines.append("")

    lines.append("-" * 40)
    lines.append("AI EXPLANATION")
    lines.append("-" * 40)
    for exp in explanations:
        lines.append(f"  ✓ {exp['text']}")
    lines.append("")

    lines.append("-" * 40)
    lines.append("BUSINESS RECOMMENDATIONS")
    lines.append("-" * 40)
    for rec in recommendations:
        lines.append(f"  {rec}")
    lines.append("")
    lines.append("=" * 60)
    lines.append("End of Report")

    return "\n".join(lines)


def generate_csv_report(score, level, confidence, features_dict, display_dict):
    """Generates a CSV-formatted string for download."""
    rows = [
        {'Section': 'Prediction', 'Metric': 'Demand Score', 'Value': f"{score:.1f}"},
        {'Section': 'Prediction', 'Metric': 'Demand Level', 'Value': level},
        {'Section': 'Prediction', 'Metric': 'Confidence', 'Value': f"{confidence:.1f}%"},
    ]
    rows.append({'Section': 'Config', 'Metric': 'Category', 'Value': features_dict.get('sport_type', '')})
    rows.append({'Section': 'Config', 'Metric': 'Venue', 'Value': features_dict.get('venue_name', '')})
    rows.append({'Section': 'Config', 'Metric': 'Performer 1', 'Value': features_dict.get('performer1_name', '')})
    rows.append({'Section': 'Config', 'Metric': 'Performer 2', 'Value': features_dict.get('performer2_name', '')})

    for section, items in display_dict.items():
        for k, v in items.items():
            rows.append({'Section': section, 'Metric': k, 'Value': str(v)})

    return pd.DataFrame(rows).to_csv(index=False)
