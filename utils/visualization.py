"""
visualization.py — Professional Plotly Visualizations
IBM AI Event Demand Analysis System

Contains 20+ chart functions for the analytics dashboard.
All charts use a consistent premium color palette with polished styling.
No data logic or computation changes — only visual presentation.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Consistent palette
IBM_BLUE = '#0f62fe'
IBM_PURPLE = '#8a3ffc'
IBM_TEAL = '#009d9a'
IBM_CYAN = '#1192e8'
IBM_GREEN = '#24a148'
IBM_RED = '#da1e28'
IBM_MAGENTA = '#ee5396'
PALETTE = [IBM_BLUE, IBM_PURPLE, IBM_TEAL, IBM_CYAN, IBM_GREEN, IBM_RED, IBM_MAGENTA, '#f1c21b', '#002d9c', '#570408']

LAYOUT_DEFAULTS = dict(
    font=dict(family='Inter, -apple-system, BlinkMacSystemFont, sans-serif', color='#e6edf3', size=12),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=24, r=24, t=56, b=24),
    title_font=dict(size=15, color='#e6edf3', family='Inter, sans-serif'),
    title_x=0.0,
    title_xanchor='left',
    hoverlabel=dict(
        bgcolor='#1c2128',
        font_size=12,
        font_family='Inter, sans-serif',
        font_color='#ffffff',
        bordercolor='rgba(255,255,255,0.1)',
    ),
    legend=dict(
        font=dict(size=11, color='#8b949e'),
        bgcolor='rgba(22,27,34,0.6)',
        bordercolor='rgba(255,255,255,0.05)',
        borderwidth=1,
    ),
    modebar=dict(
        bgcolor='rgba(0,0,0,0)',
        color='#8d8d8d',
        activecolor='#0f62fe',
    ),
)

AXIS_STYLE = dict(
    showgrid=True,
    gridwidth=1,
    gridcolor='rgba(255,255,255,0.06)',
    zeroline=False,
    linewidth=1,
    linecolor='rgba(255,255,255,0.1)',
    title_font=dict(size=12, color='#8b949e'),
    tickfont=dict(size=11, color='#8b949e'),
)

CONFIG_OPTIONS = dict(
    displayModeBar=True,
    modeBarButtonsToRemove=['lasso2d', 'select2d', 'autoScale2d'],
    displaylogo=False,
)


def _apply_layout(fig, **kwargs):
    """Applies consistent layout to a figure."""
    fig.update_layout(**LAYOUT_DEFAULTS, **kwargs)
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


# =============================================
# 1. EVENT CATEGORY ANALYSIS
# =============================================

def plot_events_by_category(df):
    """Horizontal bar chart of event counts by sport category."""
    counts = df['sport_type'].value_counts().reset_index()
    counts.columns = ['Category', 'Count']
    fig = px.bar(counts, x='Count', y='Category', orientation='h',
                 color='Category', color_discrete_sequence=PALETTE,
                 title='Events by Category')
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig, height=300)


def plot_demand_score_distribution(df):
    """Histogram with KDE overlay for demand score distribution."""
    fig = px.histogram(df, x='Demand_Score', nbins=30, marginal='box',
                       color_discrete_sequence=[IBM_BLUE],
                       title='Demand Score Distribution')
    fig.update_layout(xaxis_title='Demand Score', yaxis_title='Count')
    fig.update_traces(marker_line_width=0, opacity=0.85)
    return _apply_layout(fig)


def plot_demand_level_donut(df):
    """Donut chart of demand levels."""
    counts = df['Demand_Level'].value_counts().reset_index()
    counts.columns = ['Level', 'Count']
    color_map = {'High Demand': IBM_RED, 'Medium Demand': '#f1c21b', 'Low Demand': IBM_GREEN}
    fig = px.pie(counts, names='Level', values='Count', hole=0.55,
                 color='Level', color_discrete_map=color_map,
                 title='Demand Level Distribution')
    fig.update_traces(
        textposition='outside', textinfo='percent+label',
        textfont=dict(size=12, family='Inter'),
        marker=dict(line=dict(color='white', width=2)),
        pull=[0.03, 0, 0],
    )
    return _apply_layout(fig)


# =============================================
# 2. VENUE ANALYSIS
# =============================================

def plot_capacity_boxplot(df):
    """Box plot of venue capacity grouped by sport type."""
    fig = px.box(df, x='sport_type', y='capacity', color='sport_type',
                 color_discrete_sequence=PALETTE,
                 title='Venue Capacity Distribution by Category')
    fig.update_layout(showlegend=False, xaxis_title='Category', yaxis_title='Capacity')
    return _apply_layout(fig)


def plot_venue_popularity_violin(df):
    """Violin plot of venue popularity by category."""
    fig = px.violin(df, x='sport_type', y='venue_popularity', box=True,
                    color='sport_type', color_discrete_sequence=PALETTE,
                    title='Venue Popularity Distribution by Category')
    fig.update_layout(showlegend=False)
    return _apply_layout(fig)


def plot_top_venues(df, n=10):
    """Bar chart of top N venues by popularity."""
    top = df.drop_duplicates('venue_name').nlargest(n, 'venue_popularity')[['venue_name', 'venue_popularity', 'capacity']]
    
    if top.empty or top['venue_popularity'].sum() == 0:
        return None
        
    fig = px.bar(top, x='venue_popularity', y='venue_name', orientation='h',
                 color_discrete_sequence=[IBM_CYAN],
                 hover_data=['capacity'],
                 title=f'Top {n} Venues by Popularity')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


def plot_capacity_treemap(df):
    """Treemap of capacity levels by sport type."""
    agg = df.groupby(['sport_type', 'capacity_level']).size().reset_index(name='count')
    fig = px.treemap(agg, path=['sport_type', 'capacity_level'], values='count',
                     color='count', color_continuous_scale='Blues',
                     title='Capacity Level Breakdown')
    fig.update_traces(marker_line_width=1, marker_line_color='white')
    return _apply_layout(fig)


# =============================================
# 3. PERFORMER ANALYSIS
# =============================================

def plot_top_performers(df, n=10):
    """Bar chart of top N performers by popularity."""
    top = df.drop_duplicates('performer1_name').nlargest(n, 'performer1_performer_popularity')[
        ['performer1_name', 'performer1_performer_popularity', 'sport_type']]
    fig = px.bar(top, x='performer1_performer_popularity', y='performer1_name', orientation='h',
                 color='sport_type', color_discrete_sequence=PALETTE,
                 title=f'Top {n} Performers by Popularity')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


def plot_performer_score_vs_demand(df):
    """Scatter plot of performer score vs demand."""
    fig = px.scatter(df, x='total_performer_score', y='Demand_Score',
                     color='sport_type', color_discrete_sequence=PALETTE,
                     opacity=0.55, title='Performer Star Power vs Demand',
                     hover_data=['performer1_name', 'venue_name'])
    fig.update_layout(xaxis_title='Total Performer Score', yaxis_title='Demand Score')
    fig.update_traces(marker=dict(size=7, line=dict(width=0.5, color='white')))
    return _apply_layout(fig)


# =============================================
# 4. TEMPORAL ANALYSIS
# =============================================

def plot_monthly_trends(df):
    """Line chart of average demand by month."""
    monthly = df.groupby('event_month')['Demand_Score'].mean().reset_index()
    monthly.columns = ['Month', 'Avg Demand Score']
    fig = px.line(monthly, x='Month', y='Avg Demand Score', markers=True,
                  color_discrete_sequence=[IBM_BLUE],
                  title='Monthly Demand Trends')
    fig.update_layout(xaxis=dict(dtick=1))
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=10, line=dict(width=2, color='white')),
    )
    return _apply_layout(fig)


def plot_weekday_distribution(df):
    """Bar chart of events by day of week."""
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    counts = df['event_day_name'].value_counts().reindex(day_order).reset_index()
    counts.columns = ['Day', 'Count']
    fig = px.bar(counts, x='Day', y='Count', color='Count',
                 color_continuous_scale='Blues',
                 title='Events by Day of Week')
    fig.update_layout(coloraxis_showscale=False)
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


def plot_weekend_donut(df):
    """Donut chart of weekend vs weekday."""
    counts = df['is_weekend'].value_counts().reset_index()
    counts.columns = ['Type', 'Count']
    counts['Type'] = counts['Type'].map({0: 'Weekday', 1: 'Weekend'})
    fig = px.pie(counts, names='Type', values='Count', hole=0.55,
                 color_discrete_sequence=[IBM_BLUE, IBM_PURPLE],
                 title='Weekend vs Weekday Events')
    fig.update_traces(
        textposition='outside', textinfo='percent+label',
        marker=dict(line=dict(color='white', width=2)),
    )
    return _apply_layout(fig)


def plot_playoff_impact(df):
    """Grouped bar chart comparing demand by playoff status."""
    agg = df.groupby(['sport_type', 'is_playoff'])['Demand_Score'].mean().reset_index()
    agg['Playoff'] = agg['is_playoff'].map({0: 'Regular', 1: 'Playoff'})
    fig = px.bar(agg, x='sport_type', y='Demand_Score', color='Playoff',
                 barmode='group', color_discrete_sequence=[IBM_BLUE, IBM_RED],
                 title='Playoff Impact on Demand Score')
    fig.update_layout(xaxis_title='Category', yaxis_title='Avg Demand Score')
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


def plot_hour_month_heatmap(df):
    """Density heatmap of events by hour and month."""
    fig = px.density_heatmap(df, x='event_month', y='event_hour',
                             z='Demand_Score', histfunc='avg',
                             color_continuous_scale='Viridis',
                             title='Demand Hotspots (Month × Hour)',
                             nbinsx=12, nbinsy=24)
    fig.update_layout(xaxis_title='Month', yaxis_title='Hour of Day')
    return _apply_layout(fig)


# =============================================
# 5. CAPACITY & DEMAND ANALYSIS
# =============================================

def plot_capacity_vs_demand(df):
    """Scatter plot of capacity vs demand score."""
    fig = px.scatter(df, x='capacity', y='Demand_Score',
                     color='sport_type', size='venue_popularity',
                     color_discrete_sequence=PALETTE, opacity=0.55,
                     title='Venue Capacity vs Demand Score',
                     hover_data=['venue_name', 'performer1_name'])
    fig.update_traces(marker=dict(line=dict(width=0.5, color='white')))
    return _apply_layout(fig)


# =============================================
# 6. ADVANCED ANALYTICS
# =============================================

def plot_sunburst(df):
    """Sunburst chart: Category → Weekend → Playoff."""
    sb = df.copy()
    sb['Weekend'] = sb['is_weekend'].map({0: 'Weekday', 1: 'Weekend'})
    sb['Playoff'] = sb['is_playoff'].map({0: 'Regular', 1: 'Playoff'})
    agg = sb.groupby(['sport_type', 'Weekend', 'Playoff']).size().reset_index(name='count')
    fig = px.sunburst(agg, path=['sport_type', 'Weekend', 'Playoff'], values='count',
                      color='count', color_continuous_scale='Blues',
                      title='Event Hierarchy: Category → Timing → Playoff')
    return _apply_layout(fig)


def plot_3d_scatter(df):
    """3D scatter: Capacity × Star Power × Demand."""
    fig = px.scatter_3d(df, x='capacity', y='total_performer_score', z='Demand_Score',
                        color='sport_type', color_discrete_sequence=PALETTE,
                        opacity=0.65, title='3D: Capacity × Star Power × Demand',
                        hover_data=['venue_name', 'performer1_name'])
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=48),
        scene=dict(
            xaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(0,0,0,0.06)'),
            yaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(0,0,0,0.06)'),
            zaxis=dict(backgroundcolor='rgba(0,0,0,0)', gridcolor='rgba(0,0,0,0.06)'),
        ),
    )
    return _apply_layout(fig, height=500)


def plot_state_distribution(df):
    """Bar chart of events by state."""
    counts = df['state'].value_counts().head(15).reset_index()
    counts.columns = ['State', 'Count']
    fig = px.bar(counts, x='Count', y='State', orientation='h',
                 color='Count', color_continuous_scale='Blues',
                 title='Top 15 States by Event Count')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


def plot_demand_by_category(df):
    """Bar chart comparing average demand across categories."""
    agg = df.groupby('sport_type')['Demand_Score'].agg(['mean', 'std']).reset_index()
    agg.columns = ['Category', 'Mean', 'Std']
    fig = px.bar(agg, x='Category', y='Mean', error_y='Std',
                 color='Category', color_discrete_sequence=PALETTE,
                 title='Average Demand Score by Category')
    fig.update_layout(showlegend=False)
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


# =============================================
# 7. MODEL EXPLAINABILITY
# =============================================

def plot_feature_importance(importance_records, n=15):
    """Horizontal bar chart of top feature importances."""
    df = pd.DataFrame(importance_records)
    df = df.head(n)
    fig = px.bar(df, x='Importance', y='Feature', orientation='h',
                 color='Importance', color_continuous_scale='Purples',
                 title=f'Top {n} Feature Importances (Random Forest)')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False)
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


def plot_correlation_heatmap(df):
    """Correlation heatmap of numerical features."""
    num_df = df.select_dtypes(include=[np.number])
    drop_cols = [c for c in num_df.columns if 'Id' in c or 'year' in c]
    num_df = num_df.drop(columns=drop_cols, errors='ignore')
    corr = num_df.corr()
    fig = px.imshow(corr, text_auto='.2f', aspect='auto',
                    color_continuous_scale='RdBu_r',
                    title='Feature Correlation Heatmap')
    return _apply_layout(fig, height=500)


def plot_feature_contributions(contrib_df):
    """Horizontal bar chart of per-feature contributions for a specific prediction."""
    if contrib_df.empty:
        fig = go.Figure()
        fig.add_annotation(text="No contribution data available", showarrow=False,
                           font=dict(size=14, color='#8d8d8d'))
        return _apply_layout(fig, height=300)

    fig = px.bar(contrib_df.head(8), x='Contribution_Pct', y='Feature', orientation='h',
                 color='Contribution_Pct', color_continuous_scale='Oranges',
                 title='Feature Contributions to This Prediction')
    fig.update_layout(yaxis={'categoryorder': 'total ascending'}, coloraxis_showscale=False,
                      xaxis_title='Contribution (%)')
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_layout(fig)


# =============================================
# 8. GAUGE METER
# =============================================

def plot_gauge_meter(score, title='Demand Score'):
    """Plotly indicator gauge for demand score — premium styled."""
    if score >= 66:
        bar_color = IBM_RED
    elif score >= 33:
        bar_color = '#f1c21b'
    else:
        bar_color = IBM_GREEN

    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=score,
        number={
            'font': {'size': 52, 'color': '#e6edf3', 'family': 'JetBrains Mono, monospace'},
            'suffix': '<span style="font-size:18px;color:#8b949e;"> / 100</span>',
        },
        title={'text': title, 'font': {'size': 15, 'color': '#8b949e', 'family': 'Inter, sans-serif'}},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1.5,
                'tickcolor': '#6e7681',
                'dtick': 20,
                'tickfont': {'size': 10, 'color': '#8b949e'},
            },
            'bar': {'color': bar_color, 'thickness': 0.35},
            'bgcolor': '#1c2128',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 33], 'color': 'rgba(36,161,72,0.15)'},
                {'range': [33, 66], 'color': 'rgba(241,194,27,0.15)'},
                {'range': [66, 100], 'color': 'rgba(218,30,40,0.15)'},
            ],
            'threshold': {
                'line': {'color': '#e6edf3', 'width': 3},
                'thickness': 0.8,
                'value': score,
            },
        },
    ))
    fig.update_layout(
        height=280,
        margin=dict(l=30, r=30, t=64, b=16),
        font=dict(family='Inter, sans-serif'),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    return fig


# =============================================
# 9. COMPARISON CHARTS
# =============================================

def plot_comparison_radar(event_a, event_b, label_a='Event A', label_b='Event B'):
    """Radar chart comparing two events across key dimensions — polished."""
    categories = ['Demand Score', 'Capacity (k)', 'P1 Score', 'P2 Score',
                  'Weekend', 'Playoff', 'Evening']

    vals_a = [
        event_a.get('score', 0),
        event_a.get('capacity', 0) / 1000,
        event_a.get('p1_score', 0) * 100,
        event_a.get('p2_score', 0) * 100,
        event_a.get('is_weekend', 0) * 100,
        event_a.get('is_playoff', 0) * 100,
        event_a.get('is_evening', 0) * 100,
    ]
    vals_b = [
        event_b.get('score', 0),
        event_b.get('capacity', 0) / 1000,
        event_b.get('p1_score', 0) * 100,
        event_b.get('p2_score', 0) * 100,
        event_b.get('is_weekend', 0) * 100,
        event_b.get('is_playoff', 0) * 100,
        event_b.get('is_evening', 0) * 100,
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals_a + [vals_a[0]], theta=categories + [categories[0]],
        name=label_a, line=dict(color=IBM_BLUE, width=2.5),
        fill='toself', fillcolor='rgba(15,98,254,0.12)', opacity=0.9,
    ))
    fig.add_trace(go.Scatterpolar(
        r=vals_b + [vals_b[0]], theta=categories + [categories[0]],
        name=label_b, line=dict(color=IBM_RED, width=2.5),
        fill='toself', fillcolor='rgba(218,30,40,0.12)', opacity=0.9,
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, gridcolor='rgba(0,0,0,0.06)', linecolor='rgba(0,0,0,0.08)'),
            angularaxis=dict(gridcolor='rgba(0,0,0,0.06)', linecolor='rgba(0,0,0,0.08)'),
            bgcolor='rgba(0,0,0,0)',
        ),
        title='Event Comparison Radar',
        legend=dict(orientation='h', yanchor='bottom', y=-0.15, xanchor='center', x=0.5),
    )
    return _apply_layout(fig, height=420)
