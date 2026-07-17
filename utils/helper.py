"""
helper.py — Enterprise UI Components & Constants
IBM AI Event Demand Analysis System

Premium design system with dark mode, glassmorphism, micro-animations,
and responsive layouts. All render_* functions produce HTML/CSS only.
"""

# =============================================
# COLOR PALETTE (IBM Carbon Design System)
# =============================================
COLORS = {
    'primary': '#0f62fe',
    'primary_hover': '#0353e9',
    'success': '#24a148',
    'danger': '#da1e28',
    'warning': '#f1c21b',
    'purple': '#8a3ffc',
    'teal': '#009d9a',
    'cyan': '#1192e8',
    'magenta': '#ee5396',
    'dark': '#161616',
    'gray_90': '#262626',
    'gray_70': '#525252',
    'gray_50': '#8d8d8d',
    'gray_30': '#c6c6c6',
    'gray_10': '#f4f4f4',
    'white': '#ffffff',
}

SPORT_ICONS = {
    'nba': '🏀', 'nhl': '🏒', 'mlb': '⚾', 'nfl': '🏈', 'stadium_tours': '🏟️'
}

SPORT_COLORS = {
    'nba': '#C9082A', 'nhl': '#000000', 'mlb': '#002D72',
    'nfl': '#013369', 'stadium_tours': '#8a3ffc'
}

DEMAND_CONFIG = {
    'High Demand': {'color': '#da1e28', 'icon': '🔴', 'bg': '#fff1f1'},
    'Medium Demand': {'color': '#f1c21b', 'icon': '🟡', 'bg': '#fcf4d6'},
    'Low Demand': {'color': '#24a148', 'icon': '🟢', 'bg': '#defbe6'},
}

# =============================================
# GLOBAL CSS — Premium Design System
# =============================================
GLOBAL_CSS = """
<style>
    /* ========================================
       CSS CUSTOM PROPERTIES (THEME TOKENS)
       ======================================== */
    :root {
        /* Surfaces */
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-card: rgba(22,27,34,0.85);
        --bg-card-hover: rgba(30,37,46,0.95);
        --bg-input: #1c2128;
        --bg-elevated: #1c2128;

        /* Text */
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --text-muted: #6e7681;
        --text-inverse: #0d1117;

        /* Borders */
        --border-default: rgba(255,255,255,0.08);
        --border-hover: rgba(255,255,255,0.15);

        /* Accents */
        --accent-blue: #0f62fe;
        --accent-purple: #8a3ffc;
        --accent-teal: #009d9a;
        --accent-cyan: #1192e8;
        --accent-green: #24a148;
        --accent-red: #da1e28;
        --accent-yellow: #f1c21b;
        --accent-magenta: #ee5396;

        /* Gradients */
        --gradient-hero: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 40%, #24243e 100%);
        --gradient-blue: linear-gradient(135deg, #0f62fe, #6979f8);
        --gradient-purple: linear-gradient(135deg, #8a3ffc, #b57bee);
        --gradient-accent: linear-gradient(135deg, #0f62fe 0%, #8a3ffc 50%, #ee5396 100%);

        /* Glass */
        --glass-bg: rgba(22,27,34,0.72);
        --glass-border: rgba(255,255,255,0.08);
        --glass-blur: 16px;

        /* Shadows */
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.3);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.4);
        --shadow-lg: 0 10px 30px rgba(0,0,0,0.5);
        --shadow-glow-blue: 0 0 20px rgba(15,98,254,0.15);
        --shadow-glow-purple: 0 0 20px rgba(138,63,252,0.15);

        /* Radius */
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
        --radius-full: 9999px;

        /* Timing */
        --ease: cubic-bezier(0.4, 0, 0.2, 1);
        --duration: 0.25s;

        /* Sidebar */
        --sidebar-bg: linear-gradient(180deg, #0a0a1a 0%, #111128 50%, #0d0d22 100%);
        --sidebar-text: #c8cad0;
        --sidebar-active-bg: rgba(15,98,254,0.12);
        --sidebar-active-border: #0f62fe;
    }

    /* ========================================
       LIGHT MODE OVERRIDES
       Activated by Streamlit's theme system (config.toml base="light"),
       NOT by browser prefers-color-scheme.
       ======================================== */
    [data-theme='light'] {
        --bg-primary: #f0f2f5;
        --bg-secondary: #ffffff;
        --bg-card: rgba(255,255,255,0.85);
        --bg-card-hover: rgba(255,255,255,0.95);
        --bg-input: #f7f8fa;
        --bg-elevated: #ffffff;
        --text-primary: #0d1117;
        --text-secondary: #525252;
        --text-muted: #8d8d8d;
        --text-inverse: #ffffff;
        --border-default: rgba(0,0,0,0.08);
        --border-hover: rgba(0,0,0,0.15);
        --glass-bg: rgba(255,255,255,0.72);
        --glass-border: rgba(255,255,255,0.25);
        --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.07), 0 2px 4px rgba(0,0,0,0.04);
        --shadow-lg: 0 10px 30px rgba(0,0,0,0.1), 0 4px 8px rgba(0,0,0,0.05);
    }

    /* ========================================
       HIDE STREAMLIT DEFAULTS
       ======================================== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 0;
        max-width: 1400px;
    }

    /* ========================================
       TYPOGRAPHY
       ======================================== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    h1, h2, h3, h4, h5 {
        color: var(--text-color, var(--text-primary));
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    p, span, div, label {
        color: var(--text-color, inherit);
    }

    /* ========================================
       ANIMATIONS
       ======================================== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(16px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 8px rgba(15,98,254,0.3); }
        50% { box-shadow: 0 0 20px rgba(15,98,254,0.5); }
    }
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes countUp {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }
    @keyframes borderGlow {
        0%, 100% { border-color: rgba(15,98,254,0.3); }
        50% { border-color: rgba(15,98,254,0.7); }
    }

    .animate-in {
        animation: fadeInUp 0.5s var(--ease) both;
    }

    /* ========================================
       SIDEBAR
       ======================================== */
    section[data-testid="stSidebar"] {
        background: var(--sidebar-bg);
        min-width: 280px;
        max-width: 280px;
        border-right: 1px solid rgba(255,255,255,0.04);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: var(--sidebar-text) !important;
        font-size: 0.9rem;
        font-weight: 500;
        padding: 0.6rem 1rem;
        border-radius: var(--radius-sm);
        transition: all var(--duration) var(--ease);
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 2px 0;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(255,255,255,0.05);
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label[data-selected="true"] {
        background: var(--sidebar-active-bg);
        border-left: 3px solid var(--sidebar-active-border);
        color: #ffffff !important;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.06);
        margin: 0.75rem 0;
    }

    /* ========================================
       BUTTONS
       ======================================== */
    .stButton > button {
        background: var(--gradient-blue);
        color: white !important;
        border: none;
        border-radius: var(--radius-sm);
        padding: 0.65rem 1.75rem;
        font-weight: 600;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
        transition: all var(--duration) var(--ease);
        box-shadow: var(--shadow-sm);
        letter-spacing: 0.01em;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md), var(--shadow-glow-blue);
        color: white !important;
        border: none;
    }
    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Form Submit */
    .stFormSubmitButton > button {
        background: var(--gradient-accent);
        background-size: 200% 200%;
        animation: gradientShift 4s ease infinite;
        color: white !important;
        border: none;
        border-radius: var(--radius-sm);
        padding: 0.85rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.03em;
        box-shadow: var(--shadow-md);
        transition: all var(--duration) var(--ease);
    }
    .stFormSubmitButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: var(--shadow-lg), 0 0 30px rgba(15,98,254,0.25);
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: var(--bg-card);
        color: var(--text-primary) !important;
        border: 1px solid var(--border-default);
        border-radius: var(--radius-sm);
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all var(--duration) var(--ease);
        backdrop-filter: blur(var(--glass-blur));
    }
    .stDownloadButton > button:hover {
        background: var(--accent-blue);
        color: white !important;
        border-color: var(--accent-blue);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    /* ========================================
       TABS
       ======================================== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: none;
        background: var(--bg-card);
        border-radius: var(--radius-md);
        padding: 4px;
        box-shadow: var(--shadow-sm);
    }
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        background-color: transparent;
        border-radius: var(--radius-sm);
        color: var(--text-secondary);
        font-size: 0.85rem;
        font-weight: 600;
        padding: 0 1.25rem;
        transition: all var(--duration) var(--ease);
        border: none;
        white-space: nowrap;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(15,98,254,0.06);
        color: var(--accent-blue);
    }
    .stTabs [aria-selected="true"] {
        background: var(--gradient-blue) !important;
        color: white !important;
        border-radius: var(--radius-sm) !important;
        border-bottom: none !important;
        box-shadow: var(--shadow-sm);
    }

    /* ========================================
       KPI / METRIC CARDS
       ======================================== */
    .kpi-card {
        background: var(--bg-card);
        backdrop-filter: blur(var(--glass-blur));
        -webkit-backdrop-filter: blur(var(--glass-blur));
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        border: 1px solid var(--border-default);
        border-left: 4px solid var(--accent-blue);
        box-shadow: var(--shadow-sm);
        transition: all var(--duration) var(--ease);
        margin-bottom: 0.75rem;
        animation: fadeInUp 0.5s var(--ease) both;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        opacity: 0;
        transition: opacity var(--duration) var(--ease);
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-lg);
        border-color: var(--border-hover);
    }
    .kpi-card:hover::before { opacity: 1; }

    .kpi-card .kpi-label {
        font-size: 0.7rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .kpi-card .kpi-value {
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1.1;
        font-family: 'JetBrains Mono', 'Inter', monospace;
        animation: countUp 0.6s var(--ease) both;
    }
    .kpi-card .kpi-sub {
        font-size: 0.75rem;
        color: var(--text-muted);
        margin-top: 0.35rem;
        font-weight: 500;
    }

    .kpi-card.blue   { border-left-color: #0f62fe; }
    .kpi-card.purple { border-left-color: #8a3ffc; }
    .kpi-card.green  { border-left-color: #24a148; }
    .kpi-card.red    { border-left-color: #da1e28; }
    .kpi-card.teal   { border-left-color: #009d9a; }
    .kpi-card.cyan   { border-left-color: #1192e8; }

    /* ========================================
       RESULT CARD (Prediction Output)
       ======================================== */
    .result-card {
        background: var(--bg-card);
        backdrop-filter: blur(var(--glass-blur));
        border-radius: var(--radius-lg);
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-default);
        border-top: 4px solid var(--accent-blue);
        transition: all 0.3s var(--ease);
        animation: fadeInUp 0.6s var(--ease) both;
        position: relative;
        overflow: hidden;
    }
    .result-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(15,98,254,0.03), rgba(138,63,252,0.03));
        pointer-events: none;
    }
    .result-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
    }
    .result-card .result-label {
        font-size: 0.75rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        position: relative;
        z-index: 1;
    }
    .result-card .result-value {
        font-size: 2.5rem;
        font-weight: 800;
        line-height: 1.2;
        margin: 0.5rem 0;
        font-family: 'JetBrains Mono', monospace;
        position: relative;
        z-index: 1;
    }

    /* ========================================
       SECTION HEADERS
       ======================================== */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding-bottom: 0.85rem;
        border-bottom: 2px solid transparent;
        border-image: linear-gradient(90deg, var(--accent-blue), var(--accent-purple), transparent) 1;
        margin-bottom: 1.5rem;
        margin-top: 1.25rem;
        animation: fadeIn 0.4s var(--ease) both;
    }
    .section-header h3 {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    /* ========================================
       AUTO-FILL ITEMS
       ======================================== */
    .autofill-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0.85rem;
        background: var(--bg-input);
        border-radius: var(--radius-sm);
        border: 1px solid var(--border-default);
        transition: all var(--duration) var(--ease);
        font-size: 0.85rem;
    }
    .autofill-item:hover {
        background: var(--bg-card-hover);
        border-color: var(--border-hover);
    }
    .autofill-item .label {
        color: var(--text-secondary);
        font-weight: 500;
    }
    .autofill-item .value {
        color: var(--text-primary);
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
    }

    /* ========================================
       HERO BANNER
       ======================================== */
    .hero-banner {
        background: var(--gradient-hero);
        color: white;
        padding: 2.5rem 3rem;
        border-radius: var(--radius-lg);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
        animation: fadeInUp 0.6s var(--ease) both;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle at 30% 50%, rgba(15,98,254,0.12) 0%, transparent 50%),
                    radial-gradient(circle at 70% 50%, rgba(138,63,252,0.08) 0%, transparent 50%);
        animation: gradientShift 8s ease infinite;
        background-size: 200% 200%;
    }
    .hero-banner h1 {
        color: #ffffff;
        font-size: 2.2rem;
        margin-bottom: 0.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.7);
        font-size: 1.05rem;
        margin: 0;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    /* ========================================
       DEMAND BADGE
       ======================================== */
    .demand-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.5rem;
        border-radius: var(--radius-full);
        font-weight: 700;
        font-size: 1rem;
        letter-spacing: 0.03em;
        animation: fadeInUp 0.5s var(--ease) both;
        box-shadow: var(--shadow-sm);
    }

    /* ========================================
       INSIGHT CARD
       ======================================== */
    .insight-card {
        background: var(--bg-card);
        backdrop-filter: blur(var(--glass-blur));
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        border: 1px solid var(--border-default);
        border-left: 4px solid var(--accent-blue);
        box-shadow: var(--shadow-sm);
        margin-bottom: 0.75rem;
        transition: all var(--duration) var(--ease);
        animation: fadeInUp 0.4s var(--ease) both;
    }
    .insight-card:hover {
        transform: translateX(4px);
        box-shadow: var(--shadow-md);
    }
    .insight-card .insight-icon {
        font-size: 1.3rem;
        margin-right: 0.5rem;
    }
    .insight-card .insight-title {
        font-weight: 700;
        font-size: 0.85rem;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    .insight-card .insight-value {
        font-weight: 600;
        font-size: 1rem;
        color: var(--accent-blue);
        font-family: 'JetBrains Mono', monospace;
    }

    /* ========================================
       SCENARIO CARD (What-If)
       ======================================== */
    .scenario-card {
        background: var(--bg-card);
        backdrop-filter: blur(var(--glass-blur));
        border-radius: var(--radius-md);
        padding: 1.25rem 1.5rem;
        border: 1px solid var(--border-default);
        box-shadow: var(--shadow-sm);
        margin-bottom: 0.75rem;
        transition: all var(--duration) var(--ease);
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .scenario-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    .scenario-card .delta-positive {
        color: #24a148;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    .scenario-card .delta-negative {
        color: #da1e28;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ========================================
       TECH BADGE
       ======================================== */
    .tech-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.4rem 1rem;
        background: var(--bg-input);
        border: 1px solid var(--border-default);
        border-radius: var(--radius-full);
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
        transition: all var(--duration) var(--ease);
    }
    .tech-badge:hover {
        background: var(--accent-blue);
        color: white;
        border-color: var(--accent-blue);
    }

    /* ========================================
       TIMELINE STEP
       ======================================== */
    .timeline-step {
        display: flex;
        align-items: flex-start;
        gap: 1.25rem;
        padding: 1.25rem 0;
        position: relative;
        animation: fadeInUp 0.5s var(--ease) both;
    }
    .timeline-step::before {
        content: '';
        position: absolute;
        left: 20px;
        top: 48px;
        bottom: -12px;
        width: 2px;
        background: linear-gradient(180deg, var(--accent-blue), var(--accent-purple));
        opacity: 0.3;
    }
    .timeline-step:last-child::before { display: none; }
    .timeline-step .step-number {
        min-width: 42px;
        height: 42px;
        border-radius: 50%;
        background: var(--gradient-blue);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: var(--shadow-sm);
        flex-shrink: 0;
    }
    .timeline-step .step-content h4 {
        margin: 0 0 0.25rem 0;
        font-size: 1rem;
        font-weight: 700;
    }
    .timeline-step .step-content p {
        margin: 0;
        color: var(--text-secondary);
        font-size: 0.88rem;
        line-height: 1.5;
    }

    /* ========================================
       GLASS PANEL (Generic container)
       ======================================== */
    .glass-panel {
        background: var(--glass-bg);
        backdrop-filter: blur(var(--glass-blur));
        -webkit-backdrop-filter: blur(var(--glass-blur));
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 1.75rem;
        box-shadow: var(--shadow-md);
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.5s var(--ease) both;
    }

    /* ========================================
       VS DIVIDER (Comparison Page)
       ======================================== */
    .vs-divider {
        display: flex;
        align-items: center;
        justify-content: center;
        padding-top: 180px;
    }
    .vs-badge {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background: var(--gradient-accent);
        background-size: 200% 200%;
        animation: gradientShift 3s ease infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 1.1rem;
        color: white;
        box-shadow: 0 0 24px rgba(15,98,254,0.3);
        font-family: 'Inter', sans-serif;
    }

    /* ========================================
       WINNER BANNER
       ======================================== */
    .winner-banner {
        background: linear-gradient(135deg, rgba(36,161,72,0.08), rgba(36,161,72,0.02));
        border: 1px solid rgba(36,161,72,0.2);
        border-radius: var(--radius-md);
        padding: 1.25rem 1.75rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        animation: fadeInUp 0.6s var(--ease) both;
    }
    .winner-banner .trophy { font-size: 2rem; }
    .winner-banner .win-text {
        font-weight: 700;
        font-size: 1.05rem;
        color: var(--text-primary);
    }
    .winner-banner .win-detail {
        font-size: 0.88rem;
        color: var(--text-secondary);
    }

    /* ========================================
       FORM INPUTS
       ======================================== */
    .stSelectbox > div > div,
    .stDateInput > div > div,
    .stTimeInput > div > div {
        border-radius: var(--radius-sm) !important;
        border-color: var(--border-default) !important;
        transition: all var(--duration) var(--ease);
    }
    .stSelectbox > div > div:focus-within,
    .stDateInput > div > div:focus-within,
    .stTimeInput > div > div:focus-within {
        border-color: var(--accent-blue) !important;
        box-shadow: 0 0 0 3px rgba(15,98,254,0.1) !important;
    }

    /* ========================================
       DATAFRAMES
       ======================================== */
    .stDataFrame {
        border-radius: var(--radius-md);
        overflow: hidden;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-default);
    }

    /* ========================================
       CHART CARDS (Analytics Dashboard)
       ======================================== */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--bg-card) !important;
        border: 1px solid #30363d !important;
        border-radius: 8px !important;
        padding: 16px !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08) !important;
    }
    [data-theme='light'] [data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid #e0e0e0 !important;
    }
    .chart-title {
        text-align: left;
        font-size: 13px;
        color: #525252;
        font-weight: 600;
        margin-bottom: 8px;
    }

    /* ========================================
       EXPANDERS
       ======================================== */
    .streamlit-expanderHeader {
        font-weight: 700;
        font-size: 0.95rem;
        border-radius: var(--radius-sm);
    }

    /* ========================================
       RESPONSIVE
       ======================================== */
    @media (max-width: 768px) {
        .hero-banner { padding: 1.5rem; }
        .hero-banner h1 { font-size: 1.5rem; }
        .kpi-card .kpi-value { font-size: 1.5rem; }
        .result-card .result-value { font-size: 2rem; }
        .block-container { padding-left: 1rem; padding-right: 1rem; }
    }
</style>
"""

# =============================================
# REUSABLE HTML COMPONENT GENERATORS
# =============================================

def render_kpi_card(label, value, sub="", color="blue"):
    """Renders a premium glassmorphism KPI metric card."""
    return f"""
    <div class="kpi-card {color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """

def render_result_card(label, value, color="#0f62fe", border_color="#0f62fe"):
    """Renders a large result card for prediction output."""
    return f"""
    <div class="result-card" style="border-top-color: {border_color};">
        <div class="result-label">{label}</div>
        <div class="result-value" style="color: {color};">{value}</div>
    </div>
    """

def render_demand_badge(level):
    """Renders a styled demand level badge with glow."""
    cfg = DEMAND_CONFIG.get(level, DEMAND_CONFIG['Medium Demand'])
    return f"""
    <div class="demand-badge" style="background:{cfg['bg']}; color:{cfg['color']};
                border: 2px solid {cfg['color']};">
        {cfg['icon']} {level.upper()}
    </div>
    """

def render_section_header(icon, title):
    """Renders a styled section header with gradient underline."""
    return f"""
    <div class="section-header">
        <span style="font-size:1.5rem;">{icon}</span>
        <h3>{title}</h3>
    </div>
    """

def render_autofill_item(label, value):
    """Renders a single auto-filled feature row."""
    return f"""
    <div class="autofill-item">
        <span class="label">{label}</span>
        <span class="value">{value}</span>
    </div>
    """

def render_insight_card(icon, title, value, border_color="var(--accent-blue)"):
    """Renders an insight card with icon, title, and highlighted value."""
    return f"""
    <div class="insight-card" style="border-left-color: {border_color};">
        <div>
            <span class="insight-icon">{icon}</span>
            <span class="insight-title">{title}</span>
        </div>
        <div class="insight-value">{value}</div>
    </div>
    """

def render_scenario_card(icon, name, change, score, level, delta_val):
    """Renders a scenario comparison card for What-If analysis."""
    try:
        d = float(delta_val)
        cls = "delta-positive" if d >= 0 else "delta-negative"
        delta_str = f"+{d:.1f}" if d >= 0 else f"{d:.1f}"
    except (ValueError, TypeError):
        cls = ""
        delta_str = str(delta_val)
    return f"""
    <div class="scenario-card">
        <div style="font-size:1.5rem;">{icon}</div>
        <div style="flex:1;">
            <div style="font-weight:700; font-size:0.95rem; color:var(--text-primary);">{name}</div>
            <div style="font-size:0.8rem; color:var(--text-secondary);">{change}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-weight:800; font-size:1.2rem; font-family:'JetBrains Mono',monospace; color:var(--text-primary);">{score}</div>
            <div class="{cls}" style="font-size:0.85rem;">{delta_str}</div>
        </div>
    </div>
    """

def render_timeline_step(number, title, description, delay=0):
    """Renders a timeline step for the About / How-It-Works section."""
    return f"""
    <div class="timeline-step" style="animation-delay: {delay}s;">
        <div class="step-number">{number}</div>
        <div class="step-content">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
    </div>
    """

def render_tech_badge(icon, text):
    """Renders a technology badge pill."""
    return f"""<span class="tech-badge">{icon} {text}</span>"""

def render_winner_banner(winner, score_a, score_b, diff):
    """Renders a winner celebration banner for comparison page."""
    return f"""
    <div class="winner-banner">
        <div class="trophy">🏆</div>
        <div>
            <div class="win-text">{winner} Wins!</div>
            <div class="win-detail">Score: {max(score_a, score_b):.1f} vs {min(score_a, score_b):.1f} — Δ {diff:.1f} points</div>
        </div>
    </div>
    """

def render_vs_badge():
    """Renders the animated VS badge for comparison page."""
    return """
    <div class="vs-divider">
        <div class="vs-badge">VS</div>
    </div>
    """

def render_glass_panel(content_html):
    """Wraps content in a glass-panel container."""
    return f"""<div class="glass-panel">{content_html}</div>"""
