import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import helix
from openai import OpenAI
from dotenv import load_dotenv
import cosine_similarity
from pyvis.network import Network

# --- Configure embedders (pick one) via env vars if you’ll use Embed()
# os.environ["OPENAI_API_KEY"] = "sk-..."     # or GEMINI_API_KEY / VOYAGE_API_KEY

net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
net.barnes_hut()

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Connect to a local helix instance
db = helix.Client(local=True, verbose=True, port=6969)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

app = FastAPI(title="KG Backend with HelixDB")

# --------- Pydantic models
class Node(BaseModel):
    user: str
    text: str
    date: str

class Edge(BaseModel):
    srcId: int
    dstId: int
    Relation: str

# --------- Endpoints

@app.post("/nodes")
def add_node(node: Node):
    try:
        embedding = get_embedding(node.text)
        id = db.query('addIdea', {"user": node.user, 
                           "text": node.text,
                           "embed": embedding,
                           "date": node.date})[0]['n']['id']
        
        return {"ok": True, "node": id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/edges")
def add_edge(edge: Edge):
    try:
        res = db.query("linkIdeas", {"srcId": edge.srcId, "dstId": edge.dstId, "Relation": edge.Relation})
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
    try:     
        net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
        net.barnes_hut()

        allNodes = db.query("getAllIdeas", {})[0]['ideas']
        # print(allNodes)
        for i, node in enumerate(allNodes):
            net.add_node(node['id'], label=node['text'])
            # print(node['id'])
        for i, node in enumerate(allNodes):
            allEdges = db.query("getAllConnectedIdeas", {"parent_id": node['id']})
            # print(allEdges)
            for edge in allEdges[0]['ideas']:
                weight = cosine_similarity.cosine_edge_weight(node['embed'], edge['embed'])
                print(weight)
                net.add_edge(node['id'], edge['id'], value=weight)
        
        net.write_html("graph.html")
        net.show_buttons(filter_=['physics'])
        net.set_options('var options = { interaction: {hover: true}, physics: {stabilization: true} }')

        html = net.generate_html()  # HTML string
        return HTMLResponse(content=html)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
