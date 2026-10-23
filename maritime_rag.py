import os
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DIR = "chroma_maritime_db"

def get_maritime_collection():
    # Initialize Persistent Local ChromaDB Client
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    # Use default ONNX CPU sentence-transformer embeddings (all-MiniLM-L6-v2)
    ef = embedding_functions.DefaultEmbeddingFunction()
    
    collection = client.get_or_create_collection(
        name="maritime_contracts_and_sow",
        embedding_function=ef
    )
    
    # Seed data if collection is empty
    if collection.count() == 0:
        documents = [
            (
                "contract_saudi_aramco_01",
                "Master Service Agreement - Saudi Crude (Ras Tanura to Sikka): Force Majeure explicitly excludes regional maritime blockade, state-level chokepoint closures, or geopolitical tensions in the Strait of Hormuz unless a direct military attack damages the vessel. Buyer is liable for 50% of war-risk insurance surcharges if transit is diverted around Africa.",
                {"supplier": "Saudi Aramco Export", "cargo": "Heavy Crude", "region": "Persian Gulf"}
            ),
            (
                "contract_iraq_basra_02",
                "Crude Supply Agreement - Basra Light to Paradip: Force Majeure covers territorial water closures. However, late-delivery financial penalties (0.5% per day of delay, capped at 10%) apply if alternative overland bypass pipelines or non-Hormuz routing options were operationally viable but unused by the supplier.",
                {"supplier": "State Organization for Marketing of Oil (SOMO)", "cargo": "Basra Medium", "region": "Persian Gulf"}
            ),
            (
                "contract_qatar_lng_03",
                "LNG Supply Contract - Mesaieed to Dahej: Force Majeure is strictly invoked only upon formal declaration of war or complete closure of territorial navigational lanes by the UN or coastal states. In the event of Hormuz closure, buyer and seller must negotiate a temporary freight redistribution fee within 48 hours.",
                {"supplier": "QatarEnergy LNG", "cargo": "LNG", "region": "Persian Gulf"}
            ),
            (
                "contract_russia_urals_04",
                "Alternative Sourcing Agreement - Primorsk to Vadinar (Urals Crude): Bypasses Middle Eastern chokepoints entirely. Standard commercial force majeure applies. No war-risk insurance surcharges or chokepoint closure penalties applicable. Guaranteed steady transit via Northern/Baltic corridors.",
                {"supplier": "Rosneft Trading / Russian Exporters", "cargo": "Urals Crude", "region": "Non-Gulf Alternative"}
            ),
            (
                "contract_us_wti_05",
                "North American Export Agreement - Corpus Christi to Sikka (WTI Light Sweet): Atlantic and Pacific transit corridors unaffected by Persian Gulf closures. Fixed freight rates locked for 90 days. Ideal emergency alternative supplier during regional Middle Eastern maritime disruptions.",
                {"supplier": "Permian Basin Exporters LLC", "cargo": "WTI Crude", "region": "Non-Gulf Alternative"}
            )
        ]
        
        for doc_id, text, metadata in documents:
            collection.add(
                ids=[doc_id],
                documents=[text],
                metadatas=[metadata]
            )
            
    return collection

def query_maritime_rag(query_text, n_results=2):
    collection = get_maritime_collection()
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    snippets = []
    if results and "documents" in results and results["documents"]:
        for doc_list in results["documents"]:
            for doc in doc_list:
                snippets.append(doc)
                
    return "\n\n".join(snippets)

if __name__ == "__main__":
    col = get_maritime_collection()
    print(f"✅ Maritime RAG vector store initialized! Total documents indexed: {col.count()}")
    print("\nSample RAG Query Test ('Force Majeure Hormuz closure penalties'):")
    print(query_maritime_rag("Force Majeure Hormuz closure penalties"))