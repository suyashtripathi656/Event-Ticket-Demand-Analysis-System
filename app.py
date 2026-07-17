"""
app.py — Enterprise AI Event Demand Analysis System
IBM Data Science Internship | Production Dashboard

Main application entry point with sidebar navigation across 6 pages:
1. Overview  2. Analytics  3. Demand Predictor  4. Event Comparison
5. What-If Analysis  6. About Project
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import os
import traceback

from utils.helper import (
    GLOBAL_CSS, COLORS, SPORT_ICONS, DEMAND_CONFIG,
    render_kpi_card, render_result_card, render_demand_badge,
    render_section_header, render_autofill_item, render_insight_card,
    render_scenario_card, render_timeline_step, render_tech_badge,
    render_winner_banner, render_vs_badge, render_glass_panel,
)
from utils.preprocessing import load_dataset, get_unique_options, smart_autofill, prepare_model_input
from utils.prediction import load_artifacts, predict_demand, get_explanation, generate_business_recommendation, get_feature_contributions
from utils.visualization import (
    plot_events_by_category, plot_demand_score_distribution, plot_demand_level_donut,
    plot_capacity_boxplot, plot_venue_popularity_violin, plot_top_venues, plot_capacity_treemap,
    plot_top_performers, plot_performer_score_vs_demand,
    plot_monthly_trends, plot_weekday_distribution, plot_weekend_donut,
    plot_playoff_impact, plot_hour_month_heatmap,
    plot_capacity_vs_demand, plot_sunburst, plot_3d_scatter, plot_state_distribution,
    plot_demand_by_category,
    plot_feature_importance, plot_correlation_heatmap, plot_feature_contributions,
    plot_gauge_meter, plot_comparison_radar,
)
from utils.recommendation import (
    find_similar_events, find_similar_venues, find_similar_performers,
    find_higher_demand_events, generate_prediction_report, generate_csv_report,
)

# =============================================
# PAGE CONFIG
# =============================================
st.set_page_config(
    page_title="Event Ticket Demand Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# =============================================
# DATA & MODEL LOADING
# =============================================
@st.cache_resource
def load_all():
    """Loads dataset, model, preprocessor, and dropdown options.
    Note: Columns like performer1_performer_popularity, venue_popularity, venue_score
    are kept in the dataset for display/autofill but are NOT model features (dropped as leakage).
    """
    df = load_dataset()
    model, prep = load_artifacts()
    opts = get_unique_options(df)
    return df, model, prep, opts

try:
    master_df, model, preprocessor, options = load_all()
except Exception as e:
    st.error(f"⚠️ Failed to load resources: {e}")
    st.info("Please run `python train_and_save_model.py` first to generate model artifacts.")
    st.stop()

# =============================================
# SIDEBAR NAVIGATION
# =============================================
with st.sidebar:
    # Logo / Brand
    st.markdown("### Event Ticket Demand Analysis System")
    st.markdown("---")
    st.markdown("---")

    page = st.radio("Navigation", [
        "🏠 Overview",
        "📊 Analytics Dashboard",
        "🎯 Demand Predictor",
        "⚖️ Event Comparison",
        "🔬 What-If Analysis",
        "🎓 About Project",
    ], label_visibility="collapsed")

    st.markdown("---")

    # System status
    st.markdown(f"""
    <div style="padding: 0.75rem 1rem; background:rgba(255,255,255,0.03);
                border-radius:8px; margin:0.25rem 0;">
        <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.4rem;">
            <div style="width:7px; height:7px; border-radius:50%; background:#24a148;
                        box-shadow:0 0 6px rgba(36,161,72,0.5);"></div>
            <span style="color:rgba(255,255,255,0.6); font-size:0.72rem; font-weight:600;
                         letter-spacing:0.05em;">SYSTEM ONLINE</span>
        </div>
        <div style="color:rgba(255,255,255,0.35); font-size:0.68rem; line-height:1.6;">
            Model: Random Forest (100 trees)<br>
            Dataset: {len(master_df):,} events loaded<br>
            Features: {len(preprocessor['features'])} active
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="padding: 0.5rem; text-align:center;">
        <p style="color:rgba(255,255,255,0.3); font-size:0.68rem; margin:0; font-weight:500;">
            Scikit-Learn · Plotly · Streamlit
        </p>
    </div>
    """, unsafe_allow_html=True)


# =============================================
# HELPER: Render Chart Card
# =============================================
def render_chart_card(fig, title_text=None):
    if title_text is None:
        title_text = fig.layout.title.text if fig.layout.title and fig.layout.title.text else ""
    # Remove Plotly title and adjust margins to fit the card layout, letting Plotly handle L/R margins
    fig.update_layout(title="", margin=dict(t=20, b=20))
    with st.container(border=True):
        st.markdown(f'<div class="chart-title">{title_text}</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)

# =============================================
# HELPER: Run prediction pipeline
# =============================================
def run_prediction(category, venue, p1, p2, event_date, event_time, is_playoff):
    """Runs the full smart-autofill → encode → predict pipeline."""
    try:
        features, display = smart_autofill(category, venue, p1, p2, event_date, event_time, is_playoff, master_df)
        encoded = prepare_model_input(features, preprocessor)
        score, level, confidence = predict_demand(encoded, model)
        explanations = get_explanation(encoded, preprocessor['importance_df'], features)
        recommendations = generate_business_recommendation(score, level, features, display)
        contrib_df = get_feature_contributions(encoded, model, preprocessor)
        return score, level, confidence, features, display, encoded, explanations, recommendations, contrib_df
    except Exception as e:
        st.error(f"⚠️ Prediction pipeline error: {e}")
        st.code(traceback.format_exc(), language='text')
        st.stop()


# =============================================
# PAGE 1: OVERVIEW
# =============================================
if page == "🏠 Overview":
    st.markdown("""
    <div class="hero-banner">
        <h1>Event Ticket Demand Analysis</h1>
        <p>Intelligent estimation of event ticket demand using Machine Learning & Explainable AI</p>
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards — 3x2 responsive grid
    row1_c1, row1_c2, row1_c3 = st.columns(3)
    with row1_c1:
        st.markdown(render_kpi_card("Total Events", f"{len(master_df):,}", "in dataset", "blue"), unsafe_allow_html=True)
    with row1_c2:
        st.markdown(render_kpi_card("Unique Venues", f"{master_df['venue_name'].nunique()}", "across US", "purple"), unsafe_allow_html=True)
    with row1_c3:
        st.markdown(render_kpi_card("Performers", f"{master_df['performer1_name'].nunique()}", "tracked", "teal"), unsafe_allow_html=True)

    row2_c1, row2_c2, row2_c3 = st.columns(3)
    with row2_c1:
        st.markdown(render_kpi_card("Sport Types", f"{master_df['sport_type'].nunique()}", "categories", "cyan"), unsafe_allow_html=True)
    with row2_c2:
        avg_demand = master_df['Demand_Score'].mean()
        st.markdown(render_kpi_card("Avg Demand", f"{avg_demand:.1f}", "score (0-100)", "green"), unsafe_allow_html=True)
    with row2_c3:
        high_pct = (master_df['Demand_Level'] == 'High Demand').sum() / len(master_df) * 100
        st.markdown(render_kpi_card("High Demand", f"{high_pct:.1f}%", "of all events", "red"), unsafe_allow_html=True)

    # --- How It Works: Timeline ---
    st.markdown(render_section_header("⚡", "How It Works"), unsafe_allow_html=True)

    hw_col, chart_col = st.columns([3, 2])
    with hw_col:
        st.markdown(render_timeline_step("1", "Data Integration",
            "Events, Performers, and Venues data merged into a unified dataset with 1,385+ records.", 0), unsafe_allow_html=True)
        st.markdown(render_timeline_step("2", "Feature Engineering",
            "15+ features including temporal dynamics, star power metrics, and venue capacity ratios.", 0.1), unsafe_allow_html=True)
        st.markdown(render_timeline_step("3", "Machine Learning",
            "Random Forest Regressor trained on engineered Demand Score (0-100) with 100 decision trees.", 0.2), unsafe_allow_html=True)
        st.markdown(render_timeline_step("4", "Smart Prediction",
            "Enter 7 natural inputs → system auto-fills 20+ features → AI predicts demand instantly.", 0.3), unsafe_allow_html=True)
        st.markdown(render_timeline_step("5", "Explainable AI",
            "Every prediction comes with business-readable explanations and actionable recommendations.", 0.4), unsafe_allow_html=True)

    with chart_col:
        st.plotly_chart(plot_demand_level_donut(master_df), use_container_width=True)
        st.plotly_chart(plot_events_by_category(master_df), use_container_width=True)

    # Key Capabilities
    st.markdown(render_section_header("🎯", "Key Capabilities"), unsafe_allow_html=True)
    cap_c1, cap_c2, cap_c3, cap_c4, cap_c5 = st.columns(5)
    with cap_c1:
        st.markdown(render_kpi_card("Analytics", "20+", "interactive charts", "blue"), unsafe_allow_html=True)
    with cap_c2:
        st.markdown(render_kpi_card("Predictor", "Smart", "auto-fill system", "purple"), unsafe_allow_html=True)
    with cap_c3:
        st.markdown(render_kpi_card("Comparison", "Side by", "side analysis", "teal"), unsafe_allow_html=True)
    with cap_c4:
        st.markdown(render_kpi_card("What-If", "Scenario", "simulation", "cyan"), unsafe_allow_html=True)
    with cap_c5:
        st.markdown(render_kpi_card("Export", "CSV &", "text reports", "green"), unsafe_allow_html=True)


# =============================================
# PAGE 2: ANALYTICS DASHBOARD
# =============================================
elif page == "📊 Analytics Dashboard":
    st.markdown(render_section_header("📊", "Advanced Analytics Dashboard"), unsafe_allow_html=True)

    # Filter bar
    filter_col1, filter_col2, filter_col3 = st.columns([1, 2, 1])
    with filter_col1:
        # Initialize filter state
        if 'analytics_cat_filter' not in st.session_state:
            st.session_state.analytics_cat_filter = 'All'
        cat_filter = st.selectbox(
            "Filter by Category",
            ['All'] + options['categories'],
            index=(['All'] + options['categories']).index(st.session_state.analytics_cat_filter)
                  if st.session_state.analytics_cat_filter in ['All'] + options['categories'] else 0,
            key="analytics_filter_select",
        )
        st.session_state.analytics_cat_filter = cat_filter
    with filter_col3:
        if cat_filter != 'All':
            if st.button("✕ Reset Filter"):
                st.session_state.analytics_cat_filter = 'All'
                st.rerun()
    df_f = master_df if cat_filter == 'All' else master_df[master_df['sport_type'] == cat_filter]

    # Dataset summary strip
    ds_c1, ds_c2, ds_c3, ds_c4 = st.columns(4)
    with ds_c1:
        st.markdown(render_kpi_card("Events", f"{len(df_f):,}", "in filter", "blue"), unsafe_allow_html=True)
    with ds_c2:
        st.markdown(render_kpi_card("Avg Score", f"{df_f['Demand_Score'].mean():.1f}", "demand", "purple"), unsafe_allow_html=True)
    with ds_c3:
        st.markdown(render_kpi_card("Venues", f"{df_f['venue_name'].nunique()}", "unique", "teal"), unsafe_allow_html=True)
    with ds_c4:
        st.markdown(render_kpi_card("Performers", f"{df_f['performer1_name'].nunique()}", "unique", "cyan"), unsafe_allow_html=True)

    # Analytics Tabs
    t1, t2, t3, t4, t5 = st.tabs(["📈 Demand", "🏟️ Venues", "⭐ Performers", "📅 Temporal", "🧠 Model"])

    with t1:
        c1, c2 = st.columns(2)
        with c1:
            render_chart_card(plot_demand_score_distribution(df_f))
        with c2:
            render_chart_card(plot_demand_by_category(df_f))

        c3, c4 = st.columns(2)
        with c3:
            render_chart_card(plot_demand_level_donut(df_f))
        with c4:
            render_chart_card(plot_capacity_vs_demand(df_f))

        render_chart_card(plot_3d_scatter(df_f))

    with t2:
        c1, c2 = st.columns(2)
        with c1:
            render_chart_card(plot_capacity_boxplot(df_f))
        with c2:
            render_chart_card(plot_venue_popularity_violin(df_f))

        c3, c4 = st.columns(2)
        with c3:
            render_chart_card(plot_capacity_treemap(df_f))
        with c4:
            render_chart_card(plot_state_distribution(df_f))

    with t3:
        c1, c2 = st.columns(2)
        with c1:
            render_chart_card(plot_top_performers(df_f))
        with c2:
            render_chart_card(plot_performer_score_vs_demand(df_f))

    with t4:
        c1, c2 = st.columns(2)
        with c1:
            render_chart_card(plot_monthly_trends(df_f))
        with c2:
            render_chart_card(plot_weekend_donut(df_f))

        c3, c4 = st.columns(2)
        with c3:
            render_chart_card(plot_weekday_distribution(df_f))
        with c4:
            render_chart_card(plot_playoff_impact(df_f))

        c5, c6 = st.columns(2)
        with c5:
            render_chart_card(plot_hour_month_heatmap(df_f))
        with c6:
            render_chart_card(plot_sunburst(df_f))

    with t5:
        c1, c2 = st.columns(2)
        with c1:
            render_chart_card(plot_feature_importance(preprocessor['importance_df']))
        with c2:
            render_chart_card(plot_correlation_heatmap(df_f))

    # Business Insights
    st.markdown(render_section_header("💡", "Auto-Generated Business Insights"), unsafe_allow_html=True)

    top_cat = df_f.groupby('sport_type')['Demand_Score'].mean().idxmax()
    top_venue = df_f.groupby('venue_name')['venue_popularity'].max().idxmax()
    top_perf = df_f.groupby('performer1_name')['performer1_performer_popularity'].max().idxmax()
    wk_demand = df_f[df_f['is_weekend'] == 1]['Demand_Score'].mean()
    wd_demand = df_f[df_f['is_weekend'] == 0]['Demand_Score'].mean()
    playoff_demand = df_f[df_f['is_playoff'] == 1]['Demand_Score'].mean() if df_f['is_playoff'].sum() > 0 else 0
    cap_corr = df_f['capacity'].corr(df_f['Demand_Score'])

    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown(render_insight_card("🏆", "Highest Demand Category",
            f"{SPORT_ICONS.get(top_cat, '')} {top_cat.upper()}", "#da1e28"), unsafe_allow_html=True)
        st.markdown(render_insight_card("🏟️", "Most Popular Venue",
            top_venue, "#0f62fe"), unsafe_allow_html=True)
    with i2:
        st.markdown(render_insight_card("⭐", "Top Performer",
            top_perf, "#8a3ffc"), unsafe_allow_html=True)
        st.markdown(render_insight_card("📅", "Weekend vs Weekday",
            f"{wk_demand:.1f} vs {wd_demand:.1f}", "#009d9a"), unsafe_allow_html=True)
    with i3:
        st.markdown(render_insight_card("🏆", "Playoff Avg Demand",
            f"{playoff_demand:.1f}", "#1192e8"), unsafe_allow_html=True)
        st.markdown(render_insight_card("📐", "Capacity-Demand Corr",
            f"{cap_corr:.3f}", "#ee5396"), unsafe_allow_html=True)


# =============================================
# PAGE 3: DEMAND PREDICTOR
# =============================================
elif page == "🎯 Demand Predictor":
    st.markdown(render_section_header("🎯", "AI Demand Predictor — Smart Input System"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--bg-card); border:1px solid var(--border-default);
                border-radius:var(--radius-md); padding:1rem 1.5rem; margin-bottom:1.5rem;
                display:flex; align-items:center; gap:0.75rem;">
        <span style="font-size:1.25rem;">💡</span>
        <span style="color:var(--text-secondary); font-size:0.9rem;">
            Enter only <strong>7 natural inputs</strong> — the system automatically retrieves
            and engineers all remaining features from the dataset.
        </span>
    </div>
    """, unsafe_allow_html=True)

    with st.form("predict_form"):
        st.markdown("#### ⚙️ Event Configuration")
        fc1, fc2, fc3 = st.columns(3)
        with fc1:
            p_category = st.selectbox("Event Category", options['categories'])
            p_venue = st.selectbox("Venue", options['venues'])
            p_playoff = st.radio("Playoff/Championship?", ["No", "Yes"], horizontal=True)
        with fc2:
            p_p1 = st.selectbox("Performer 1 (Home)", options['performers_p1'])
            p_p2 = st.selectbox("Performer 2 (Away)", options['performers_p2'])
        with fc3:
            p_date = st.date_input("Event Date", datetime.date.today() + datetime.timedelta(days=30))
            p_time = st.time_input("Event Time", datetime.time(19, 30))

        submitted = st.form_submit_button("Predict Demand", use_container_width=True)

    if submitted:
        is_playoff = 1 if p_playoff == "Yes" else 0
        with st.spinner("Running Smart Auto-Fill & AI Prediction Pipeline..."):
            score, level, confidence, features, display, encoded, explanations, recommendations, contrib_df = \
                run_prediction(p_category, p_venue, p_p1, p_p2, p_date, p_time, is_playoff)

        # ---- RESULTS ----
        st.markdown("---")
        st.markdown(render_section_header("🎯", "Prediction Results"), unsafe_allow_html=True)

        # Gauge + KPIs
        g_col, r_col1, r_col2 = st.columns([2, 1, 1])
        with g_col:
            st.plotly_chart(plot_gauge_meter(score), use_container_width=True)
        with r_col1:
            cfg = DEMAND_CONFIG.get(level, DEMAND_CONFIG['Medium Demand'])
            st.markdown(render_result_card("Demand Level", level, cfg['color'], cfg['color']), unsafe_allow_html=True)
        with r_col2:
            st.markdown(render_result_card("Confidence", f"{confidence:.1f}%", COLORS['purple'], COLORS['purple']), unsafe_allow_html=True)

        # Demand badge
        badge_col, _ = st.columns([1, 3])
        with badge_col:
            st.markdown(render_demand_badge(level), unsafe_allow_html=True)

        # Auto-filled features (transparency)
        with st.expander("🔍 Auto-Filled Features — Smart Retrieval from Dataset", expanded=False):
            for section_name, items in display.items():
                st.markdown(f"**{section_name}**")
                cols = st.columns(3)
                for i, (k, v) in enumerate(items.items()):
                    with cols[i % 3]:
                        st.markdown(render_autofill_item(k, v), unsafe_allow_html=True)

        # Explainable AI
        st.markdown(render_section_header("🧠", "Explainable AI — Why This Prediction?"), unsafe_allow_html=True)

        exp_cols = st.columns(2)
        for idx, exp in enumerate(explanations):
            with exp_cols[idx % 2]:
                st.markdown(render_insight_card("✅", exp.get('feature', 'insight'),
                    exp['text'], "#0f62fe"), unsafe_allow_html=True)

        # Feature Contributions + Business Recommendations
        ec1, ec2 = st.columns(2)
        with ec1:
            st.plotly_chart(plot_feature_contributions(contrib_df), use_container_width=True)
        with ec2:
            st.markdown(render_section_header("💼", "Business Recommendations"), unsafe_allow_html=True)
            for rec in recommendations:
                st.markdown(rec)

        # Similar Events & Recommendations
        st.markdown(render_section_header("🔗", "Similar Events & Recommendations"), unsafe_allow_html=True)
        sim_tabs = st.tabs(["🔍 Similar Events", "🏟️ Similar Venues", "⭐ Similar Performers", "📈 Higher Demand"])
        with sim_tabs[0]:
            sim_events = find_similar_events(features, master_df)
            if not sim_events.empty:
                st.dataframe(sim_events, hide_index=True, use_container_width=True)
        with sim_tabs[1]:
            sim_venues = find_similar_venues(p_venue, master_df)
            if not sim_venues.empty:
                st.dataframe(sim_venues, hide_index=True, use_container_width=True)
        with sim_tabs[2]:
            sim_perfs = find_similar_performers(p_p1, master_df)
            if not sim_perfs.empty:
                st.dataframe(sim_perfs, hide_index=True, use_container_width=True)
        with sim_tabs[3]:
            higher = find_higher_demand_events(score, master_df)
            if not higher.empty:
                st.dataframe(higher, hide_index=True, use_container_width=True)

        # Export
        st.markdown(render_section_header("📥", "Export Report"), unsafe_allow_html=True)
        exp_c1, exp_c2 = st.columns(2)
        with exp_c1:
            report_text = generate_prediction_report(score, level, confidence, features, display, explanations, recommendations)
            st.download_button("📄 Download Text Report", report_text, file_name="demand_report.txt", mime="text/plain", use_container_width=True)
        with exp_c2:
            csv_data = generate_csv_report(score, level, confidence, features, display)
            st.download_button("📊 Download CSV Report", csv_data, file_name="demand_report.csv", mime="text/csv", use_container_width=True)


# =============================================
# PAGE 4: EVENT COMPARISON
# =============================================
elif page == "⚖️ Event Comparison":
    st.markdown(render_section_header("⚖️", "Event Comparison Module"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--bg-card); border:1px solid var(--border-default);
                border-radius:var(--radius-md); padding:1rem 1.5rem; margin-bottom:1.5rem;
                display:flex; align-items:center; gap:0.75rem;">
        <span style="font-size:1.25rem;">⚖️</span>
        <span style="color:var(--text-secondary); font-size:0.9rem;">
            Configure two events side-by-side to compare their predicted demand
            and understand why one scores higher.
        </span>
    </div>
    """, unsafe_allow_html=True)

    col_a, col_sep, col_b = st.columns([5, 1, 5])

    with col_a:
        st.markdown("""
        <div style="background:var(--gradient-blue); color:white; padding:0.5rem 1rem;
                    border-radius:var(--radius-sm); font-weight:700; font-size:0.9rem;
                    display:inline-block; margin-bottom:1rem;">🅰️ Event A</div>
        """, unsafe_allow_html=True)
        ca_cat = st.selectbox("Category", options['categories'], key="ca_cat")
        ca_venue = st.selectbox("Venue", options['venues'], key="ca_venue")
        ca_p1 = st.selectbox("Performer 1", options['performers_p1'], key="ca_p1")
        ca_p2 = st.selectbox("Performer 2", options['performers_p2'], key="ca_p2")
        ca_date = st.date_input("Date", datetime.date.today() + datetime.timedelta(days=30), key="ca_date")
        ca_time = st.time_input("Time", datetime.time(19, 0), key="ca_time")
        ca_playoff = st.radio("Playoff?", ["No", "Yes"], key="ca_pf", horizontal=True)

    with col_sep:
        st.markdown(render_vs_badge(), unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div style="background:linear-gradient(135deg, #da1e28, #ee5396); color:white;
                    padding:0.5rem 1rem; border-radius:var(--radius-sm); font-weight:700;
                    font-size:0.9rem; display:inline-block; margin-bottom:1rem;">🅱️ Event B</div>
        """, unsafe_allow_html=True)
        cb_cat = st.selectbox("Category", options['categories'], key="cb_cat")
        cb_venue = st.selectbox("Venue", options['venues'], key="cb_venue", index=min(1, len(options['venues'])-1))
        cb_p1 = st.selectbox("Performer 1", options['performers_p1'], key="cb_p1", index=min(1, len(options['performers_p1'])-1))
        cb_p2 = st.selectbox("Performer 2", options['performers_p2'], key="cb_p2")
        cb_date = st.date_input("Date", datetime.date.today() + datetime.timedelta(days=14), key="cb_date")
        cb_time = st.time_input("Time", datetime.time(14, 0), key="cb_time")
        cb_playoff = st.radio("Playoff?", ["No", "Yes"], key="cb_pf", horizontal=True)

    if st.button("⚖️ Compare Events", use_container_width=True):
        with st.spinner("Running dual prediction pipeline..."):
            sA, lA, cA, fA, dA, eA, exA, rA, ctA = run_prediction(ca_cat, ca_venue, ca_p1, ca_p2, ca_date, ca_time, 1 if ca_playoff == "Yes" else 0)
            sB, lB, cB, fB, dB, eB, exB, rB, ctB = run_prediction(cb_cat, cb_venue, cb_p1, cb_p2, cb_date, cb_time, 1 if cb_playoff == "Yes" else 0)

        st.markdown("---")

        # Results side by side
        rc1, rc2 = st.columns(2)
        with rc1:
            st.plotly_chart(plot_gauge_meter(sA, 'Event A'), use_container_width=True)
            badge_a, _ = st.columns([1, 2])
            with badge_a:
                st.markdown(render_demand_badge(lA), unsafe_allow_html=True)
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.9rem;
                        color:var(--text-secondary); margin-top:0.5rem;">
                Confidence: <strong>{cA:.1f}%</strong>
            </div>
            """, unsafe_allow_html=True)
        with rc2:
            st.plotly_chart(plot_gauge_meter(sB, 'Event B'), use_container_width=True)
            badge_b, _ = st.columns([1, 2])
            with badge_b:
                st.markdown(render_demand_badge(lB), unsafe_allow_html=True)
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.9rem;
                        color:var(--text-secondary); margin-top:0.5rem;">
                Confidence: <strong>{cB:.1f}%</strong>
            </div>
            """, unsafe_allow_html=True)

        # Radar
        radar_data_a = {'score': sA, 'capacity': fA.get('capacity', 0), 'p1_score': fA.get('performer1_performer_score', 0),
                        'p2_score': fA.get('performer2_performer_score', 0), 'is_weekend': fA.get('is_weekend', 0),
                        'is_playoff': fA.get('is_playoff', 0), 'is_evening': fA.get('is_evening', 0)}
        radar_data_b = {'score': sB, 'capacity': fB.get('capacity', 0), 'p1_score': fB.get('performer1_performer_score', 0),
                        'p2_score': fB.get('performer2_performer_score', 0), 'is_weekend': fB.get('is_weekend', 0),
                        'is_playoff': fB.get('is_playoff', 0), 'is_evening': fB.get('is_evening', 0)}
        st.plotly_chart(plot_comparison_radar(radar_data_a, radar_data_b, 'Event A', 'Event B'), use_container_width=True)

        # Winner banner
        if sA > sB:
            st.markdown(render_winner_banner("Event A", sA, sB, sA - sB), unsafe_allow_html=True)
        elif sB > sA:
            st.markdown(render_winner_banner("Event B", sB, sA, sB - sA), unsafe_allow_html=True)
        else:
            st.info("🤝 Both events have identical predicted demand scores.")

        # Key differences
        st.markdown(render_section_header("🔍", "Key Differences"), unsafe_allow_html=True)
        diffs = []
        if fA.get('capacity', 0) != fB.get('capacity', 0):
            diffs.append(f"**Capacity:** A = {fA.get('capacity',0):,} vs B = {fB.get('capacity',0):,}")
        if fA.get('is_playoff', 0) != fB.get('is_playoff', 0):
            diffs.append(f"**Playoff:** A = {'Yes' if fA.get('is_playoff') else 'No'} vs B = {'Yes' if fB.get('is_playoff') else 'No'}")
        if fA.get('is_weekend', 0) != fB.get('is_weekend', 0):
            diffs.append(f"**Weekend:** A = {'Yes' if fA.get('is_weekend') else 'No'} vs B = {'Yes' if fB.get('is_weekend') else 'No'}")
        if fA.get('total_performer_score', 0) != fB.get('total_performer_score', 0):
            diffs.append(f"**Star Power:** A = {fA.get('total_performer_score',0):.2f} vs B = {fB.get('total_performer_score',0):.2f}")

        if diffs:
            diff_cols = st.columns(2)
            for idx, d in enumerate(diffs):
                with diff_cols[idx % 2]:
                    st.markdown(f"- {d}")
        else:
            st.info("No significant differences detected between the two event configurations.")


# =============================================
# PAGE 5: WHAT-IF ANALYSIS
# =============================================
elif page == "🔬 What-If Analysis":
    st.markdown(render_section_header("🔬", "What-If Scenario Analysis"), unsafe_allow_html=True)

    st.markdown("""
    <div style="background:var(--bg-card); border:1px solid var(--border-default);
                border-radius:var(--radius-md); padding:1rem 1.5rem; margin-bottom:1.5rem;
                display:flex; align-items:center; gap:0.75rem;">
        <span style="font-size:1.25rem;">🧪</span>
        <span style="color:var(--text-secondary); font-size:0.9rem;">
            Configure a <strong>baseline event</strong>, then see how the predicted demand
            changes when individual variables are modified.
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📌 Baseline Event Configuration")
    wc1, wc2, wc3 = st.columns(3)
    with wc1:
        w_cat = st.selectbox("Category", options['categories'], key="w_cat")
        w_venue = st.selectbox("Venue", options['venues'], key="w_venue")
    with wc2:
        w_p1 = st.selectbox("Performer 1", options['performers_p1'], key="w_p1")
        w_p2 = st.selectbox("Performer 2", options['performers_p2'], key="w_p2")
    with wc3:
        w_date = st.date_input("Date", datetime.date.today() + datetime.timedelta(days=30), key="w_date")
        w_time = st.time_input("Time", datetime.time(19, 30), key="w_time")
        w_playoff = st.radio("Playoff?", ["No", "Yes"], key="w_pf", horizontal=True)

    if st.button("📊 Run Baseline + Scenarios", use_container_width=True):
        w_is_playoff = 1 if w_playoff == "Yes" else 0

        with st.spinner("Computing baseline and scenarios..."):
            # Baseline
            base_score, base_level, base_conf, base_feat, base_disp, _, _, _, _ = \
                run_prediction(w_cat, w_venue, w_p1, w_p2, w_date, w_time, w_is_playoff)

            # Scenario 1: Flip weekend (find the nearest date that flips the weekend/weekday status)
            alt_date_wk = w_date
            for _guard in range(7):  # Safety: at most 7 days to flip
                alt_date_wk = alt_date_wk + datetime.timedelta(days=1)
                if (alt_date_wk.weekday() >= 5) != (w_date.weekday() >= 5):
                    break
            s1_score, s1_level, _, _, _, _, _, _, _ = run_prediction(w_cat, w_venue, w_p1, w_p2, alt_date_wk, w_time, w_is_playoff)

            # Scenario 2: Flip playoff
            s2_score, s2_level, _, _, _, _, _, _, _ = run_prediction(w_cat, w_venue, w_p1, w_p2, w_date, w_time, 1 - w_is_playoff)

            # Scenario 3: Different venue (pick first different one)
            alt_venues = [v for v in options['venues'] if v != w_venue]
            alt_venue = alt_venues[0] if alt_venues else w_venue
            s3_score, s3_level, _, _, _, _, _, _, _ = run_prediction(w_cat, alt_venue, w_p1, w_p2, w_date, w_time, w_is_playoff)

            # Scenario 4: Morning time
            morning = datetime.time(10, 0)
            s4_score, s4_level, _, _, _, _, _, _, _ = run_prediction(w_cat, w_venue, w_p1, w_p2, w_date, morning, w_is_playoff)

        # Display
        st.markdown("---")
        st.markdown(render_section_header("📊", "Scenario Comparison"), unsafe_allow_html=True)

        # Baseline gauge
        gauge_col, stats_col = st.columns([2, 1])
        with gauge_col:
            st.plotly_chart(plot_gauge_meter(base_score, 'Baseline Demand'), use_container_width=True)
        with stats_col:
            st.markdown(render_result_card("Baseline Score", f"{base_score:.1f}", "#0f62fe", "#0f62fe"), unsafe_allow_html=True)
            st.markdown(render_demand_badge(base_level), unsafe_allow_html=True)

        # Scenario cards
        st.markdown(render_section_header("🧪", "Scenario Results"), unsafe_allow_html=True)

        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown(render_scenario_card("📅", "Flip Weekend/Weekday",
                f"Date → {alt_date_wk}", f"{s1_score:.1f}", s1_level,
                f"{s1_score - base_score:.1f}"), unsafe_allow_html=True)
            st.markdown(render_scenario_card("🏆", "Flip Playoff",
                f"Playoff → {'Yes' if not w_is_playoff else 'No'}", f"{s2_score:.1f}", s2_level,
                f"{s2_score - base_score:.1f}"), unsafe_allow_html=True)
        with sc2:
            st.markdown(render_scenario_card("🏟️", "Change Venue",
                f"Venue → {alt_venue[:35]}", f"{s3_score:.1f}", s3_level,
                f"{s3_score - base_score:.1f}"), unsafe_allow_html=True)
            st.markdown(render_scenario_card("🌅", "Morning Slot",
                "Time → 10:00 AM", f"{s4_score:.1f}", s4_level,
                f"{s4_score - base_score:.1f}"), unsafe_allow_html=True)

        # Biggest impact
        st.markdown("---")
        changes = [('Weekend/Weekday flip', s1_score - base_score), ('Playoff flip', s2_score - base_score),
                    ('Venue change', s3_score - base_score), ('Morning slot', s4_score - base_score)]
        biggest = max(changes, key=lambda x: abs(x[1]))
        delta_color = "#24a148" if biggest[1] >= 0 else "#da1e28"
        st.markdown(f"""
        <div style="background:var(--bg-card); border:1px solid var(--border-default);
                    border-left:4px solid {delta_color}; border-radius:var(--radius-md);
                    padding:1.25rem 1.75rem; display:flex; align-items:center; gap:1rem;">
            <span style="font-size:2rem;">🔑</span>
            <div>
                <div style="font-weight:700; font-size:1rem; color:var(--text-primary);">
                    Biggest Impact: {biggest[0]}
                </div>
                <div style="font-size:0.9rem; color:var(--text-secondary);">
                    Caused a <strong style="color:{delta_color}; font-family:'JetBrains Mono',monospace;">
                    {biggest[1]:+.1f}</strong> point change in demand score.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# =============================================
# PAGE 6: ABOUT PROJECT
# =============================================
elif page == "🎓 About Project":
    st.markdown("""
    <div class="hero-banner">
        <h1>AI-Powered Event Ticket Demand Analysis System</h1>
        <p>IBM Data Science Internship — End-to-End Machine Learning Project</p>
    </div>
    """, unsafe_allow_html=True)

    # Project phases as expanders
    with st.expander("📘 Phase 1: Data Integration & Cleaning", expanded=True):
        st.markdown("""
        **Challenge:** Raw data was fragmented across three separate sources — Events, Performers, and Venues.

        **Solution:**
        - Performed complex Pandas merge operations to join performer statistics and venue capabilities onto event records
        - Handled missing values strategically (e.g., imputing 'No Second Performer' instead of dropping rows)
        - Standardized data types, removed duplicates, and validated referential integrity
        - **Output:** A robust `master_combined_dataset.csv` with **1,385 records × 49 columns**
        """)

    with st.expander("⚙️ Phase 2: Feature Engineering & Target Formulation"):
        st.markdown("""
        **Challenge:** No direct "Tickets Sold" column existed. We needed to engineer a mathematical demand proxy.

        **Demand Score Formula:**
        ```
        Base_Score = Log(P1_Popularity) × 0.35 + Log(P2_Popularity) × 0.15 + Log(Venue_Popularity) × 0.25
        ```

        **Non-Linear Multipliers:**
        - Playoff events → 1.5× boost
        - Weekend events → 1.1× boost

        **Engineered Features:** `total_performer_score`, `pop_to_capacity_ratio`, `is_prime_time`, capacity categories, popularity levels
        """)

    with st.expander("🤖 Phase 3: Machine Learning Model"):
        st.markdown(f"""
        **Algorithm:** Random Forest Regressor (100 trees, max_depth=15)

        **Why Random Forest?**
        - Captures non-linear interactions (e.g., Playoff + Weekend + Large Venue = exponential demand)
        - Built-in feature importance ranking for explainability
        - Robust to outliers and missing data
        - Inter-tree standard deviation provides a natural confidence metric

        **Feature Selection:** Top {len(preprocessor['features'])} features selected from {len(preprocessor['dummy_columns'])} candidates using tree-based importance ranking
        """)

    with st.expander("🧠 Phase 4: Explainable AI & Deployment"):
        st.markdown("""
        **Principle:** AI predictions must be transparent, not black boxes.

        **XAI Implementation:**
        - Per-feature contribution analysis (permutation-based)
        - Business-readable explanations generated from feature importances
        - Confidence scoring via inter-tree prediction variance
        - Actionable business recommendations (pricing, marketing, scheduling)

        **Deployment:** Streamlit enterprise dashboard with modular architecture
        """)

    # Technology Stack
    st.markdown("---")
    st.markdown(render_section_header("🛠️", "Technology Stack"), unsafe_allow_html=True)

    tc1, tc2, tc3, tc4 = st.columns(4)
    with tc1:
        st.markdown(render_kpi_card("Data Processing", "Pandas", "NumPy", "blue"), unsafe_allow_html=True)
    with tc2:
        st.markdown(render_kpi_card("Machine Learning", "Scikit-Learn", "Random Forest", "purple"), unsafe_allow_html=True)
    with tc3:
        st.markdown(render_kpi_card("Visualization", "Plotly", "20+ Charts", "teal"), unsafe_allow_html=True)
    with tc4:
        st.markdown(render_kpi_card("Web Framework", "Streamlit", "Custom CSS", "cyan"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tech badges
    badges = [
        ("🐍", "Python 3.10+"), ("📊", "Pandas"), ("🔢", "NumPy"),
        ("🤖", "Scikit-Learn"), ("📈", "Plotly"), ("🌐", "Streamlit"),
        ("📦", "Joblib"), ("🎨", "Custom CSS"),
    ]
    badge_html = " ".join([render_tech_badge(icon, text) for icon, text in badges])
    st.markdown(f'<div style="display:flex; flex-wrap:wrap; gap:0.5rem;">{badge_html}</div>', unsafe_allow_html=True)
