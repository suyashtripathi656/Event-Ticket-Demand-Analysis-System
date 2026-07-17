"""
prediction.py — Prediction Engine & Explainable AI
IBM AI Event Demand Analysis System

Handles model loading, demand prediction, confidence scoring,
explainable AI analysis, and business recommendation generation.
"""

import joblib
import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_artifacts(base_path=None):
    """Loads the trained Random Forest model and preprocessor metadata."""
    if base_path is None:
        base_path = os.path.join(BASE_DIR, 'output')
    model = joblib.load(os.path.join(base_path, 'trained_model.pkl'))
    preprocessor = joblib.load(os.path.join(base_path, 'preprocessor.pkl'))
    return model, preprocessor


def get_demand_level(score):
    """Assigns demand level based on score 0-100."""
    if score >= 66:
        return 'High Demand'
    elif score >= 33:
        return 'Medium Demand'
    return 'Low Demand'


def predict_demand(encoded_input_df, model):
    """
    Runs the Random Forest prediction and calculates a confidence metric
    using inter-tree standard deviation as a proxy for uncertainty.

    Returns:
        score (float): Predicted demand score (0-100)
        level (str): Demand level category
        confidence (float): Confidence percentage (0-100)
    """
    score = float(np.clip(model.predict(encoded_input_df)[0], 0, 100))

    # Confidence via inter-tree agreement
    tree_preds = np.array([
        est.predict(encoded_input_df.values)[0] for est in model.estimators_
    ])
    std_dev = np.std(tree_preds)
    confidence = float(np.clip(100 - (std_dev * 2.5), 0, 100))

    level = get_demand_level(score)
    return score, level, confidence


def get_explanation(encoded_input, importance_records, features_dict=None):
    """
    Generates comprehensive Explainable AI reasoning by analyzing which features
    are active in the prediction and cross-referencing feature importances.

    Returns a list of dictionaries with icon, text, and impact level.
    """
    explanations = []

    # Map of feature patterns to business-readable explanations
    explanation_map = {
        'capacity': lambda v: f"Venue capacity of {int(v):,} seats {'significantly boosts' if v > 30000 else 'moderately impacts'} demand.",
        'total_performer_score': lambda v: f"Combined performer star power score of {v:.2f} {'drives strong' if v > 1.0 else 'provides moderate'} demand.",
        'pop_to_capacity_ratio': lambda v: f"Performer-to-venue popularity ratio of {v:.4f} indicates {'optimal' if v > 0.5 else 'moderate'} demand alignment.",
        'is_playoff': lambda v: "🏆 Playoff/Championship event creates massive demand surge." if v > 0 else None,
        'is_weekend': lambda v: "📅 Weekend scheduling attracts larger casual audiences." if v > 0 else None,
        'is_evening': lambda v: "🌙 Evening time slot aligns with peak attendance windows." if v > 0 else None,
        'is_prime_time': lambda v: "⭐ Prime-time slot (Weekend + Evening) maximizes audience reach." if v > 0 else None,
        'num_performers': lambda v: f"Event features {int(v)} performer(s), {'increasing competitive interest' if v >= 2 else 'standard single-performer event'}.",
        'event_month': lambda v: f"Month {int(v)} is {'peak' if v in [5,6,10,11] else 'regular'} season for sports events.",
        'performer1_performer_score': lambda v: f"Primary performer score of {v:.2f} {'is elite-tier' if v > 0.7 else 'is competitive'}.",
        'performer2_performer_score': lambda v: f"Secondary performer score of {v:.2f} {'adds significant draw' if v > 0.5 else 'provides additional interest'}." if v > 0 else None,
    }

    # Check importance records
    for record in importance_records:
        fname = record['Feature']
        importance = record['Importance']

        # Check if this feature exists in the encoded input
        if fname in encoded_input.columns:
            val = encoded_input[fname].iloc[0]
            if val != 0:
                # Try to find a business explanation
                matched = False
                for pattern, explainer in explanation_map.items():
                    if pattern in fname:
                        text = explainer(val)
                        if text:
                            explanations.append({
                                'text': text,
                                'importance': importance,
                                'feature': fname,
                            })
                            matched = True
                            break

                if not matched and importance > 0.01:
                    # Handle one-hot encoded features
                    if 'sport_type_' in fname:
                        sport = fname.replace('sport_type_', '').upper()
                        explanations.append({
                            'text': f"🏟️ {sport} events have historically strong demand patterns.",
                            'importance': importance,
                            'feature': fname,
                        })
                    elif 'divisionName' in fname or 'divisionShortName' in fname:
                        div = fname.split('_')[-1]
                        explanations.append({
                            'text': f"Division/Conference '{div}' has notable demand influence.",
                            'importance': importance,
                            'feature': fname,
                        })
                    elif 'capacity_level_' in fname:
                        level = fname.replace('capacity_level_', '')
                        explanations.append({
                            'text': f"'{level}' capacity venues {'significantly boost' if level in ['Large','Mega'] else 'moderately affect'} demand.",
                            'importance': importance,
                            'feature': fname,
                        })
                    else:
                        explanations.append({
                            'text': f"Feature '{fname}' (value: {val:.2f}) contributes to the prediction.",
                            'importance': importance,
                            'feature': fname,
                        })

        if len(explanations) >= 6:
            break

    if not explanations:
        explanations.append({
            'text': "The prediction is based on balanced baseline metrics across all features.",
            'importance': 0.0,
            'feature': 'baseline',
        })

    return explanations


def generate_business_recommendation(score, level, features_dict, display_dict):
    """
    Generates actionable business recommendations based on the prediction.

    Returns a list of recommendation strings.
    """
    recommendations = []
    is_playoff = features_dict.get('is_playoff', 0)
    is_weekend = features_dict.get('is_weekend', 0)
    is_evening = features_dict.get('is_evening', 0)
    capacity = features_dict.get('capacity', 0)

    if level == 'High Demand':
        recommendations.append("📈 **Premium Pricing Strategy**: High demand suggests premium ticket pricing will be well-received.")
        recommendations.append("🎟️ **Early Bird Sales**: Launch early-bird ticket sales to capitalize on anticipated demand.")
        if capacity > 40000:
            recommendations.append("🏟️ **Full Venue Operations**: Activate all venue sections and concession stands for maximum revenue.")
        recommendations.append("📢 **Marketing**: Minimal marketing spend needed — organic demand is strong.")

    elif level == 'Medium Demand':
        recommendations.append("💰 **Tiered Pricing**: Implement tiered pricing with mid-range base and premium section markups.")
        if not is_weekend:
            recommendations.append("📅 **Consider Rescheduling**: Moving to a weekend slot could boost demand by ~10%.")
        if not is_evening:
            recommendations.append("🌙 **Evening Slot**: Evening events historically attract larger audiences.")
        recommendations.append("📢 **Targeted Marketing**: Focus on local fan base and social media campaigns.")

    else:  # Low Demand
        recommendations.append("🎯 **Promotional Pricing**: Implement aggressive promotional pricing and bundle deals.")
        recommendations.append("🤝 **Group Discounts**: Offer corporate and group discount packages.")
        if not is_playoff:
            recommendations.append("🏆 **Highlight Event Significance**: Emphasize any competitive stakes in marketing.")
        recommendations.append("📢 **Heavy Marketing**: Increase marketing spend significantly to drive awareness.")

    return recommendations


def get_feature_contributions(encoded_input, model, preprocessor_data):
    """
    Calculates per-feature contribution using the mean decrease in prediction
    when each feature is zeroed out (permutation-style approximation).

    Returns a DataFrame of feature names and their contribution percentages.
    """
    base_pred = model.predict(encoded_input)[0]
    contributions = []

    # NOTE: preprocessor_data['importance_df'] is a list of dicts (from .to_dict('records')),
    # NOT a pandas DataFrame. It is consumed as raw records by get_explanation().
    importance_df = pd.DataFrame(preprocessor_data['importance_df'])
    top_features = importance_df.head(10)['Feature'].tolist()

    for feat in top_features:
        if feat in encoded_input.columns:
            modified = encoded_input.copy()
            modified[feat] = 0
            new_pred = model.predict(modified)[0]
            diff = abs(base_pred - new_pred)
            contributions.append({'Feature': feat, 'Contribution': diff})

    contrib_df = pd.DataFrame(contributions)
    if not contrib_df.empty and contrib_df['Contribution'].sum() > 0:
        contrib_df['Contribution_Pct'] = (contrib_df['Contribution'] / contrib_df['Contribution'].sum() * 100)
    else:
        contrib_df['Contribution_Pct'] = 0.0

    return contrib_df.sort_values('Contribution_Pct', ascending=False).reset_index(drop=True)
