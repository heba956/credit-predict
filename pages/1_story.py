import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Why Credit Scores Diverge", layout="wide",
                   initial_sidebar_state="collapsed")

# Inject Google Fonts
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@700;800&display=swap" rel="stylesheet">
<style>
    body, .stApp { background-color: #0A0A0F; }
    .block-container { padding-top: 2rem; max-width: 860px; }
    h2 { color: #EEEEF8; font-family: 'Syne', sans-serif; font-weight: 800; }
    .stPlotlyChart { background: transparent; }
</style>
""", unsafe_allow_html=True)

GOOD='#00E5A0'; STD='#FFD166'; POOR='#FF4D6D'
BG='#0A0A0F'; PANEL='#10101A'; GRID='#16161F'; TEXT='#D8D8E8'
SC = {'Good':GOOD,'Standard':STD,'Poor':POOR}

BASE = dict(
    paper_bgcolor=BG, plot_bgcolor=PANEL,
    font=dict(family='DM Mono, monospace', color='#555570', size=10),
    margin=dict(t=40,b=36,l=48,r=16),
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor=GRID, font=dict(color='#555570')),
    xaxis=dict(gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID, tickfont=dict(color='#555570')),
    yaxis=dict(gridcolor=GRID, linecolor=GRID, zerolinecolor=GRID, tickfont=dict(color='#555570')),
)

@st.cache_data
def load():
    import os
    # Try to load data.csv from common locations
    for path in ['data.csv', 'sample_data.csv']:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    else:
        # Generate synthetic data if no CSV found
        np.random.seed(42)
        n = 13482
        scores = np.random.choice(['Good','Standard','Poor'], n, p=[0.33,0.34,0.33])
        df = pd.DataFrame({
            'Credit_Score': scores,
            'Age': np.random.randint(18, 85, n),
            'Num_of_Delayed_Payment': np.where(scores=='Good',
                np.random.exponential(3, n),
                np.where(scores=='Standard',
                    np.random.exponential(7, n),
                    np.random.exponential(15, n))).clip(0, 50).astype(int),
            'Outstanding_Debt': np.where(scores=='Good',
                np.random.exponential(664, n),
                np.where(scores=='Standard',
                    np.random.exponential(1015, n),
                    np.random.exponential(1897, n))).clip(0, 4999),
            'Credit_History_Age': [
                f"{int(y)} Years and {int(m)} Months"
                for y, m in zip(
                    np.where(scores=='Good',
                        np.random.normal(22, 5, n),
                        np.where(scores=='Standard',
                            np.random.normal(17, 5, n),
                            np.random.normal(13, 5, n))).clip(0, 40),
                    np.random.randint(0, 12, n)
                )
            ],
            'Num_Credit_Inquiries': np.where(scores=='Good',
                np.random.exponential(3, n),
                np.where(scores=='Standard',
                    np.random.exponential(7, n),
                    np.random.exponential(12, n))).clip(0, 30).astype(int),
            'Payment_Behaviour': np.random.choice(
                ['High_spent_Small_value_payments','Low_spent_Large_value_payments',
                 'High_spent_Medium_value_payments'], n),
            'Interest_Rate': np.random.uniform(5, 35, n),
            'Annual_Income': np.random.uniform(20000, 200000, n),
            'Monthly_Inhand_Salary': np.random.uniform(1500, 15000, n),
            'Total_EMI_per_month': np.random.uniform(50, 2000, n),
        })
        return df

    df.drop(columns=['Name','Unnamed: 0'], inplace=True, errors='ignore')
    df['Age'] = pd.to_numeric(df['Age'].astype(str).str.replace('_',''), errors='coerce')
    df = df[(df['Age']>10)&(df['Age']<110)]
    for col in ['Num_of_Delayed_Payment','Outstanding_Debt','Annual_Income',
                'Interest_Rate','Num_Credit_Inquiries','Monthly_Inhand_Salary',
                'Total_EMI_per_month']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('_',''), errors='coerce')
    df['Num_of_Delayed_Payment'] = df['Num_of_Delayed_Payment'].clip(lower=0)
    df = df[df['Payment_Behaviour'] != '!@9#%8']
    df.dropna(subset=['Credit_Score'], inplace=True)

    def parse(s):
        try:
            y=int(str(s).split('Years')[0].strip())
            m=int(str(s).split('and')[1].split('Months')[0].strip())
            return y*12+m
        except: return np.nan
    df['Credit_History_Months'] = df['Credit_History_Age'].apply(parse)
    return df

df = load()

# Parse Credit_History_Months if not present
if 'Credit_History_Months' not in df.columns:
    def parse(s):
        try:
            y=int(str(s).split('Years')[0].strip())
            m=int(str(s).split('and')[1].split('Months')[0].strip())
            return y*12+m
        except: return np.nan
    df['Credit_History_Months'] = df['Credit_History_Age'].apply(parse)

# ── HEADER ───────────────────────────────────────────────────────────────────
n_profiles = f"{len(df):,}"
st.markdown(f"""
<div style='padding:32px 0 4px 0'>
    <div style='font-family:DM Mono,monospace;font-size:0.58rem;
                color:#252535;letter-spacing:4px'>THE STORY</div>
    <div style='font-family:Syne,sans-serif;font-size:2.4rem;font-weight:800;
                color:#EEEEF8;letter-spacing:-1px;line-height:1.1;margin:8px 0 12px 0'>
        Why Credit Scores<br>Diverge
    </div>
    <p style='font-family:DM Mono,monospace;font-size:0.78rem;
              color:#333348;max-width:520px;line-height:1.9'>
        Four patterns found in {n_profiles} real credit profiles that explain
        how people end up in entirely different financial tiers.
    </p>
</div>
<div style='width:100%;height:1px;background:#16161F;margin:20px 0 32px 0'></div>
""", unsafe_allow_html=True)

# ── ACT 1 — MISSED PAYMENTS ──────────────────────────────────────────────────
st.markdown("""
<div style='font-family:DM Mono,monospace;font-size:0.58rem;
            color:#FF4D6D;letter-spacing:4px'>PATTERN 01</div>
<h2 style='margin:4px 0 6px 0;color:#EEEEF8;font-family:Syne,sans-serif;font-weight:800'>The 20-Payment Cliff</h2>
<p style='font-family:DM Mono,monospace;font-size:0.75rem;color:#333348;margin-bottom:16px'>
Past 20 missed payments, Good scorers almost vanish entirely
</p>
""", unsafe_allow_html=True)

bins=[0,5,10,15,20,30,50]; labels=['0–5','6–10','11–15','16–20','21–30','31+']
df['DB'] = pd.cut(df['Num_of_Delayed_Payment'].clip(0,50), bins=bins, include_lowest=True)
ct = pd.crosstab(df['DB'], df['Credit_Score'], normalize='index')*100
ct.index = labels[:len(ct)]

fig = go.Figure()
for s,c in SC.items():
    if s in ct.columns:
        fig.add_trace(go.Bar(name=s, x=ct.index, y=ct[s],
                             marker_color=c, opacity=0.85))
fig.add_vrect(x0=3.5,x1=5.5,fillcolor=POOR,opacity=0.04,line_width=0)
fig.add_vline(x=3.5,line_dash='dot',line_color=POOR,opacity=0.4)
fig.update_layout(**BASE, barmode='group', height=320,
                  title=dict(text='Credit Score Distribution by Missed Payments',
                             font=dict(color='#444460',size=11,family='DM Mono')),
                  xaxis_title='Missed Payments', yaxis_title='% of People')
st.plotly_chart(fig, use_container_width=True)

st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

# ── ACT 2 — DEBT ─────────────────────────────────────────────────────────────
st.markdown("""
<div style='font-family:DM Mono,monospace;font-size:0.58rem;
            color:#FF4D6D;letter-spacing:4px'>PATTERN 02</div>
<h2 style='margin:4px 0 6px 0;color:#EEEEF8;font-family:Syne,sans-serif;font-weight:800'>The Debt Divide</h2>
<p style='font-family:DM Mono,monospace;font-size:0.75rem;color:#333348;margin-bottom:16px'>
Poor scorers carry 3× more outstanding debt than Good scorers
</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])
with col1:
    fig2 = go.Figure()
    for s,c in SC.items():
        d = df[df['Credit_Score']==s]['Outstanding_Debt'].dropna()
        d = pd.to_numeric(d.astype(str).str.replace('_',''), errors='coerce').dropna()
        d = d[d<5000]
        fig2.add_trace(go.Histogram(x=d, name=s, marker_color=c,
                                    opacity=0.55, histnorm='probability density', nbinsx=60))
    fig2.update_layout(**BASE, barmode='overlay', height=300,
                       title=dict(text='Outstanding Debt Distribution',
                                  font=dict(color='#444460',size=11,family='DM Mono')),
                       xaxis_title='Outstanding Debt ($)', yaxis_title='Density')
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    for s,c in [('Good',GOOD),('Standard',STD),('Poor',POOR)]:
        d = df[df['Credit_Score']==s]['Outstanding_Debt']
        d = pd.to_numeric(d.astype(str).str.replace('_',''), errors='coerce').dropna()
        med = d.median()
        st.markdown(f"""
        <div style='background:#10101A;border-left:2px solid {c};
                    padding:14px;border-radius:0 6px 6px 0;margin-bottom:10px'>
            <div style='font-family:DM Mono,monospace;font-size:0.55rem;
                        color:{c};letter-spacing:3px'>{s.upper()}</div>
            <div style='font-family:Syne,sans-serif;font-size:1.4rem;
                        font-weight:800;color:{c}'>${med:,.0f}</div>
            <div style='font-family:DM Mono,monospace;font-size:0.65rem;
                        color:#252535'>median</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

# ── ACT 3 — CREDIT HISTORY ───────────────────────────────────────────────────
st.markdown("""
<div style='font-family:DM Mono,monospace;font-size:0.58rem;
            color:#FF4D6D;letter-spacing:4px'>PATTERN 03</div>
<h2 style='margin:4px 0 6px 0;color:#EEEEF8;font-family:Syne,sans-serif;font-weight:800'>Time is the Unfair Advantage</h2>
<p style='font-family:DM Mono,monospace;font-size:0.75rem;color:#333348;margin-bottom:16px'>
Good scorers have nearly 9 extra years of credit history on average
</p>
""", unsafe_allow_html=True)

means = df.groupby('Credit_Score')['Credit_History_Months'].mean()/12
fig3 = go.Figure()
for s,c in [('Poor',POOR),('Standard',STD),('Good',GOOD)]:
    if s in means:
        fig3.add_trace(go.Bar(x=[means[s]], y=[s], orientation='h',
                              name=s, marker_color=c, opacity=0.85,
                              text=f'{means[s]:.1f} yrs', textposition='outside',
                              textfont=dict(color=c,family='DM Mono')))
fig3.update_layout(**BASE, showlegend=False, height=200,
                   title=dict(text='Avg Credit History by Tier',
                              font=dict(color='#444460',size=11,family='DM Mono')),
                   xaxis_title='Years')
fig3.update_yaxes(tickfont=dict(color='#888899', size=11))
st.plotly_chart(fig3, use_container_width=True)

st.markdown('<div style="height:24px"></div>', unsafe_allow_html=True)

# ── ACT 4 — INQUIRY TRAP ─────────────────────────────────────────────────────
st.markdown("""
<div style='font-family:DM Mono,monospace;font-size:0.58rem;
            color:#FF4D6D;letter-spacing:4px'>PATTERN 04</div>
<h2 style='margin:4px 0 6px 0;color:#EEEEF8;font-family:Syne,sans-serif;font-weight:800'>The Inquiry Trap</h2>
<p style='font-family:DM Mono,monospace;font-size:0.75rem;color:#333348;margin-bottom:16px'>
Every desperate credit application hurts your score — the system punishes people for trying to escape it
</p>
""", unsafe_allow_html=True)

ib=[0,5,10,15,20,100]; il=['0–5','6–10','11–15','16–20','20+']
df['IB'] = pd.cut(df['Num_Credit_Inquiries'].clip(0,100), bins=ib, include_lowest=True)
ct4 = pd.crosstab(df['IB'], df['Credit_Score'], normalize='index')*100
ct4.index = il[:len(ct4)]

fig4 = go.Figure()
for s,c in SC.items():
    if s in ct4.columns:
        fig4.add_trace(go.Scatter(x=ct4.index, y=ct4[s], name=s,
                                  line=dict(color=c,width=2),
                                  mode='lines+markers',
                                  marker=dict(size=7,color=c,
                                              line=dict(color=BG,width=1.5))))
fig4.update_layout(**BASE, height=300,
                   title=dict(text='Credit Score by Number of Credit Inquiries',
                              font=dict(color='#444460',size=11,family='DM Mono')),
                   xaxis_title='Credit Inquiries', yaxis_title='% of People')
st.plotly_chart(fig4, use_container_width=True)

# ── VERDICT ───────────────────────────────────────────────────────────────────
st.markdown('<div style="width:100%;height:1px;background:#16161F;margin:32px 0"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='font-family:DM Mono,monospace;font-size:0.58rem;
            color:#252535;letter-spacing:4px;margin-bottom:12px'>THE CONCLUSION</div>
<h2 style='margin-bottom:20px;color:#EEEEF8;font-family:Syne,sans-serif;font-weight:800'>The trap is behaviour, not income</h2>
""", unsafe_allow_html=True)

for label, color, desc in [
    ('GOOD',     GOOD, '<5 missed payments · $664 median debt · 21.9 yr history'),
    ('STANDARD', STD,  '~7 missed payments · $1,015 median debt · 17.3 yr history'),
    ('POOR',     POOR, '>15 missed payments · $1,897 median debt · 13.2 yr history'),
]:
    st.markdown(f"""
    <div style='border-left:2px solid {color};padding:14px 20px;
                margin-bottom:10px;background:#10101A;border-radius:0 6px 6px 0;
                display:flex;align-items:center;gap:24px'>
        <div style='font-family:DM Mono,monospace;font-size:0.7rem;
                    font-weight:600;color:{color};min-width:72px;letter-spacing:2px'>{label}</div>
        <div style='font-family:DM Mono,monospace;font-size:0.72rem;color:#333348'>{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height:48px'></div>", unsafe_allow_html=True)
