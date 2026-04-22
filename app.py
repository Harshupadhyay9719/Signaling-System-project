import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Drug Dashboard", layout="wide")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("drugs_dataset.csv")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.big-title {
    font-size: 40px;
    font-weight: bold;
    color: #4CAF50;
}
.card {
    background-color: #1e1e1e;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<p class="big-title"> Drug Decay Intelligence Dashboard</p>', unsafe_allow_html=True)
st.markdown("####  Real-time Pharmacokinetic Modeling using Laplace Transform")

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙️ Controls")

drug_name = st.sidebar.selectbox("Select Medicine", df["Drug"])
dose = st.sidebar.slider("Dose (mg)", 10, 500, 100)
time_range = st.sidebar.slider("Time Range (hours)", 10, 300, 120)

# ---------------- GET DATA ----------------
row = df[df["Drug"] == drug_name].iloc[0]
half_life = row["Half_life_hours"]
k = row["k"]

# ---------------- METRIC CARDS ----------------
col1, col2, col3 = st.columns(3)

col1.markdown(f'<div class="card">🧪 Half-life<br><h2>{round(half_life,2)} hrs</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="card">⚡ Elimination k<br><h2>{round(k,4)}</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="card">⏱ Neutral Time<br><h2>{round(5*half_life,2)} hrs</h2></div>', unsafe_allow_html=True)

# ---------------- GRAPH ----------------
t = np.linspace(0, time_range, 500)
C = dose * np.exp(-k * t)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=t,
    y=C,
    mode='lines',
    name=drug_name,
    line=dict(width=4, color="#00FFAA"),
    fill='tozeroy'
))

fig.add_hline(y=20, line_dash="dash", line_color="yellow", annotation_text="Min Effective")
fig.add_hline(y=80, line_dash="dash", line_color="red", annotation_text="Toxic Limit")

fig.update_layout(
    template="plotly_dark",
    title=" Drug Concentration Dynamics",
    xaxis_title="Time (hours)",
    yaxis_title="Concentration",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- TABS ----------------
tab1, tab2 = st.tabs([" Insights", " Compare Drugs"])

# -------- INSIGHTS --------
with tab1:
    st.success(f"""
    ✔ {drug_name} will become negligible after ~ **{round(5*half_life,2)} hours**
    
    ✔ Higher k → faster elimination  
    ✔ Lower k → longer drug effect  
    """)

# -------- COMPARISON --------
with tab2:
    drug2 = st.selectbox("Select second drug", df["Drug"], index=1)

    if drug2:
        row2 = df[df["Drug"] == drug2].iloc[0]
        k2 = row2["k"]

        C2 = dose * np.exp(-k2 * t)

        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(x=t, y=C, name=drug_name))
        fig2.add_trace(go.Scatter(x=t, y=C2, name=drug2))

        fig2.update_layout(template="plotly_dark", title="Drug Comparison")

        st.plotly_chart(fig2, use_container_width=True)