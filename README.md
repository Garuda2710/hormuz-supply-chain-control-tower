# ⚡ Maritime Logistics Control Tower: Strait of Hormuz Resilience & Sourcing Engine

An enterprise-grade supply chain intelligence platform designed to simulate the macro-economic and logistical impacts of a Level-5 closure in the **Strait of Hormuz** on India's energy and industrial import supply chains. The platform combines real-time commodity pricing, relational geospatial route mapping, legal contract auditing (RAG), and a multi-agent AI advisory committee to optimize alternative non-Gulf procurement in real time.

---

## 🌟 Key Features

1. **📊 Quantitative Logistics Engine (`maritime_db.py`)**:
   - Calculates lead-time surges, transit day deltas, and operational bunker cost inflation across global trade lanes.
   - Evaluates inventory buffer depletion thresholds and models critical stockout risks for refineries.

2. **🗺️ Realistic Geospatial Maritime Maps (`Plotly`)**:
   - Dynamic multi-point waypoint tracking that traces realistic curves around coastlines and landmasses.
   - Automatically reroutes vulnerable Persian Gulf shipments past the **Cape of Good Hope** when chokepoints close, while highlighting secure non-Gulf corridors (Russia, US, Venezuela).

3. **⚖️ Legal RAG Pipeline (`maritime_rag.py`)**:
   - Indexes Master Service Agreements (MSAs), Force Majeure clauses, and war-risk insurance liabilities using **ChromaDB**.
   - Enables legal audits on whether chokepoint blockages constitute valid Force Majeure or trigger financial penalties.

4. **🤖 Multi-Agent AI Crisis Committee (`supply_agents.py`)**:
   - Powered by **Groq** (`openai/gpt-oss-120b`).
   - Coordinates three specialized personas: a **Geopolitical Risk Sentinel**, a **Contract Legal Auditor**, and a **Procurement Sourcing Strategist**.
   - Generates comprehensive executive crisis briefings with actionable alternative sourcing recommendations.

5. **📈 Live Market Intelligence (`yfinance`)**:
   - Pulls live spot market pricing for **Brent Crude (`BZ=F`)** and **WTI Crude (`CL=F`)** directly into the control tower dashboard.

---

## 🛠️ Tech Stack

* **Frontend / UI**: Streamlit
* **Geospatial Visualization**: Plotly (Scattergeo & Map Projections)
* **LLM & Agent Framework**: Groq API
* **Vector Database (RAG)**: ChromaDB (All-MiniLM-L6-v2 embeddings)
* **Relational Database**: SQLite & Pandas
* **Market Data API**: Yahoo Finance (`yfinance`)

---

## 📂 Project Structure

```text
hormuz-supply-chain/
│
├── app.py                 # Main Streamlit Dashboard & UI Control Tower
├── maritime_db.py         # SQLite Database, Trade Routes & Waypoint Schema
├── maritime_rag.py        # ChromaDB Vector Store & Contract Clause Indexer
├── supply_agents.py       # Groq Multi-Agent Simulation Engine
├── requirements.txt       # Project Dependencies
└── README.md              # Project Documentation