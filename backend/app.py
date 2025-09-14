import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import helix

# --- Configure embedders (pick one) via env vars if you’ll use Embed()
# os.environ["OPENAI_API_KEY"] = "sk-..."     # or GEMINI_API_KEY / VOYAGE_API_KEY

# Connect to local HelixDB
db = helix.Client(local=True, verbose=True)  # default port 6969

app = FastAPI(title="KG Backend with HelixDB")

# --------- Pydantic models
class Node(BaseModel):
    text: str

class Edge(BaseModel):
    srcId: int
    dstId: int
    Relation: str

# --------- Endpoints

@app.post("/nodes")
def add_node(node: Node):
    try:
        res = db.query('addNode', {"text": node.text})
        return {"ok": True, "node": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/edges")
def add_edge(edge: Edge):
    try:
        res = db.query("linkNodes", {"srcId": edge.srcId, "dstId": edge.dstId, "Relation": edge.Relation})
        return {"ok": True, "edge": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
def search(q: str = Query(...), topK: int = Query(5, ge=1, le=50)):
    try:
        res = db.query("semanticSearch", {"q": q, "topK": topK})
        return {"ok": True, "results": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Return Cytoscape-friendly graph JSON for visualization
@app.get("/graph")
def graph_json(limit: int = 200):
    """
    Minimal example: pull up to `limit` Things and RELATES_TO edges.
    In practice you’d add HQL queries that return exactly what you want
    (e.g., ego-net around a node, or paths between nodes), then call them here.
    """
    try:
        # Example HQL inline: fetch nodes & edges (add a real query in your .hx for performance)
        nodes = db.query("selectThings", {"limit": limit}) if db.has_query("selectThings") else []
        edges = db.query("selectEdges", {"limit": limit}) if db.has_query("selectEdges") else []

        # map to Cytoscape elements: [{ data: { id, label }}, { data: { id, source, target }}]
        elements = []
        for n in nodes:
            elements.append({"data": {"id": n["id"], "label": n.get("title", n["id"])} })
        for e in edges:
            edge_id = f'{e["src"]}->{e["dst"]}'
            elements.append({"data": {"id": edge_id, "source": e["src"], "target": e["dst"]}})
        return {"elements": elements}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
