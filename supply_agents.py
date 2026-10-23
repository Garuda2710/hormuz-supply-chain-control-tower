import os
from dotenv import load_dotenv
from groq import Groq
from maritime_db import calculate_logistics_impact
from maritime_rag import query_maritime_rag

load_dotenv()
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def run_supply_chain_simulation(route_id="RT_01", current_inventory_days=10):
    # 1. Fetch Quantitative Logistics Metrics
    logistics = calculate_logistics_impact(route_id, current_inventory_days)
    
    if not logistics:
        return {
            "error": True,
            "ai_briefing": "❌ Error: Selected route ID could not be found in the maritime database."
        }
    
    # 2. Fetch Relevant Legal/Contract Clauses via RAG
    rag_context = query_maritime_rag(f"Force Majeure and war-risk insurance for {logistics['origin']} route")

    # 3. Construct System & User Prompts for Multi-Agent Panel
    system_prompt = (
        "You are an elite enterprise supply chain intelligence committee advising an Indian multinational energy and manufacturing conglomerate. "
        "Your task is to analyze a geopolitical maritime chokepoint closure (Strait of Hormuz), evaluate financial and inventory stockout risks, "
        "audit supplier contracts via legal RAG context, and provide actionable procurement mitigation recommendations (such as shifting to non-Gulf alternative suppliers like Russia or the US)."
    )

    user_prompt = f"""
    Analyze the following supply chain disruption scenario and generate a structured 3-part executive briefing:

    === 📊 QUANTITATIVE LOGISTICS METRICS ===
    - Trade Route: {logistics['origin']} ({logistics['port']}) ➔ India
    - Cargo Type: {logistics['cargo']}
    - Chokepoint Dependency: {logistics['chokepoint']}
    - Baseline Transit Time: {logistics['baseline_days']} days
    - Disrupted Transit Time (Cape of Good Hope Reroute): {logistics['disrupted_days']} days (Delay: +{logistics['delay_delta_days']} days)
    - Bunker Fuel / Operational Cost Surge: +{logistics['cost_surge_pct']}%
    - Current Inventory Buffer: {logistics['current_inventory_days']} days
    - Critical Stockout Risk: {'🚨 HIGH RISK (Inventory will run out before arrival!)' if logistics['stockout_risk'] else '✅ SAFE (Sufficient buffer)'}
    - Shortfall Duration: {max(0, logistics['disrupted_days'] - logistics['current_inventory_days'])} days without raw materials if unmitigated.

    === 📜 CONTRACTUAL & LEGAL RAG CONTEXT ===
    {rag_context}

    === 🎯 REQUIRED OUTPUT STRUCTURE ===
    Provide your response in three distinct sections:
    1. **🚨 Agent 1: Geopolitical & Risk Sentinel Assessment** (Evaluate the severity of the Hormuz closure and the impact on Indian import terminals).
    2. **⚖️ Agent 2: Contract & Legal Auditor Memo** (Audit the supplier's Force Majeure clauses and war-risk insurance liabilities based on the RAG context).
    3. **💡 Agent 3: Procurement & Alternative Sourcing Strategist** (Provide concrete recommendations on whether to invoke contract penalties, absorb bunker costs, or immediately shift procurement to non-Gulf alternative corridors like Russia or the US).
    """

    response = groq_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_completion_tokens=2500
    )

    return {
        "logistics": logistics,
        "rag_context": rag_context,
        "ai_briefing": response.choices[0].message.content
    }

if __name__ == "__main__":
    print("Testing Multi-Agent Supply Chain Simulation for Saudi Route (RT_01)...")
    res = run_supply_chain_simulation(route_id="RT_01", current_inventory_days=10)
    print("\n--- AI BRIEFING OUTPUT ---\n")
    print(res["ai_briefing"])