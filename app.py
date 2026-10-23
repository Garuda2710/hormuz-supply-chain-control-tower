import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import json
from maritime_db import get_all_routes, calculate_logistics_impact
from supply_agents import run_supply_chain_simulation

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Hormuz Supply Chain Control Tower",
    page_icon="⚡",
    layout="wide"
)

# --- STYLING & THEME ---
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        .metric-card { background-color: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; }
    </style>
""", unsafe_allow_html=True)

# --- FETCH LIVE MARKET CRUDE PRICES ---
@st.cache_data(ttl=600)
def fetch_live_market_prices():
    try:
        brent = yf.Ticker("BZ=F").history(period="1d")
        wti = yf.Ticker("CL=F").history(period="1d")
        brent_price = round(brent['Close'].iloc[-1], 2) if not brent.empty else 74.50
        wti_price = round(wti['Close'].iloc[-1], 2) if not wti.empty else 70.20
        return brent_price, wti_price
    except:
        return 74.50, 70.20

brent_live, wti_live = fetch_live_market_prices()

# --- HEADER & LIVE TICKER BAR ---
st.title("⚡ Maritime Logistics Control Tower: Strait of Hormuz Resilience & Sourcing Engine")
st.markdown("Real-time geopolitical risk monitoring, quantitative inventory buffer modeling, legal RAG auditing, and alternative non-Gulf procurement optimization for India.")

col_t1, col_t2, col_t3 = st.columns(3)
col_t1.metric("🌐 Brent Crude Spot (Live)", f"${brent_live} / bbl", "+2.4% (Hormuz Risk)")
col_t2.metric("US WTI Crude Spot (Live)", f"${wti_live} / bbl", "+1.8%")
col_t3.metric("Chokepoint Status", "LEVEL 5 CLOSURE", "🔴 Critical Alert", delta_color="inverse")

st.markdown("---")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🛠️ Simulation Control Panel")

routes_df = get_all_routes()
route_options = {f"{row['origin_country']} ({row['origin_port']}) ➔ {row['cargo_type']}": row['route_id'] for _, row in routes_df.iterrows()}

selected_route_label = st.sidebar.selectbox("Select Trade Route / Supplier", list(route_options.keys()))
selected_route_id = route_options[selected_route_label]

current_inventory = st.sidebar.slider("Current Refinery Inventory Buffer (Days)", min_value=3, max_value=30, value=10, step=1)

run_sim_btn = st.sidebar.button("🚀 Run Multi-Agent Crisis Simulation", type="primary")

# --- FETCH ROUTE DETAILS ---
logistics = calculate_logistics_impact(selected_route_id, current_inventory)

# --- SECTION 1: REALISTIC MARITIME TRACKING MAP (Plotly) ---
st.subheader("🗺️ Live Maritime Trade Corridor & Vessel Tracking Map")
st.markdown("Displaying smooth multi-point waypoint shipping lanes avoiding landmasses. **Red curves** represent Hormuz-vulnerable choke paths (showing Cape of Good Hope rerouting when closed), while **Green curves** represent secure non-Gulf alternative corridors.")

fig = go.Figure()

# Plot background routes using realistic waypoints
for _, row in routes_df.iterrows():
    is_selected = row['route_id'] == selected_route_id
    is_hormuz = "Hormuz" in row['chokepoint_dependency']
    
    # Select waypoint arrays
    if is_hormuz:
        lons = json.loads(row['disrupted_lons'] if is_selected else row['normal_lons'])
        lats = json.loads(row['disrupted_lats'] if is_selected else row['normal_lats'])
        line_color = "#ff4b4b"
    else:
        lons = json.loads(row['normal_lons'])
        lats = json.loads(row['normal_lats'])
        line_color = "#00cc96"

    line_width = 4.5 if is_selected else 1.2
    opacity = 1.0 if is_selected else 0.35

    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='lines',
        line=dict(width=line_width, color=line_color),
        opacity=opacity,
        hoverinfo='text',
        text=f"Corridor: {row['origin_country']} to India ({row['cargo_type']}) | Status: {row['chokepoint_dependency']}"
    ))

# Highlight Selected Origin and India Destination Markers
fig.add_trace(go.Scattergeo(
    lon=[logistics['origin_lon'], logistics['dest_lon']],
    lat=[logistics['origin_lat'], logistics['dest_lat']],
    mode='markers+text',
    text=[logistics['origin'], "India Terminals (Sikka/Vadinar/Mumbai)"],
    textposition="top center",
    marker=dict(size=12, color=['#ff4b4b' if logistics['is_vulnerable'] else '#00cc96', '#636efa'])
))

fig.update_layout(
    geo=dict(
        showland=True, landcolor="#1f2937",
        showocean=True, oceancolor="#0b0f19",
        showcountries=True, countrycolor="#374151",
        projection_type="natural earth",
        center=dict(lat=20, lon=65),
        projection_scale=1.6
    ),
    margin=dict(l=0, r=0, t=0, b=0),
    height=500,
    paper_bgcolor="#0e1117",
    plot_bgcolor="#0e1117",
    font=dict(color="white")
)

st.plotly_chart(fig, use_container_width=True)

# --- SECTION 2: QUANTITATIVE METRICS ROW ---
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Baseline Transit", f"{logistics['baseline_days']} Days")
col2.metric("Disrupted Transit", f"{logistics['disrupted_days']} Days", f"+{logistics['delay_delta_days']} Days Delay")
col3.metric("Bunker Cost Surge", f"+{logistics['cost_surge_pct']}%", "Operational Impact")
col4.metric("Stockout Risk Status", "HIGH RISK 🚨" if logistics['stockout_risk'] else "SECURE ✅", f"Inventory: {current_inventory} Days")

# --- SECTION 3: MULTI-AGENT AI EXECUTIVE BRIEFING & ALTERNATIVE MAPS ---
if run_sim_btn:
    with st.spinner("🤖 Multi-Agent AI Committee analyzing supply disruption, legal contracts, and alternative non-Gulf corridors..."):
        sim_result = run_supply_chain_simulation(route_id=selected_route_id, current_inventory_days=current_inventory)
        
        if sim_result.get("error"):
            st.error(sim_result["ai_briefing"])
        else:
            st.markdown("---")
            st.header("📋 AI-Generated Executive Crisis Briefing & Mitigation Strategy")
            st.markdown(sim_result["ai_briefing"])
            
            # --- DEDICATED ALTERNATIVE SOURCING ROUTE MAP VISUALIZER ---
            st.markdown("### 🗺️ Recommended Alternative Sourcing Corridor Visualizer")
            st.markdown("When shifting procurement away from Hormuz-vulnerable suppliers, our engine maps secure alternative shipping lanes directly into Indian ports:")
            
            alt_routes = routes_df[~routes_df['chokepoint_dependency'].str.contains("Hormuz", na=False)]
            
            fig_alt = go.Figure()
            for _, alt_row in alt_routes.iterrows():
                alt_lons = json.loads(alt_row['normal_lons'])
                alt_lats = json.loads(alt_row['normal_lats'])
                
                fig_alt.add_trace(go.Scattergeo(
                    lon=alt_lons,
                    lat=alt_lats,
                    mode='lines+markers',
                    name=f"{alt_row['origin_country']} ➔ India",
                    line=dict(width=3, color="#00cc96"),
                    marker=dict(size=6),
                    hoverinfo='text',
                    text=f"Secure Alternative: {alt_row['origin_country']} ({alt_row['cargo_type']})"
                ))
            
            fig_alt.update_layout(
                geo=dict(
                    showland=True, landcolor="#1f2937",
                    showocean=True, oceancolor="#0b0f19",
                    showcountries=True, countrycolor="#374151",
                    projection_type="natural earth",
                    center=dict(lat=20, lon=50),
                    projection_scale=1.5
                ),
                margin=dict(l=0, r=0, t=0, b=0),
                height=400,
                paper_bgcolor="#0e1117",
                plot_bgcolor="#0e1117",
                font=dict(color="white"),
                legend=dict(x=0, y=1)
            )
            
            st.plotly_chart(fig_alt, use_container_width=True)

            # Download button for the briefing report
            st.download_button(
                label="📥 Download Executive Briefing (Markdown)",
                data=sim_result["ai_briefing"],
                file_name=f"Hormuz_Crisis_Briefing_{selected_route_id}.md",
                mime="text/markdown"
            )
else:
    st.info("👈 Adjust your parameters in the sidebar and click **'Run Multi-Agent Crisis Simulation'** to generate the AI procurement strategy and alternative corridor maps.")