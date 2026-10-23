import sqlite3
import pandas as pd
import json

DB_NAME = "hormuz_supply_chain.db"

def init_maritime_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create Trade Routes Table with Waypoint Coordinates for Realistic Maritime Polylines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trade_routes (
            route_id TEXT PRIMARY KEY,
            origin_country TEXT,
            origin_port TEXT,
            destination_country TEXT,
            destination_port TEXT,
            cargo_type TEXT,
            baseline_transit_days INTEGER,
            disrupted_transit_days INTEGER,
            normal_bunker_cost_usd REAL,
            disrupted_bunker_cost_usd REAL,
            chokepoint_dependency TEXT,
            normal_lons TEXT,
            normal_lats TEXT,
            disrupted_lons TEXT,
            disrupted_lats TEXT,
            origin_lat REAL,
            origin_lon REAL,
            dest_lat REAL,
            dest_lon REAL
        )
    """)

    # Seed Comprehensive Global Trade Data with Realistic Maritime Waypoints
    routes_data = [
        # --- 1. SAUDI ARABIA (Ras Tanura -> Sikka) ---
        (
            "RT_01", "Saudi Arabia", "Ras Tanura", "India", "Sikka / Vadinar", "Crude Oil (Heavy Sour)", 5, 18, 45000, 78000, "Strait of Hormuz",
            json.dumps([50.16, 56.0, 60.0, 65.0, 69.67]), # Normal Lons (through Hormuz)
            json.dumps([26.65, 26.2, 22.0, 19.0, 22.47]), # Normal Lats
            json.dumps([50.16, 56.0, 50.0, 30.0, 15.0, 20.0, 35.0, 55.0, 65.0, 69.67]), # Disrupted Cape Route Lons
            json.dumps([26.65, 24.0, 12.0, -5.0, -34.0, -30.0, -10.0, 5.0, 18.0, 22.47]), # Disrupted Cape Route Lats
            26.65, 50.16, 22.47, 69.67
        ),
        # --- 2. IRAQ (Basra -> Paradip / Mumbai) ---
        (
            "RT_02", "Iraq", "Basra", "India", "Paradip / Mumbai", "Crude Oil (Basra Medium)", 7, 21, 52000, 89000, "Strait of Hormuz",
            json.dumps([48.65, 50.0, 57.0, 65.0, 72.82]),
            json.dumps([29.98, 27.5, 23.0, 18.0, 18.96]),
            json.dumps([48.65, 50.0, 45.0, 25.0, 10.0, -34.0, -25.0, 10.0, 50.0, 72.82]),
            json.dumps([29.98, 24.0, 10.0, -10.0, -35.0, -30.0, -15.0, 5.0, 15.0, 18.96]),
            29.98, 48.65, 18.96, 72.82
        ),
        # --- 3. QATAR (Mesaieed -> Dahej) ---
        (
            "RT_03", "Qatar", "Mesaieed", "India", "Dahej / Hazira", "Liquefied Natural Gas (LNG)", 4, 16, 48000, 82000, "Strait of Hormuz",
            json.dumps([51.54, 57.0, 62.0, 67.0, 72.58]),
            json.dumps([24.99, 25.5, 22.0, 20.0, 21.70]),
            json.dumps([51.54, 55.0, 48.0, 25.0, -34.0, -28.0, 5.0, 60.0, 72.58]),
            json.dumps([24.99, 23.0, 10.0, -10.0, -35.0, -25.0, 5.0, 18.0, 21.70]),
            24.99, 51.54, 21.70, 72.58
        ),
        # --- 4. UAE (Jebel Ali -> Nhava Sheva) ---
        (
            "RT_04", "UAE", "Jebel Ali", "India", "Nhava Sheva", "Industrial Containers", 4, 15, 42000, 74000, "Strait of Hormuz",
            json.dumps([55.06, 58.0, 63.0, 68.0, 72.95]),
            json.dumps([25.01, 24.5, 21.0, 19.0, 18.94]),
            json.dumps([55.06, 52.0, 40.0, 20.0, -34.0, -25.0, 10.0, 60.0, 72.95]),
            json.dumps([25.01, 23.0, 5.0, -15.0, -35.0, -30.0, 5.0, 15.0, 18.94]),
            25.01, 55.06, 18.94, 72.95
        ),
        # --- 5. RUSSIA (Primorsk -> Vadinar) [Non-Gulf Alternative] ---
        (
            "RT_ALT_05", "Russia", "Primorsk / Novorossiysk", "India", "Vadinar / Paradeep", "Urals Crude (Medium Sour)", 24, 26, 65000, 71000, "None (Bypasses Hormuz)",
            json.dumps([28.63, 18.0, 5.0, -5.0, 15.0, 32.5, 45.0, 58.0, 69.67]),
            json.dumps([60.35, 55.0, 40.0, 36.0, 32.0, 31.2, 12.0, 18.0, 22.47]),
            json.dumps([28.63, 18.0, 5.0, -5.0, 15.0, 32.5, 45.0, 58.0, 69.67]),
            json.dumps([60.35, 55.0, 40.0, 36.0, 32.0, 31.2, 12.0, 18.0, 22.47]),
            60.35, 28.63, 22.47, 69.67
        ),
        # --- 6. USA (Corpus Christi -> Sikka) [Non-Gulf Alternative] ---
        (
            "RT_ALT_06", "USA", "Corpus Christi", "India", "Sikka", "WTI Crude / Light Sweet", 35, 38, 85000, 92000, "None (Atlantic Corridor)",
            json.dumps([-97.39, -85.0, -60.0, -30.0, -10.0, 15.0, 32.5, 50.0, 69.67]),
            json.dumps([27.80, 24.0, 20.0, 15.0, 10.0, 32.0, 31.2, 15.0, 22.47]),
            json.dumps([-97.39, -85.0, -60.0, -30.0, -10.0, 15.0, 32.5, 50.0, 69.67]),
            json.dumps([27.80, 24.0, 20.0, 15.0, 10.0, 32.0, 31.2, 15.0, 22.47]),
            27.80, -97.39, 22.47, 69.67
        ),
        # --- 7. VENEZUELA (Jose Terminal -> Mumbai) [Non-Gulf Alternative] ---
        (
            "RT_ALT_07", "Venezuela", "Jose Terminal", "India", "Mumbai", "Venezuelan Heavy Crude", 32, 35, 80000, 87000, "None (Atlantic Corridor)",
            json.dumps([-64.70, -50.0, -30.0, -10.0, 15.0, 32.5, 50.0, 65.0, 72.82]),
            json.dumps([10.15, 5.0, 0.0, -5.0, 10.0, 31.2, 15.0, 12.0, 18.96]),
            json.dumps([-64.70, -50.0, -30.0, -10.0, 15.0, 32.5, 50.0, 65.0, 72.82]),
            json.dumps([10.15, 5.0, 0.0, -5.0, 10.0, 31.2, 15.0, 12.0, 18.96]),
            10.15, -64.70, 18.96, 72.82
        )
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO trade_routes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, routes_data)

    conn.commit()
    conn.close()

def get_all_routes():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql("SELECT * FROM trade_routes", conn)
    conn.close()
    return df

def calculate_logistics_impact(route_id, current_inventory_days=12):
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql(f"SELECT * FROM trade_routes WHERE route_id = '{route_id}'", conn)
    conn.close()
    
    if df.empty:
        return None
    
    route = df.iloc[0]
    baseline_days = route["baseline_transit_days"]
    disrupted_days = route["disrupted_transit_days"]
    delay_delta = disrupted_days - baseline_days
    
    cost_surge_pct = round(((route["disrupted_bunker_cost_usd"] - route["normal_bunker_cost_usd"]) / route["normal_bunker_cost_usd"]) * 100, 1)
    is_vulnerable = "Hormuz" in route["chokepoint_dependency"]
    
    stockout_risk = current_inventory_days < disrupted_days if is_vulnerable else False

    # Select Waypoints based on vulnerability & disruption
    lons = json.loads(route["disrupted_lons"] if is_vulnerable else route["normal_lons"])
    lats = json.loads(route["disrupted_lats"] if is_vulnerable else route["normal_lats"])

    return {
        "route_id": route["route_id"],
        "origin": route["origin_country"],
        "port": route["origin_port"],
        "cargo": route["cargo_type"],
        "chokepoint": route["chokepoint_dependency"],
        "baseline_days": baseline_days,
        "disrupted_days": disrupted_days,
        "delay_delta_days": delay_delta,
        "cost_surge_pct": cost_surge_pct,
        "stockout_risk": stockout_risk,
        "is_vulnerable": is_vulnerable,
        "current_inventory_days": current_inventory_days,
        "route_lons": lons,
        "route_lats": lats,
        "origin_lat": route["origin_lat"],
        "origin_lon": route["origin_lon"],
        "dest_lat": route["dest_lat"],
        "dest_lon": route["dest_lon"]
    }

if __name__ == "__main__":
    init_maritime_database()
    print("✅ Maritime Database updated with realistic waypoint polylines!")