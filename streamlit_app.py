"""
DA-AI Intelligence Dashboard — Streamlit Version
=========================================================
Paste this into Streamlit Cloud (streamlit.io) or run locally:
    pip install streamlit plotly pandas
    streamlit run app.py

GitHub repo structure:
    /
    ├── app.py                          ← this file
    ├── requirements.txt
    └── data/
        ├── 01_Company_Financial_Metrics.csv
        ├── 02_User_Growth_Metrics.csv
        ├── 05_Unit_Economics_Financial_Ratios.csv
        └── 06_Market_Projections_2026_2030.csv
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DA-AI Intelligence Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── THEME COLOURS ──────────────────────────────────────────────────────────────
COLORS = {
    "OpenAI":         "#00D4AA",
    "Anthropic":      "#FF6B6B",
    "xAI (Grok)":     "#FFD93D",
    "Google (Gemini)":"#4ECDC4",
    "Meta (Llama)":   "#A78BFA",
}
BG      = "#080d18"
BG2     = "#0a111f"
BORDER  = "#1a2e50"
TEXT    = "#e2e8f0"
MUTED   = "#3d5a7a"
COMPANIES = list(COLORS.keys())

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&display=swap');
html, body, [class*="css"]  {
    font-family: 'IBM Plex Mono', monospace !important;
    background-color: #080d18 !important;
    color: #e2e8f0 !important;
}
.stApp { background-color: #080d18; }
section[data-testid="stSidebar"] { background: #0a111f; border-right: 1px solid #1a2e50; }
.metric-card {
    background: #0a111f;
    border: 1px solid #1a2e50;
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 4px;
}
.metric-val  { font-size: 26px; font-weight: 800; line-height: 1; margin: 4px 0; }
.metric-sub  { font-size: 11px; color: #2a3e5a; margin-top: 4px; }
.metric-lbl  { font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: #2a3e5a; }
.section-title {
    font-size: 13px; font-weight: 700; letter-spacing: 1px;
    color: #94a3b8; margin-bottom: 10px; padding-left: 10px;
    border-left: 3px solid #00D4AA;
}
div[data-testid="stMetric"] {
    background: #0a111f;
    border: 1px solid #1a2e50;
    border-radius: 10px;
    padding: 12px 16px;
}
div[data-testid="stMetric"] label { color: #3d5a7a !important; font-size: 10px !important; }
div[data-testid="stMetric"] div[data-testid="stMetricValue"] { color: #00D4AA !important; font-size: 22px !important; }
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] { font-size: 11px !important; }
.stTabs [data-baseweb="tab-list"] { background: #0a111f; border-bottom: 1px solid #1a2e50; gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: transparent; color: #475569;
    border: 1px solid transparent; border-radius: 8px 8px 0 0;
    font-family: 'IBM Plex Mono', monospace; font-size: 12px; padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: #0f1e3d !important; color: #00D4AA !important;
    border: 1px solid #1a2e50 !important;
}
h1 { font-size: 28px !important; font-weight: 800 !important; letter-spacing: 3px !important; color: #00D4AA !important; }
h2, h3 { color: #94a3b8 !important; }
hr { border-color: #1a2e50 !important; }
</style>
""", unsafe_allow_html=True)

# ── PLOTLY LAYOUT DEFAULTS ─────────────────────────────────────────────────────
LAYOUT = dict(
    paper_bgcolor="#0a111f", plot_bgcolor="#0a111f",
    font=dict(family="IBM Plex Mono", color="#94a3b8", size=11),
    margin=dict(l=40, r=20, t=40, b=40),
    legend=dict(bgcolor="#0a111f", bordercolor="#1a2e50", borderwidth=1),
    xaxis=dict(gridcolor="#111d30", zerolinecolor="#1a2e50", tickfont=dict(color="#3d5a7a")),
    yaxis=dict(gridcolor="#111d30", zerolinecolor="#1a2e50", tickfont=dict(color="#3d5a7a")),
)

def apply_layout(fig, title="", h=320):
    fig.update_layout(**LAYOUT, height=h, title=dict(text=title, font=dict(size=12, color="#64748b")))
    return fig

# ── DATA ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    fin = pd.DataFrame([
        {"company":"OpenAI","year":2022,"arr":0.028,"rev":0.028,"val":29,"margin":10,"burn":0.5,"loss":-0.5},
        {"company":"OpenAI","year":2023,"arr":2.0,"rev":1.6,"val":57,"margin":15,"burn":2.0,"loss":-1.5},
        {"company":"OpenAI","year":2024,"arr":3.7,"rev":3.7,"val":157,"margin":20,"burn":5.0,"loss":-5.0},
        {"company":"OpenAI","year":2025,"arr":20.0,"rev":13.0,"val":300,"margin":50,"burn":9.0,"loss":-8.0},
        {"company":"Anthropic","year":2022,"arr":0.01,"rev":0.01,"val":4.1,"margin":30,"burn":0.3,"loss":-0.3},
        {"company":"Anthropic","year":2023,"arr":0.1,"rev":0.1,"val":18.4,"margin":40,"burn":1.2,"loss":-1.1},
        {"company":"Anthropic","year":2024,"arr":0.85,"rev":0.85,"val":40,"margin":55,"burn":5.3,"loss":-5.3},
        {"company":"Anthropic","year":2025,"arr":9.0,"rev":5.0,"val":183,"margin":77,"burn":3.0,"loss":-3.0},
        {"company":"xAI (Grok)","year":2024,"arr":0.1,"rev":0.1,"val":50,"margin":15,"burn":5.0,"loss":-4.9},
        {"company":"xAI (Grok)","year":2025,"arr":3.2,"rev":1.5,"val":230,"margin":25,"burn":13.0,"loss":-11.5},
        {"company":"Google (Gemini)","year":2023,"arr":2.0,"rev":307.4,"val":1100,"margin":45,"burn":20,"loss":60},
        {"company":"Google (Gemini)","year":2024,"arr":8.0,"rev":350,"val":1800,"margin":50,"burn":50,"loss":73.8},
        {"company":"Google (Gemini)","year":2025,"arr":25.0,"rev":380,"val":2000,"margin":55,"burn":80,"loss":111},
        {"company":"Meta (Llama)","year":2023,"arr":1.0,"rev":116.6,"val":360,"margin":80,"burn":15,"loss":23.2},
        {"company":"Meta (Llama)","year":2024,"arr":5.0,"rev":164.5,"val":1200,"margin":81,"burn":40,"loss":62.4},
        {"company":"Meta (Llama)","year":2025,"arr":15.0,"rev":189.5,"val":1400,"margin":82,"burn":71,"loss":70},
    ])

    usr = pd.DataFrame([
        {"company":"OpenAI","year":2022,"mau":1,"paid":0.1,"enterprise":0.1,"share":15},
        {"company":"OpenAI","year":2023,"mau":100,"paid":5,"enterprise":20,"share":68},
        {"company":"OpenAI","year":2024,"mau":200,"paid":15,"enterprise":260,"share":65},
        {"company":"OpenAI","year":2025,"mau":600,"paid":25,"enterprise":600,"share":60.6},
        {"company":"Anthropic","year":2022,"mau":0.2,"paid":0.005,"enterprise":0.2,"share":0.5},
        {"company":"Anthropic","year":2023,"mau":0.5,"paid":0.01,"enterprise":0.5,"share":1},
        {"company":"Anthropic","year":2024,"mau":10,"paid":0.5,"enterprise":50,"share":5},
        {"company":"Anthropic","year":2025,"mau":30,"paid":2,"enterprise":300,"share":12},
        {"company":"xAI (Grok)","year":2024,"mau":5,"paid":0.5,"enterprise":5,"share":1},
        {"company":"xAI (Grok)","year":2025,"mau":64,"paid":5,"enterprise":20,"share":3.5},
        {"company":"Google (Gemini)","year":2024,"mau":50,"paid":2,"enterprise":100,"share":10},
        {"company":"Google (Gemini)","year":2025,"mau":450,"paid":10,"enterprise":500,"share":13.4},
        {"company":"Meta (Llama)","year":2023,"mau":10,"paid":0,"enterprise":0,"share":5},
        {"company":"Meta (Llama)","year":2024,"mau":200,"paid":0,"enterprise":200,"share":8},
        {"company":"Meta (Llama)","year":2025,"mau":600,"paid":0,"enterprise":1000,"share":10},
    ])

    ue = pd.DataFrame([
        {"company":"OpenAI","year":2023,"arpu":32,"ltv":960,"cac":50,"ltvcac":19.2,"burn_mult":1.3},
        {"company":"OpenAI","year":2024,"arpu":24.7,"ltv":888,"cac":40,"ltvcac":22.2,"burn_mult":1.4},
        {"company":"OpenAI","year":2025,"arpu":21.7,"ltv":780,"cac":35,"ltvcac":22.3,"burn_mult":0.7},
        {"company":"Anthropic","year":2023,"arpu":200,"ltv":7200,"cac":500,"ltvcac":14.4,"burn_mult":12.0},
        {"company":"Anthropic","year":2024,"arpu":85,"ltv":3060,"cac":250,"ltvcac":12.2,"burn_mult":6.2},
        {"company":"Anthropic","year":2025,"arpu":166.7,"ltv":6000,"cac":200,"ltvcac":30.0,"burn_mult":0.6},
        {"company":"xAI (Grok)","year":2024,"arpu":20,"ltv":720,"cac":100,"ltvcac":7.2,"burn_mult":50.0},
        {"company":"xAI (Grok)","year":2025,"arpu":23.4,"ltv":842,"cac":80,"ltvcac":10.5,"burn_mult":4.1},
    ])

    proj = pd.DataFrame([
        {"company":"OpenAI","year":2026,"base":29.4,"bull":40,"bear":20},
        {"company":"OpenAI","year":2028,"base":75,"bull":100,"bear":50},
        {"company":"OpenAI","year":2030,"base":125,"bull":200,"bear":80},
        {"company":"Anthropic","year":2026,"base":20,"bull":30,"bear":12},
        {"company":"Anthropic","year":2028,"base":70,"bull":90,"bear":40},
        {"company":"Anthropic","year":2030,"base":100,"bull":150,"bear":60},
        {"company":"Google (Gemini)","year":2026,"base":50,"bull":75,"bear":35},
        {"company":"Google (Gemini)","year":2028,"base":120,"bull":180,"bear":80},
        {"company":"Google (Gemini)","year":2030,"base":200,"bull":300,"bear":130},
        {"company":"xAI (Grok)","year":2026,"base":5,"bull":10,"bear":3},
        {"company":"xAI (Grok)","year":2028,"base":14,"bull":25,"bear":8},
        {"company":"xAI (Grok)","year":2030,"base":25,"bull":50,"bear":15},
        {"company":"Meta (Llama)","year":2026,"base":25,"bull":38,"bear":15},
        {"company":"Meta (Llama)","year":2028,"base":60,"bull":90,"bear":35},
        {"company":"Meta (Llama)","year":2030,"base":100,"bull":150,"bear":60},
    ])

    tools = pd.DataFrame([
        {"cat":"Text Generation","tool":"ChatGPT","co":"OpenAI","perf":9.5,"cost":7.5,"ease":9.8,"score":8.96},
        {"cat":"Text Generation","tool":"Claude 3.5","co":"Anthropic","perf":9.6,"cost":7.0,"ease":9.5,"score":8.80},
        {"cat":"Text Generation","tool":"Gemini 2.5","co":"Google","perf":9.3,"cost":8.5,"ease":9.7,"score":9.14},
        {"cat":"Text Generation","tool":"Grok 4","co":"xAI","perf":8.7,"cost":6.5,"ease":9.0,"score":8.10},
        {"cat":"Text Generation","tool":"Meta AI","co":"Meta","perf":8.9,"cost":10.0,"ease":8.5,"score":9.15},
        {"cat":"Coding","tool":"Cursor","co":"Anysphere","perf":9.4,"cost":6.5,"ease":9.0,"score":8.45},
        {"cat":"Coding","tool":"Claude Code","co":"Anthropic","perf":9.5,"cost":6.0,"ease":9.2,"score":8.39},
        {"cat":"Coding","tool":"GitHub Copilot","co":"Microsoft","perf":8.8,"cost":7.0,"ease":8.5,"score":8.20},
        {"cat":"Image Gen","tool":"Midjourney","co":"Midjourney","perf":9.7,"cost":6.0,"ease":8.0,"score":8.25},
        {"cat":"Image Gen","tool":"DALL-E 3","co":"OpenAI","perf":9.2,"cost":7.0,"ease":9.5,"score":8.60},
        {"cat":"Research","tool":"Perplexity","co":"Perplexity","perf":9.4,"cost":7.0,"ease":9.5,"score":8.70},
        {"cat":"Research","tool":"Gemini Research","co":"Google","perf":8.9,"cost":8.0,"ease":9.2,"score":8.69},
        {"cat":"Data Analysis","tool":"ChatGPT Analyst","co":"OpenAI","perf":9.0,"cost":7.5,"ease":9.0,"score":8.55},
        {"cat":"Data Analysis","tool":"Claude Artifacts","co":"Anthropic","perf":9.2,"cost":7.0,"ease":9.3,"score":8.56},
        {"cat":"Data Analysis","tool":"AI Studio","co":"Google","perf":8.8,"cost":8.5,"ease":9.0,"score":8.75},
    ])

    return fin, usr, ue, proj, tools

fin, usr, ue, proj, tools = load_data()

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:linear-gradient(135deg,#050a14,#0f1e3d,#050a14);
            border-bottom:1px solid #1a2e50;padding:28px 8px 20px;margin-bottom:0">
  <h1 style="background:linear-gradient(90deg,#00D4AA,#4ECDC4,#A78BFA,#FFD93D);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             font-size:26px;font-weight:800;letter-spacing:3px;margin:0">
    DA-AI INTELLIGENCE DASHBOARD
  </h1>
  <p style="color:#2a3e5a;font-size:10px;letter-spacing:3px;text-transform:uppercase;margin-top:6px">
    OpenAI · Anthropic · Google Gemini · Meta Llama · xAI Grok — Revenue · Growth · Market Dominance · 2022–2030
  </p>
</div>
""", unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("AI Market 2025","$70B","↑ from $10B in 2023")
with c2: st.metric("Market 2030 Proj.","$500B","7× growth expected")
with c3: st.metric("Fastest Growing","Anthropic","488% YoY revenue")
with c4: st.metric("Best LTV:CAC","30 : 1","Anthropic 2025")

st.markdown("<hr style='margin:8px 0 0'>",unsafe_allow_html=True)

# ── TABS ────────────────────────────────────────────────────────────────────────
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "🏆 Executive Overview",
    "📈 Revenue Analysis",
    "💰 Profitability",
    "🤖 AI Models",
    "🚀 Future Growth",
])

# ── TAB 1: OVERVIEW ────────────────────────────────────────────────────────────
with tab1:
    st.markdown("<div class='section-title'>KEY PERFORMANCE INDICATORS — 2025</div>",unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    with m1: st.metric("Best Gross Margin","77%","Anthropic")
    with m2: st.metric("Capital Efficiency","0.6×","Anthropic burn mult.")
    with m3: st.metric("Largest User Base","800M WAU","OpenAI ChatGPT")
    with m4: st.metric("Total CapEx 23-25","$538B","Industry infra")

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='section-title'>ARR GROWTH TRAJECTORY 2022–2025 ($B)</div>",unsafe_allow_html=True)
        fig = go.Figure()
        for c in COMPANIES:
            d = fin[fin.company==c].sort_values("year")
            fig.add_trace(go.Scatter(x=d.year, y=d.arr, name=c.split(" ")[0],
                mode="lines+markers", line=dict(color=COLORS[c],width=2.5),
                marker=dict(size=6,color=COLORS[c]),
               fig.add_trace(
    go.Scatter(
        x=d.year,
        y=d.arr,
        name=c.split(" ")[0],
        mode="lines+markers",
        line=dict(color=COLORS[c], width=2.5),
        marker=dict(size=6, color=COLORS[c]),
    )
)
                                    ) )  
        apply_layout(fig, h=340)
        fig.update_layout(yaxis_title="ARR ($B)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>2025 MARKET SHARE %</div>",unsafe_allow_html=True)
        u25 = usr[usr.year==2025]
        fig2 = go.Figure(go.Pie(
            labels=[c.split(" ")[0] for c in u25.company],
            values=u25.share,
            marker_colors=[COLORS[c] for c in u25.company],
            hole=0.45, textinfo="label+percent",
            textfont=dict(size=10,family="IBM Plex Mono"),
        ))
        apply_layout(fig2, h=340)
        st.plotly_chart(fig2, use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        st.markdown("<div class='section-title'>2025 ARR RANKING ($B)</div>",unsafe_allow_html=True)
        f25 = fin[fin.year==2025].sort_values("arr",ascending=True)
        fig3 = go.Figure(go.Bar(
            x=f25.arr, y=[c.split(" ")[0] for c in f25.company],
            orientation="h",
            marker_color=[COLORS[c] for c in f25.company],
            marker_line_width=0, text=[f"${v}B" for v in f25.arr], textposition="outside",
        ))
        apply_layout(fig3, h=280)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>MONTHLY ACTIVE USERS 2025 (M)</div>",unsafe_allow_html=True)
        u25s = usr[usr.year==2025].sort_values("mau",ascending=False)
        fig4 = go.Figure(go.Bar(
            x=[c.split(" ")[0] for c in u25s.company], y=u25s.mau,
            marker_color=[COLORS[c] for c in u25s.company],
            marker_line_width=0, text=u25s.mau, textposition="outside",
        ))
        apply_layout(fig4, h=280)
        st.plotly_chart(fig4, use_container_width=True)

# ── TAB 2: REVENUE ─────────────────────────────────────────────────────────────
with tab2:
    col1,col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='section-title'>ARR TREND 2022–2025 ($B)</div>",unsafe_allow_html=True)
        fig = go.Figure()
        for c in COMPANIES:
            d = fin[fin.company==c].sort_values("year")
            fig.add_trace(go.Scatter(x=d.year,y=d.arr,name=c.split(" ")[0],
                mode="lines+markers",line=dict(color=COLORS[c],width=2.5),marker=dict(size=7,color=COLORS[c])))
        apply_layout(fig, h=300)
        fig.update_layout(yaxis_title="ARR ($B)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>REVENUE SEGMENT MIX 2025</div>",unsafe_allow_html=True)
        seg = pd.DataFrame([
            {"co":"OpenAI","consumer":60,"enterprise":35,"api":5},
            {"co":"Anthropic","consumer":20,"enterprise":80,"api":0},
            {"co":"Google","consumer":30,"enterprise":40,"api":30},
            {"co":"Meta","consumer":0,"enterprise":30,"api":70},
            {"co":"xAI","consumer":70,"enterprise":20,"api":10},
        ])
        fig2 = go.Figure()
        for col,color,name in [("consumer","#00D4AA","Consumer"),("enterprise","#A78BFA","Enterprise"),("api","#FFD93D","API")]:
            fig2.add_trace(go.Bar(name=name,x=seg.co,y=seg[col],marker_color=color,marker_line_width=0))
        fig2.update_layout(barmode="stack")
        apply_layout(fig2, h=300)
        st.plotly_chart(fig2, use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        st.markdown("<div class='section-title'>YoY REVENUE GROWTH % BY PERIOD</div>",unsafe_allow_html=True)
        growth_df = pd.DataFrame([
            {"period":"2022→23","OpenAI":5614,"Anthropic":900,"xAI (Grok)":None,"Google (Gemini)":None,"Meta (Llama)":None},
            {"period":"2023→24","OpenAI":131,"Anthropic":750,"xAI (Grok)":None,"Google (Gemini)":14,"Meta (Llama)":41},
            {"period":"2024→25","OpenAI":251,"Anthropic":488,"xAI (Grok)":1400,"Google (Gemini)":9,"Meta (Llama)":15},
        ])
        fig3 = go.Figure()
        for c in COMPANIES:
            if c in growth_df.columns:
                fig3.add_trace(go.Bar(name=c.split(" ")[0],x=growth_df.period,y=growth_df[c],
                    marker_color=COLORS[c],marker_line_width=0))
        fig3.update_layout(barmode="group")
        apply_layout(fig3, h=280)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>2025 VALUATION vs ARR ($B)</div>",unsafe_allow_html=True)
        f25 = fin[fin.year==2025]
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Valuation $B",x=[c.split(" ")[0] for c in f25.company],y=f25.val,
            marker_color="#4ECDC4",marker_line_width=0))
        fig4.add_trace(go.Bar(name="ARR $B",x=[c.split(" ")[0] for c in f25.company],y=f25.arr,
            marker_color="#00D4AA",marker_line_width=0))
        fig4.update_layout(barmode="group")
        apply_layout(fig4, h=280)
        st.plotly_chart(fig4, use_container_width=True)

# ── TAB 3: PROFITABILITY ───────────────────────────────────────────────────────
with tab3:
    st.markdown("<div class='section-title'>GROSS MARGIN % — 2025</div>",unsafe_allow_html=True)
    m1,m2,m3,m4 = st.columns(4)
    f25 = fin[fin.year==2025]
    for i,(mc,col) in enumerate(zip(COMPANIES[:4],[m1,m2,m3,m4])):
        r = f25[f25.company==mc].iloc[0]
        with col:
            st.metric(mc.split(" ")[0]+f" Margin",f"{r.margin}%",f"Burn: ${r.burn}B")

    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>GROSS MARGIN TREND 2023–2025 (%)</div>",unsafe_allow_html=True)
        fig = go.Figure()
        for c in COMPANIES:
            d = fin[(fin.company==c)&(fin.year>=2023)].sort_values("year")
            if not d.empty:
                fig.add_trace(go.Scatter(x=d.year,y=d.margin,name=c.split(" ")[0],
                    mode="lines+markers",line=dict(color=COLORS[c],width=2.5),marker=dict(size=7)))
        apply_layout(fig, h=280)
        fig.update_layout(yaxis_title="Gross Margin (%)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>LTV:CAC RATIO 2025  (Target: 3:1)</div>",unsafe_allow_html=True)
        ue25 = ue[ue.year==2025]
        bar_colors = ["#00D4AA" if v>=3 else "#FF6B6B" for v in ue25.ltvcac]
        fig2 = go.Figure(go.Bar(
            x=[c.split(" ")[0] for c in ue25.company],
            y=ue25.ltvcac,
            marker_color=bar_colors,marker_line_width=0,
            text=[f"{v}" for v in ue25.ltvcac], textposition="outside",
        ))
        fig2.add_hline(y=3,line_dash="dash",line_color="#FFD93D",annotation_text="3:1 Target")
        apply_layout(fig2, h=280)
        st.plotly_chart(fig2, use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        st.markdown("<div class='section-title'>ARPU vs BURN MULTIPLE — EFFICIENCY QUADRANT 2025</div>",unsafe_allow_html=True)
        ue25 = ue[ue.year==2025]
        fig3 = go.Figure()
        for _,row in ue25.iterrows():
            c = row.company
            fig3.add_trace(go.Scatter(
                x=[row.arpu],y=[row.burn_mult],name=c.split(" ")[0],
                mode="markers+text",text=[c.split(" ")[0]],textposition="top center",
                marker=dict(size=18,color=COLORS.get(c,"#4ECDC4"),opacity=0.85),
                textfont=dict(size=10,color=COLORS.get(c,"#4ECDC4"))
            ))
        fig3.add_vline(x=100,line_dash="dash",line_color="#1a2e50")
        fig3.add_hline(y=2,line_dash="dash",line_color="#1a2e50")
        apply_layout(fig3, h=280)
        fig3.update_layout(xaxis_title="ARPU ($) — Higher is better →",yaxis_title="Burn Multiple — Lower is better →",showlegend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>COLLABORATION SYNERGY VALUE ($B)</div>",unsafe_allow_html=True)
        collab = pd.DataFrame([
            {"scenario":"OpenAI+Microsoft","synergy":50,"rev2026":150,"prob":70},
            {"scenario":"Anthropic+Google+AWS","synergy":25,"rev2026":80,"prob":50},
            {"scenario":"Meta Llama Open","synergy":20,"rev2026":35,"prob":90},
            {"scenario":"xAI+Tesla","synergy":15,"rev2026":25,"prob":60},
            {"scenario":"All 5 Coalition","synergy":150,"rev2026":400,"prob":10},
        ])
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Synergy $B",y=collab.scenario,x=collab.synergy,orientation="h",marker_color="#A78BFA",marker_line_width=0))
        fig4.add_trace(go.Bar(name="Proj. Rev 2026 $B",y=collab.scenario,x=collab.rev2026,orientation="h",marker_color="#00D4AA",marker_line_width=0))
        fig4.update_layout(barmode="group")
        apply_layout(fig4, h=280)
        st.plotly_chart(fig4, use_container_width=True)

# ── TAB 4: AI MODELS ───────────────────────────────────────────────────────────
with tab4:
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("<div class='section-title'>AI MODEL CAPABILITY RADAR</div>",unsafe_allow_html=True)
        categories = ["Performance","Cost Effect.","Ease of Use","Data Analysis","Research","Coding"]
        radar_vals = {
            "OpenAI":   [9.5,7.5,9.8,9.0,8.7,8.5],
            "Anthropic":[9.6,7.0,9.5,9.2,8.55,9.5],
            "Google":   [9.3,8.5,9.7,8.8,8.69,7.5],
            "Meta":     [8.9,10.0,8.5,7.5,7.0,7.0],
            "xAI":      [8.7,6.5,9.0,7.0,7.2,7.0],
        }
        RCOLS = {"OpenAI":"#00D4AA","Anthropic":"#FF6B6B","Google":"#4ECDC4","Meta":"#A78BFA","xAI":"#FFD93D"}
        fig = go.Figure()
        for name,vals in radar_vals.items():
            fig.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=categories+[categories[0]],
                fill="toself",name=name,line=dict(color=RCOLS[name],width=2),fillcolor=RCOLS[name].replace("#","rgba(")+"18)"))
        apply_layout(fig, h=360)
        fig.update_layout(polar=dict(
            bgcolor="#0a111f",
            radialaxis=dict(visible=True,range=[0,10],gridcolor="#1a2e50",tickfont=dict(color="#2a3e5a",size=9)),
            angularaxis=dict(gridcolor="#1a2e50",tickfont=dict(color="#64748b",size=11))
        ))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>TEXT GENERATION — SCORES</div>",unsafe_allow_html=True)
        tg = tools[tools.cat=="Text Generation"]
        fig2 = go.Figure()
        for col,color,name in [("perf","#00D4AA","Performance"),("cost","#FFD93D","Cost Effect."),("ease","#4ECDC4","Ease of Use"),("score","#A78BFA","Overall")]:
            fig2.add_trace(go.Bar(name=name,x=tg.tool,y=tg[col],marker_color=color,marker_line_width=0))
        fig2.update_layout(barmode="group")
        apply_layout(fig2, h=360)
        fig2.update_layout(yaxis_range=[6,10])
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='section-title'>ALL AI TOOLS — OVERALL SCORE (ALL CATEGORIES)</div>",unsafe_allow_html=True)
    CO_MAP = {"OpenAI":"#00D4AA","Anthropic":"#FF6B6B","Google":"#4ECDC4","Meta":"#A78BFA","xAI":"#FFD93D","Microsoft":"#4ECDC4","Anysphere":"#A78BFA","Midjourney":"#FFD93D","Perplexity":"#FF6B6B"}
    all_sorted = tools.sort_values("score",ascending=False)
    fig3 = go.Figure(go.Bar(
        x=all_sorted.tool, y=all_sorted.score,
        marker_color=[CO_MAP.get(r,"#475569") for r in all_sorted.co],
        marker_line_width=0, text=[f"{v:.2f}" for v in all_sorted.score], textposition="outside",
    ))
    apply_layout(fig3, h=300)
    fig3.update_layout(yaxis_range=[7.5,10])
    st.plotly_chart(fig3, use_container_width=True)

# ── TAB 5: FUTURE GROWTH ───────────────────────────────────────────────────────
with tab5:
    m1,m2,m3 = st.columns(3)
    with m1: st.metric("OpenAI 2030 Base","$125B","Bull: $200B | Profit: 2029")
    with m2: st.metric("Anthropic 2030 Base","$100B","Bull: $150B | Profit: 2027")
    with m3: st.metric("Google 2030 Base","$200B","Bull: $300B | Already profitable")

    col1,col2 = st.columns([2,1])
    with col1:
        st.markdown("<div class='section-title'>REVENUE PROJECTION 2025→2030 BASE CASE ($B)</div>",unsafe_allow_html=True)
        years_hist = [2022,2023,2024,2025]
        years_proj = [2026,2028,2030]
        fig = go.Figure()
        for c in COMPANIES:
            hist = fin[fin.company==c].sort_values("year")
            pr = proj[proj.company==c].sort_values("year")
            all_y = list(hist.year) + list(pr.year)
            all_v = list(hist.arr) + list(pr.base)
            fig.add_trace(go.Scatter(x=all_y[:len(hist)],y=list(hist.arr),name=c.split(" ")[0],
                mode="lines+markers",line=dict(color=COLORS[c],width=2.5),marker=dict(size=6,color=COLORS[c])))
            if not pr.empty:
                xc = [hist.iloc[-1].year]+list(pr.year)
                yc = [hist.iloc[-1].arr]+list(pr.base)
                fig.add_trace(go.Scatter(x=xc,y=yc,name=c.split(" ")[0]+" proj.",
                    mode="lines+markers",line=dict(color=COLORS[c],width=2,dash="dot"),
                    marker=dict(size=5,color=COLORS[c]),showlegend=False))
        apply_layout(fig, h=320)
        fig.update_layout(yaxis_title="Revenue ($B)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("<div class='section-title'>TOTAL AI MARKET ($B)</div>",unsafe_allow_html=True)
        mkt = pd.DataFrame({"year":[2023,2024,2025,2026,2028,2030],"market":[10,28,70,120,250,500]})
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=mkt.year,y=mkt.market,fill="tozeroy",
            line=dict(color="#4ECDC4",width=3),
            fillcolor="rgba(78,205,196,0.15)",name="Market $B"))
        apply_layout(fig2, h=320)
        st.plotly_chart(fig2, use_container_width=True)

    col3,col4 = st.columns(2)
    with col3:
        st.markdown("<div class='section-title'>2030 REVENUE: BULL / BASE / BEAR ($B)</div>",unsafe_allow_html=True)
        p30 = proj[proj.year==2030]
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name="🟢 Bull",x=[c.split(" ")[0] for c in p30.company],y=p30.bull,marker_color="#00D4AA",marker_line_width=0))
        fig3.add_trace(go.Bar(name="🔵 Base",x=[c.split(" ")[0] for c in p30.company],y=p30.base,marker_color="#4ECDC4",marker_line_width=0))
        fig3.add_trace(go.Bar(name="🔴 Bear",x=[c.split(" ")[0] for c in p30.company],y=p30.bear,marker_color="#FF6B6B",marker_line_width=0))
        fig3.update_layout(barmode="group")
        apply_layout(fig3, h=280)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown("<div class='section-title'>PARTNERSHIP PROBABILITY vs MARKET SHARE</div>",unsafe_allow_html=True)
        collab = pd.DataFrame([
            {"scenario":"OpenAI+MSFT","prob":70,"share":55},
            {"scenario":"Anthropic+GCP","prob":50,"share":30},
            {"scenario":"Meta Open","prob":90,"share":15},
            {"scenario":"xAI+Tesla","prob":60,"share":10},
            {"scenario":"All 5","prob":10,"share":95},
        ])
        fig4 = go.Figure()
        fig4.add_trace(go.Bar(name="Probability %",y=collab.scenario,x=collab.prob,orientation="h",marker_color="#FFD93D",marker_line_width=0))
        fig4.add_trace(go.Bar(name="Market Share %",y=collab.scenario,x=collab.share,orientation="h",marker_color="#A78BFA",marker_line_width=0))
        fig4.update_layout(barmode="group")
        apply_layout(fig4, h=280)
        st.plotly_chart(fig4, use_container_width=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("<hr style='margin:24px 0 8px'>",unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;color:#1a2e50;font-size:10px;letter-spacing:2px">
DA-AI PROJECT · DATA: OpenAI / Anthropic / Google / Meta / xAI Public Filings & Estimates · 2022–2030
</p>""",unsafe_allow_html=True)
