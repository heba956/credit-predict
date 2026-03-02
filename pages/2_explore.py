import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

GOOD='#00E5A0'; STD='#FFD166'; POOR='#FF4D6D'
BG='#0A0A0F'; PANEL='#10101A'; GRID='#16161F'; TEXT='#D8D8E8'
SC={'Good':GOOD,'Standard':STD,'Poor':POOR}

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
    df = pd.read_csv('data.csv')
    df.drop(columns=['Name','Unnamed: 0'], inplace=True, errors='ignore')
    df['Age'] = pd.to_numeric(df['Age'].astype(str).str.replace('_',''), errors='coerce')
    df = df[(df['Age']>10)&(df['Age']<110)]
    for col in ['Num_of_Delayed_Payment','Outstanding_Debt','Annual_Income',
                'Interest_Rate','Num_Credit_Inquiries','Monthly_Inhand_Salary',
                'Total_EMI_per_month','Credit_Utilization_Ratio','Monthly_Balance',
                'Amount_invested_monthly']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace('_',''), errors='coerce')
    df = df[df['Payment_Behaviour'] != '!@9#%8']
    df.dropna(subset=['Credit_Score'], inplace=True)
    def parse(s):
        try:
            y=int(str(s).split('Years')[0].strip())
            m=int(str(s).split('and')[1].split('Months')[0].strip())
            return y*12+m
        except: return np.nan
    df['Credit_History_Months'] = df['Credit_History_Age'].apply(parse)
    df['Debt_to_Income'] = df['Outstanding_Debt'] / (df['Annual_Income']/12).replace(0,np.nan)
    df['EMI_Burden']     = df['Total_EMI_per_month'] / df['Monthly_Inhand_Salary'].replace(0,np.nan)
    df['Stress_Index']   = (df['Debt_to_Income'].clip(0,5)/5 + df['Num_of_Delayed_Payment'].clip(0,30)/30 + df['Num_Credit_Inquiries'].clip(0,50)/50)/3
    return df

df = load()

st.markdown("""
<div style='padding:32px 0 4px 0'>
    <div style='font-family:DM Mono,monospace;font-size:0.58rem;
                color:#252535;letter-spacing:4px'>EXPLORE</div>
    <div style='font-family:Syne,sans-serif;font-size:2.4rem;font-weight:800;
                color:#EEEEF8;letter-spacing:-1px;margin:8px 0 12px 0'>
        Explore the Data
    </div>
    <p style='font-family:DM Mono,monospace;font-size:0.78rem;
              color:#333348;line-height:1.9'>
        Select any feature and chart type. See how the three tiers separate.
    </p>
</div>
<div style='width:100%;height:1px;background:#16161F;margin:16px 0 28px 0'></div>
""", unsafe_allow_html=True)

FEATURES = {
    'Outstanding Debt':         ('Outstanding_Debt',        0,   5000),
    'Annual Income':            ('Annual_Income',            0,   200000),
    'Interest Rate (%)':        ('Interest_Rate',            0,   100),
    'Missed Payments':          ('Num_of_Delayed_Payment',   0,   50),
    'Credit Inquiries':         ('Num_Credit_Inquiries',     0,   60),
    'Credit Utilization (%)':   ('Credit_Utilization_Ratio', 0,   100),
    'Monthly Balance':          ('Monthly_Balance',          -500,5000),
    'Credit History (months)':  ('Credit_History_Months',    0,   500),
    'Age':                      ('Age',                      18,  80),
    'EMI Monthly ($)':          ('Total_EMI_per_month',      0,   2000),
    'Debt-to-Income ★':         ('Debt_to_Income',           0,   3),
    'EMI Burden ★':             ('EMI_Burden',               0,   0.5),
    'Stress Index ★':           ('Stress_Index',             0,   0.8),
}

sel_col, chart_col = st.columns([1,3])

with sel_col:
    st.markdown("<div style='font-family:DM Mono,monospace;font-size:0.58rem;color:#252535;letter-spacing:3px;margin-bottom:10px'>FEATURE</div>", unsafe_allow_html=True)
    sel = st.radio("", list(FEATURES.keys()), label_visibility='collapsed')
    col_name, xmin, xmax = FEATURES[sel]

    st.markdown("<br><div style='font-family:DM Mono,monospace;font-size:0.58rem;color:#252535;letter-spacing:3px;margin-bottom:10px'>CHART</div>", unsafe_allow_html=True)
    ctype = st.radio("chart", ['Histogram','Box','Violin'], label_visibility='collapsed')

    st.markdown("<br><div style='font-family:DM Mono,monospace;font-size:0.58rem;color:#252535;letter-spacing:3px;margin-bottom:10px'>TIERS</div>", unsafe_allow_html=True)
    sg = st.checkbox('Good',     value=True)
    ss = st.checkbox('Standard', value=True)
    sp = st.checkbox('Poor',     value=True)

with chart_col:
    active = {s:c for s,c in SC.items()
              if (s=='Good' and sg) or (s=='Standard' and ss) or (s=='Poor' and sp)}
    fig = go.Figure()

    if ctype == 'Histogram':
        for s,c in active.items():
            d = df[df['Credit_Score']==s][col_name].dropna()
            d = d[(d>=xmin)&(d<=xmax)]
            fig.add_trace(go.Histogram(x=d, name=s, marker_color=c,
                                       opacity=0.55, histnorm='probability density', nbinsx=50))
        fig.update_layout(**BASE, barmode='overlay')

    elif ctype == 'Box':
        for s,c in active.items():
            d = df[df['Credit_Score']==s][col_name].dropna().clip(xmin,xmax)
            fig.add_trace(go.Box(y=d, name=s, marker_color=c,
                                  line_color=c, fillcolor=c, opacity=0.6, boxmean=True))

    else:
        for s,c in active.items():
            d = df[df['Credit_Score']==s][col_name].dropna().clip(xmin,xmax)
            fig.add_trace(go.Violin(y=d, name=s, line_color=c,
                                     fillcolor=c, opacity=0.45,
                                     meanline_visible=True, box_visible=True))

    fig.update_layout(**BASE, height=400,
                      title=dict(text=f'{sel} by Credit Tier',
                                 font=dict(color='#444460',size=11,family='DM Mono')))
    st.plotly_chart(fig, use_container_width=True)

    rows = []
    for s in ['Good','Standard','Poor']:
        d = df[df['Credit_Score']==s][col_name].dropna()
        d = d[(d>=xmin)&(d<=xmax)]
        rows.append({'Tier':s,'Median':f'{d.median():.2f}',
                     'Mean':f'{d.mean():.2f}','Std':f'{d.std():.2f}'})
    st.dataframe(pd.DataFrame(rows).set_index('Tier'), use_container_width=True)

# ── Bubble chart ──────────────────────────────────────────────────────────────
st.markdown('<div style="width:100%;height:1px;background:#16161F;margin:32px 0"></div>', unsafe_allow_html=True)
st.markdown("""
<div style='font-family:DM Mono,monospace;font-size:0.58rem;
            color:#252535;letter-spacing:4px;margin-bottom:4px'>THE CREDIT UNIVERSE</div>
<h2 style='margin-bottom:6px'>Income vs Debt</h2>
<p style='font-family:DM Mono,monospace;font-size:0.72rem;color:#333348;margin-bottom:16px'>
Bubble size = missed payments
</p>
""", unsafe_allow_html=True)

sample = df.dropna(subset=['Annual_Income','Outstanding_Debt','Num_of_Delayed_Payment'])
sample = pd.concat([
    sample[sample['Credit_Score']=='Good'].sample(min(300,len(sample[sample['Credit_Score']=='Good'])), random_state=42),
    sample[sample['Credit_Score']=='Standard'].sample(min(400,len(sample[sample['Credit_Score']=='Standard'])), random_state=42),
    sample[sample['Credit_Score']=='Poor'].sample(min(250,len(sample[sample['Credit_Score']=='Poor'])), random_state=42),
])

figb = go.Figure()
for s,c in [('Poor',POOR),('Standard',STD),('Good',GOOD)]:
    sub = sample[sample['Credit_Score']==s]
    sizes = (sub['Num_of_Delayed_Payment'].clip(0,35)/35)*50+6
    figb.add_trace(go.Scatter(
        x=sub['Annual_Income'], y=sub['Outstanding_Debt'],
        mode='markers', name=s,
        marker=dict(size=sizes, color=c, opacity=0.5,
                    line=dict(color=c,width=0.5)),
        hovertemplate=f'<b>{s}</b><br>Income: $%{{x:,.0f}}<br>Debt: $%{{y:,.0f}}<extra></extra>'
    ))

# Build xaxis/yaxis dicts by extending BASE values — no duplicate kwargs
figb.update_layout(**BASE, height=400,
                   title=dict(text='Income vs Outstanding Debt — sampled',
                              font=dict(color='#444460',size=11,family='DM Mono')))
figb.update_xaxes(tickformat='$,.0f', title_text='Annual Income ($)')
figb.update_yaxes(tickformat='$,.0f', title_text='Outstanding Debt ($)')

st.plotly_chart(figb, use_container_width=True)
