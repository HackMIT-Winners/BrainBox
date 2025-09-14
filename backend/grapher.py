import helix
from openai import OpenAI
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os
import cosine_similarity
from pyvis.network import Network

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

id1 = db.query('addIdea', {"user": "jeff", 
                           "text": "We need more marketting to promote our AI agents",
                           "embed": get_embedding("We need more marketing to promote our AI agents"),
                           "date": "09/14/2025"})[0]['n']['id']
# print(id1)

id2 = db.query('addIdea', {"user": "lisa", 
                           "text": "Agreed, one idea is to create a social media campaign",
                           "embed": get_embedding("Agreed, one idea is to create a social media campaign"),
                           "date": "09/14/2025"})[0]['n']['id']
# print(id2)

id3 = db.query('addIdea', {"user": "palmer", 
                           "text": "Yes, but I think we should also reach out to influencers",
                           "embed": get_embedding("Yes, but I think we should also reach out to influencers"),
                           "date": "09/14/2025"})[0]['n']['id']

res = db.query("linkIdeas", {"srcId": id1, "dstId": id2, "relation": "they are related", "date": "09/14/2025"})
res = db.query("linkIdeas", {"srcId": id1, "dstId": id3, "relation": "they are related", "date": "09/14/2025"})

def create_graph():
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
    # Show node text automatically
    net.write_html("graph.html")
    net.show_buttons(filter_=['physics'])
    net.set_options('var options = { interaction: {hover: true}, physics: {stabilization: true} }')

    html = net.generate_html()  # HTML string
    return HTMLResponse(content=html)

create_graph()