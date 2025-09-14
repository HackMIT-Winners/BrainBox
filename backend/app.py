import os
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import grapher
import meetingTranscript.TranscriptToGragh as transcript_processor
import helix
from openai import OpenAI
from dotenv import load_dotenv
import cosine_similarity
from pyvis.network import Network
from fastapi.middleware.cors import CORSMiddleware

similarity_threshold = 0.8  # Adjust this threshold as needed

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend's origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Pydantic models
class Node(BaseModel):
    user: str
    text: str
    date: str

class Edge(BaseModel):
    srcId: int
    dstId: int
    Relation: str

# --------- Endpoints -------

path = "/Users/xiangzhousun/Documents/GitHub/BrainBox/backend/meetingTranscript/exampleTranscript.txt"

with open(path, "r", encoding="utf-8") as f:
    text_string = f.read()

@app.get("/transcript")
async def process_transcript(text: str, meeting_name: str, speaker_name: str):
    try:
        print(os.getenv("OPENAI_API_KEY"))
        print("Processing transcript...")
        idea_events = await transcript_processor.process_transcript_file(path, meeting_name, speaker_name)
        embeddings = []
        ids = []
        print(f"Number of ideas extracted: {len(idea_events)}")
        
        
        for idea_event in idea_events:
            print(type(idea_event))
            embedding = get_embedding(idea_event['message_text'])
            embeddings.append(embedding)
            id = db.query('addIdea', {"user": idea_event['user_name'], 
                               "text": idea_event['message_text'],
                               "embed": embedding,
                               "date": idea_event['event_time']})[0]['n']['id']
            ids.append(id)
            print(f"Node ID: {id} (type: {type(id)})")
        return idea_events
        
        for i in range(len(idea_events)):
            for j in range(i+1, len(idea_events)):
                weight = cosine_similarity.cosine_edge_weight(embeddings[i], embeddings[j])
                if weight >= similarity_threshold:  # Adjust threshold as needed 
                    res = db.query("linkIdeas", {"srcId": id[i], "dstId": id[j], "Relation": ""})
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  

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

# Return a PyVis graph for visualization
@app.get("/graph")
def graph_json(limit: int = 2000):
    try:
        html = grapher.create_graph()
        return HTMLResponse(content=html)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
