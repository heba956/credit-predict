import streamlit as st

st.set_page_config(
    page_title="Credit Lens",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── UNIVERSAL BACKGROUND — same on every page ── */
html, body, [class*="css"], .stApp, .main, .block-container {
    background-color: #0A0A0F !important;
    color: #D8D8E8 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: #0A0A0F !important;
    border-right: 1px solid #16161F !important;
}
section[data-testid="stSidebar"] * { color: #555570 !important; }

/* ── HEADINGS ── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.5px;
}
h1 { color: #EEEEF8 !important; font-weight: 800 !important; }
h2 { color: #C0C0D8 !important; font-weight: 700 !important; }
h3 { color: #8888A8 !important; font-weight: 600 !important; }

/* ── METRIC CARDS ── */
[data-testid="metric-container"] {
    background: #10101A !important;
    border: 1px solid #1A1A28 !important;
    border-radius: 8px !important;
    padding: 18px !important;
}
[data-testid="metric-container"] label {
    color: #444460 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #EEEEF8 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #10101A !important;
    color: #D8D8E8 !important;
    border: 1px solid #252535 !important;
    border-radius: 4px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    border-color: #00E5A0 !important;
    color: #00E5A0 !important;
    box-shadow: 0 0 20px rgba(0,229,160,0.12) !important;
}

/* ── SLIDERS ── */
.stSlider > div > div > div > div { background: #00E5A0 !important; }
.stSlider > div > div > div { background: #1A1A28 !important; }

/* ── SELECT + INPUT ── */
.stSelectbox > div > div, .stTextInput > div > div {
    background: #10101A !important;
    border-color: #1A1A28 !important;
    color: #D8D8E8 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── CHECKBOX ── */
.stCheckbox label { color: #666688 !important; font-size: 0.8rem !important; }

/* ── RADIO ── */
.stRadio label { color: #666688 !important; font-size: 0.8rem !important; }

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid #1A1A28 !important;
    border-radius: 6px !important;
}

/* ── DIVIDER ── */
hr { border-color: #16161F !important; margin: 28px 0 !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0A0A0F !important;
    border-bottom: 1px solid #16161F !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #444460 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 10px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #00E5A0 !important;
    border-bottom: 2px solid #00E5A0 !important;
    background: transparent !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: #0A0A0F; }
::-webkit-scrollbar-thumb { background: #1A1A28; border-radius: 2px; }

/* ── PAGE LINKS IN SIDEBAR ── */
[data-testid="stSidebarNav"] a {
    color: #444460 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 1px !important;
}
[data-testid="stSidebarNav"] a:hover { color: #00E5A0 !important; }

/* ── CAPTION ── */
.stCaption { color: #333348 !important; font-size: 0.65rem !important; }
</style>
""", unsafe_allow_html=True)

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 12px 0 32px 0'>
        <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;
                    color:#EEEEF8;letter-spacing:-1px;line-height:1.1'>
            CREDIT<br>LENS
        </div>
        <div style='font-family:DM Mono,monospace;font-size:0.6rem;
                    color:#252535;letter-spacing:3px;margin-top:6px'>
            ◈ ML PROJECT
        </div>
    </div>
    <div style='width:100%;height:1px;background:#16161F;margin-bottom:24px'></div>
    <div style='font-family:DM Mono,monospace;font-size:0.6rem;
                color:#252535;letter-spacing:3px;margin-bottom:16px'>
        NAVIGATE
    </div>
    """, unsafe_allow_html=True)

    st.page_link("app.py",                  label="◈  Home")
    st.page_link("pages/1_story.py",        label="▸  The Story")
    st.page_link("pages/2_explore.py",      label="▸  Explore")
    st.page_link("pages/3_predictor.py",    label="▸  Predictor")
    st.page_link("pages/4_insights.py",     label="▸  Insights")

    st.markdown("""
    <div style='width:100%;height:1px;background:#16161F;margin-top:32px;margin-bottom:16px'></div>
    <div style='font-family:DM Mono,monospace;font-size:0.58rem;color:#1E1E2C;line-height:2'>
        13,482 profiles<br>
        LightGBM classifier<br>
        6 engineered features
    </div>
    """, unsafe_allow_html=True)

# ── HOME ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:48px 0 8px 0'>
    <div style='font-family:DM Mono,monospace;font-size:0.6rem;
                color:#252535;letter-spacing:4px;margin-bottom:16px'>
        A MACHINE LEARNING PROJECT
    </div>
    <div style='font-family:Syne,sans-serif;font-size:3.5rem;font-weight:800;
                color:#EEEEF8;line-height:1;letter-spacing:-2px'>
        CREDIT<br>LENS
    </div>
    <div style='display:flex;gap:0;margin:20px 0 24px 0'>
        <div style='width:40px;height:3px;background:#00E5A0'></div>
        <div style='width:20px;height:3px;background:#FFD166'></div>
        <div style='width:10px;height:3px;background:#FF4D6D'></div>
    </div>
    <p style='color:#444460;max-width:520px;line-height:1.9;
              font-family:DM Mono,monospace;font-size:0.82rem'>
        A machine learning system trained on 13,482 credit profiles
        to classify financial health into three tiers —
        Good, Standard, and Poor — using behavioural and financial signals.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Profiles",    "13,482")
c2.metric("Features",    "35",        delta="after engineering")
c3.metric("Tiers",       "3",         delta="Good · Standard · Poor")
c4.metric("Algorithm",   "LightGBM")

st.markdown("<br>", unsafe_allow_html=True)

# Tier cards
st.markdown("""
<div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin-top:8px'>
    <div style='background:#10101A;border:1px solid #00E5A0;border-radius:8px;padding:24px'>
        <div style='font-family:DM Mono,monospace;font-size:0.58rem;
                    color:#00E5A0;letter-spacing:4px;margin-bottom:10px'>GOOD</div>
        <div style='font-family:Syne,sans-serif;font-size:2rem;
                    font-weight:800;color:#00E5A0'>17.8%</div>
        <div style='font-family:DM Mono,monospace;font-size:0.72rem;
                    color:#1A3328;margin-top:8px;line-height:1.8'>
            &lt;5 missed payments<br>
            Low debt burden<br>
            Long credit history
        </div>
    </div>
    <div style='background:#10101A;border:1px solid #FFD166;border-radius:8px;padding:24px'>
        <div style='font-family:DM Mono,monospace;font-size:0.58rem;
                    color:#FFD166;letter-spacing:4px;margin-bottom:10px'>STANDARD</div>
        <div style='font-family:Syne,sans-serif;font-size:2rem;
                    font-weight:800;color:#FFD166'>52.5%</div>
        <div style='font-family:DM Mono,monospace;font-size:0.72rem;
                    color:#332E1A;margin-top:8px;line-height:1.8'>
            ~7 missed payments<br>
            Moderate debt<br>
            Average history
        </div>
    </div>
    <div style='background:#10101A;border:1px solid #FF4D6D;border-radius:8px;padding:24px'>
        <div style='font-family:DM Mono,monospace;font-size:0.58rem;
                    color:#FF4D6D;letter-spacing:4px;margin-bottom:10px'>POOR</div>
        <div style='font-family:Syne,sans-serif;font-size:2rem;
                    font-weight:800;color:#FF4D6D'>29.6%</div>
        <div style='font-family:DM Mono,monospace;font-size:0.72rem;
                    color:#331A20;margin-top:8px;line-height:1.8'>
            &gt;15 missed payments<br>
            High debt burden<br>
            Short history
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<br>
<div style='font-family:DM Mono,monospace;font-size:0.6rem;
            color:#1E1E2C;text-align:center;letter-spacing:3px'>
    USE THE SIDEBAR TO NAVIGATE
</div>
""", unsafe_allow_html=True)
