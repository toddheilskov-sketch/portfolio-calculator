import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(page_title="Portfolio Calculator", page_icon="💰", layout="wide")

# --- Theme Toggle ---
st.sidebar.markdown("---")
theme = st.sidebar.radio("🎨 Theme", ["Light", "Dark"], index=0)

# --- CSS Themes ---
dark_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(74, 144, 217, 0.3);
    }
    [data-testid="stSidebar"] * { color: #e0e0e0 !important; }
    h1 {
        background: linear-gradient(90deg, #4A90D9, #27AE60);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        padding-bottom: 0.5rem;
    }
    h2, h3 {
        color: #4A90D9 !important;
        font-weight: 600 !important;
        border-bottom: 1px solid rgba(74, 144, 217, 0.3);
        padding-bottom: 0.3rem;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(74, 144, 217, 0.15), rgba(39, 174, 96, 0.1));
        border: 1px solid rgba(74, 144, 217, 0.3);
        border-radius: 12px;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 4px 15px rgba(74, 144, 217, 0.1);
    }
    [data-testid="stMetricLabel"] {
        color: #a0a0b0 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(74, 144, 217, 0.2);
        border-radius: 10px;
        overflow: hidden;
    }
    hr { border-color: rgba(74, 144, 217, 0.2) !important; margin: 1.5rem 0 !important; }
    p, .stMarkdown { color: #c0c0d0 !important; }
    label { color: #a0a0b0 !important; font-size: 0.9rem !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1a1a2e; }
    ::-webkit-scrollbar-thumb { background: #4A90D9; border-radius: 3px; }
</style>
"""

light_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #f0f4ff 0%, #ffffff 50%, #f5f9f5 100%);
        font-family: 'Segoe UI', sans-serif;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f4ff 0%, #e8f0fe 100%);
        border-right: 2px solid rgba(26, 115, 232, 0.2);
    }
    [data-testid="stSidebar"] * { color: #2c3e50 !important; }
    h1 {
        background: linear-gradient(90deg, #1a73e8, #0d9e6e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        padding-bottom: 0.5rem;
    }
    h2, h3 {
        color: #1a73e8 !important;
        font-weight: 600 !important;
        border-bottom: 2px solid rgba(26, 115, 232, 0.2);
        padding-bottom: 0.3rem;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(26, 115, 232, 0.08), rgba(13, 158, 110, 0.06));
        border: 1px solid rgba(26, 115, 232, 0.25);
        border-radius: 12px;
        padding: 1rem 1.2rem !important;
        box-shadow: 0 2px 12px rgba(26, 115, 232, 0.1);
    }
    [data-testid="stMetricLabel"] {
        color: #5f6368 !important;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricValue"] {
        color: #1a1a2e !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(26, 115, 232, 0.2);
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    hr { border-color: rgba(26, 115, 232, 0.15) !important; margin: 1.5rem 0 !important; }
    p, .stMarkdown { color: #3c4043 !important; }
    label { color: #5f6368 !important; font-size: 0.9rem !important; }
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #f0f4ff; }
    ::-webkit-scrollbar-thumb { background: #1a73e8; border-radius: 3px; }
</style>
"""

# Apply selected theme
st.markdown(dark_css if theme == "Dark" else light_css, unsafe_allow_html=True)

# Subtitle color based on theme
subtitle_color = "#a0a0b0" if theme == "Dark" else "#5f6368"

st.title("💰 Portfolio Growth Calculator")
st.markdown(f'<p style="color:{subtitle_color}; font-size:1.1rem; margin-top:-1rem;">Monte Carlo simulation & compound growth analysis</p>', unsafe_allow_html=True)

# --- Inputs (sidebar) ---
st.sidebar.header("Your Inputs")
initial_balance = st.sidebar.number_input("Initial Balance ($)", min_value=0.0, value=10000.0, step=1000.0)
annual_return = st.sidebar.number_input("Expected Annual Return (%)", min_value=0.0, max_value=100.0, value=7.0, step=0.5)
years = st.sidebar.slider("Number of Years", min_value=1, max_value=50, value=10)
annual_contribution = st.sidebar.number_input("Annual Contribution ($)", min_value=0.0, value=2000.0, step=500.0)

st.sidebar.divider()
st.sidebar.header("Monte Carlo Settings")
volatility = st.sidebar.slider("Annual Volatility / Risk (%)", min_value=1, max_value=40, value=15,
                                help="Standard deviation of annual returns. S&P 500 is historically ~15%")
simulations = st.sidebar.slider("Number of Simulations", min_value=100, max_value=2000, value=500, step=100)

# --- Deterministic Calculation (base case) ---
rate = annual_return / 100
balance = initial_balance
total_contributions = 0
data = []

for year in range(1, years + 1):
    balance += annual_contribution
    total_contributions += annual_contribution
    new_balance = balance * (1 + rate)
    annual_gain = new_balance - balance
    total_gain = new_balance - (initial_balance + total_contributions)
    total_invested = initial_balance + total_contributions
    data.append({
        "Year": year,
        "Balance": round(new_balance, 2),
        "Annual Gain": round(annual_gain, 2),
        "Total Gain": round(total_gain, 2),
        "Total Contributed": round(total_contributions, 2),
        "Initial + Contributions": round(total_invested, 2),
        "Market Gains": round(total_gain, 2)
    })
    balance = new_balance

total_invested = initial_balance + total_contributions
df = pd.DataFrame(data)

# --- Monte Carlo Simulation ---
np.random.seed(42)
vol = volatility / 100
all_simulations = []

for _ in range(simulations):
    sim_balance = initial_balance
    sim_path = []
    for year in range(1, years + 1):
        sim_balance += annual_contribution
        annual_rate = np.random.normal(rate, vol)
        sim_balance *= (1 + annual_rate)
        sim_path.append(max(sim_balance, 0))
    all_simulations.append(sim_path)

sim_array = np.array(all_simulations)

# Percentiles
p5  = np.percentile(sim_array,  5, axis=0)
p10 = np.percentile(sim_array, 10, axis=0)
p25 = np.percentile(sim_array, 25, axis=0)
p50 = np.percentile(sim_array, 50, axis=0)
p75 = np.percentile(sim_array, 75, axis=0)
p90 = np.percentile(sim_array, 90, axis=0)
p95 = np.percentile(sim_array, 95, axis=0)
avg = np.mean(sim_array, axis=0)

year_range = list(range(1, years + 1))
final_balances = sim_array[:, -1]

# --- Summary Cards ---
st.subheader("Summary — Base Case")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Final Balance (Expected)", f"${balance:,.2f}")
col2.metric("Total Invested", f"${total_invested:,.2f}")
col3.metric("Market Gains", f"${balance - total_invested:,.2f}")
col4.metric("Total Return", f"{((balance - total_invested) / total_invested) * 100:,.1f}%")

st.divider()

# --- Monte Carlo Chart ---
st.subheader(f"Monte Carlo Simulation — {simulations} Scenarios")
st.write("Shows the range of possible outcomes based on market volatility. The shaded bands represent where most simulations landed.")

fig_mc = go.Figure()

fig_mc.add_trace(go.Scatter(
    x=year_range + year_range[::-1],
    y=list(p90) + list(p10[::-1]),
    fill="toself",
    fillcolor="rgba(74, 144, 217, 0.15)",
    line=dict(color="rgba(255,255,255,0)"),
    name="10th–90th Percentile"
))

fig_mc.add_trace(go.Scatter(
    x=year_range + year_range[::-1],
    y=list(p75) + list(p25[::-1]),
    fill="toself",
    fillcolor="rgba(74, 144, 217, 0.30)",
    line=dict(color="rgba(255,255,255,0)"),
    name="25th–75th Percentile"
))

fig_mc.add_trace(go.Scatter(
    x=year_range, y=p50,
    mode="lines",
    name="Median Outcome",
    line=dict(color="#4A90D9", width=2, dash="dash")
))

fig_mc.add_trace(go.Scatter(
    x=year_range, y=df["Balance"],
    mode="lines",
    name="Expected (Base Case)",
    line=dict(color="#E74C3C", width=2)
))

fig_mc.update_layout(
    xaxis_title="Year",
    yaxis_title="Portfolio Value ($)",
    yaxis_tickformat="$,.0f",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=500,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)

st.plotly_chart(fig_mc, use_container_width=True)

# --- Outcome Distribution ---
st.subheader("Distribution of Final Balances")
col_a, col_b = st.columns([2, 1])

with col_a:
    fig_hist = go.Figure()
    fig_hist.add_trace(go.Histogram(
        x=final_balances,
        nbinsx=50,
        marker_color="#4A90D9",
        opacity=0.75,
        name="Simulated Final Balances"
    ))
    fig_hist.add_vline(x=balance, line_color="#E74C3C", line_width=2,
                       annotation_text="Base Case", annotation_position="top right")
    fig_hist.add_vline(x=np.median(final_balances), line_color="#27AE60", line_width=2,
                       annotation_text="Median", annotation_position="top left")
    fig_hist.update_layout(
        xaxis_title="Final Balance ($)",
        yaxis_title="Number of Simulations",
        xaxis_tickformat="$,.0f",
        height=350,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col_b:
    st.subheader("Outcome Odds")
    st.metric("Median Outcome", f"${np.median(final_balances):,.0f}")
    st.metric("Best Case (90th %)", f"${p90[-1]:,.0f}")
    st.metric("Worst Case (10th %)", f"${p10[-1]:,.0f}")
    prob_positive = np.mean(final_balances > total_invested) * 100
    prob_double = np.mean(final_balances > total_invested * 2) * 100
    st.metric("Probability of Profit", f"{prob_positive:.1f}%")
    st.metric("Probability of Doubling", f"{prob_double:.1f}%")

st.divider()

# --- Stacked Bar Chart ---
st.subheader("Your Money vs. Market Gains Over Time")

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=df["Year"], y=df["Initial + Contributions"],
    name="Your Money (Initial + Contributions)",
    marker_color="#4A90D9"
))
fig_bar.add_trace(go.Bar(
    x=df["Year"], y=df["Market Gains"],
    name="Market Gains",
    marker_color="#27AE60"
))
fig_bar.update_layout(
    barmode="stack",
    xaxis_title="Year",
    yaxis_title="Portfolio Value ($)",
    yaxis_tickformat="$,.0f",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=400,
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_bar, use_container_width=True)

# --- Table ---
st.subheader("Year-by-Year Breakdown (Base Case)")
st.dataframe(df[["Year", "Balance", "Annual Gain", "Total Gain", "Total Contributed"]],
             use_container_width=True)

st.divider()

# --- Percentile Table ---
st.subheader("Monte Carlo Percentile Table — Portfolio Balance by Year")
st.write("Shows the range of simulated portfolio balances at each year across key percentiles and the average.")

percentile_data = []
for i, year in enumerate(year_range):
    percentile_data.append({
        "Year": year,
        "5th Percentile": f"${p5[i]:,.0f}",
        "25th Percentile": f"${p25[i]:,.0f}",
        "50th Percentile (Median)": f"${p50[i]:,.0f}",
        "Average": f"${avg[i]:,.0f}",
        "75th Percentile": f"${p75[i]:,.0f}",
        "95th Percentile": f"${p95[i]:,.0f}",
        "Base Case": f"${df['Balance'].iloc[i]:,.0f}",
    })

df_percentiles = pd.DataFrame(percentile_data)
st.dataframe(df_percentiles, use_container_width=True, hide_index=True)

st.divider()

# --- Overall Investment Period Summary Table ---
st.subheader("Overall Investment Period Summary")
st.write("Summary statistics for the **final balance** across all simulations at the end of the full investment period.")

overall_summary = pd.DataFrame([
    {"Statistic": "5th Percentile (Worst Case)",      "Final Balance": f"${np.percentile(final_balances, 5):,.0f}",  "vs. Base Case": f"{((np.percentile(final_balances, 5) / balance) - 1) * 100:+.1f}%"},
    {"Statistic": "25th Percentile (Below Average)",  "Final Balance": f"${np.percentile(final_balances, 25):,.0f}", "vs. Base Case": f"{((np.percentile(final_balances, 25) / balance) - 1) * 100:+.1f}%"},
    {"Statistic": "50th Percentile (Median)",         "Final Balance": f"${np.median(final_balances):,.0f}",          "vs. Base Case": f"{((np.median(final_balances) / balance) - 1) * 100:+.1f}%"},
    {"Statistic": "Average (Mean)",                   "Final Balance": f"${np.mean(final_balances):,.0f}",            "vs. Base Case": f"{((np.mean(final_balances) / balance) - 1) * 100:+.1f}%"},
    {"Statistic": "75th Percentile (Above Average)",  "Final Balance": f"${np.percentile(final_balances, 75):,.0f}", "vs. Base Case": f"{((np.percentile(final_balances, 75) / balance) - 1) * 100:+.1f}%"},
    {"Statistic": "95th Percentile (Best Case)",      "Final Balance": f"${np.percentile(final_balances, 95):,.0f}", "vs. Base Case": f"{((np.percentile(final_balances, 95) / balance) - 1) * 100:+.1f}%"},
    {"Statistic": "Base Case (Expected)",             "Final Balance": f"${balance:,.0f}",                           "vs. Base Case": "—"},
])

st.dataframe(overall_summary, use_container_width=True, hide_index=True)
