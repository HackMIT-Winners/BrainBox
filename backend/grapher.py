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

# ---------- New Ideas (id4 -> id10) ----------

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

id4 = db.query('addIdea', {
    "user": "nina",
    "text": "Let's A/B test landing pages to lift conversion.",
    "embed": get_embedding("Let's A/B test landing pages to lift conversion."),
    "date": "09/15/2025"
})[0]['n']['id']

id5 = db.query('addIdea', {
    "user": "arjun",
    "text": "Define KPIs for the campaign: CTR, CAC, and 7-day retention.",
    "embed": get_embedding("Define KPIs for the campaign: CTR, CAC, and 7-day retention."),
    "date": "09/15/2025"
})[0]['n']['id']

id6 = db.query('addIdea', {
    "user": "maria",
    "text": "Prototype a TikTok/Reels series showing real AI-agent use cases.",
    "embed": get_embedding("Prototype a TikTok/Reels series showing real AI-agent use cases."),
    "date": "09/16/2025"
})[0]['n']['id']

id7 = db.query('addIdea', {
    "user": "daniel",
    "text": "Partner with niche newsletters and podcasts frequented by PMs.",
    "embed": get_embedding("Partner with niche newsletters and podcasts frequented by PMs."),
    "date": "09/17/2025"
})[0]['n']['id']

id8 = db.query('addIdea', {
    "user": "zoe",
    "text": "Launch a referral program with tiered rewards for successful invites.",
    "embed": get_embedding("Launch a referral program with tiered rewards for successful invites."),
    "date": "09/18/2025"
})[0]['n']['id']

id9 = db.query('addIdea', {
    "user": "kai",
    "text": "Allocate budget and run a two-week pilot across 3 channels.",
    "embed": get_embedding("Allocate budget and run a two-week pilot across 3 channels."),
    "date": "09/19/2025"
})[0]['n']['id']

id10 = db.query('addIdea', {
    "user": "oliver",
    "text": "Create an onboarding microsite with interactive agent demos.",
    "embed": get_embedding("Create an onboarding microsite with interactive agent demos."),
    "date": "09/20/2025"
})[0]['n']['id']

# ---------- Links between Ideas ----------
# connects social campaign + experiments + measurement
res = db.query("linkIdeas", {"srcId": id2, "dstId": id4, "relation": "refines",       "date": "09/15/2025"})
res = db.query("linkIdeas", {"srcId": id4, "dstId": id5, "relation": "informed-by",   "date": "09/15/2025"})

# influencer + short-video content + partnerships
res = db.query("linkIdeas", {"srcId": id3, "dstId": id6, "relation": "supports",      "date": "09/16/2025"})
res = db.query("linkIdeas", {"srcId": id6, "dstId": id7, "relation": "complements",   "date": "09/17/2025"})

# growth loop: content -> referral -> pilot budget
res = db.query("linkIdeas", {"srcId": id6, "dstId": id8, "relation": "complements",   "date": "09/18/2025"})
res = db.query("linkIdeas", {"srcId": id8, "dstId": id9, "relation": "requires",      "date": "09/19/2025"})
res = db.query("linkIdeas", {"srcId": id5, "dstId": id9, "relation": "drives",        "date": "09/19/2025"})

# destination UX ties back to initial marketing push & content
res = db.query("linkIdeas", {"srcId": id10, "dstId": id6, "relation": "depends-on",   "date": "09/20/2025"})
res = db.query("linkIdeas", {"srcId": id1,  "dstId": id10,"relation": "leads-to",     "date": "09/20/2025"})

# optional: cross-link influencers and partnerships
res = db.query("linkIdeas", {"srcId": id7, "dstId": id3,  "relation": "aligns-with",  "date": "09/17/2025"})

# ---------- Extra Dense Links ----------
res = db.query("linkIdeas", {
    "srcId": id2, "dstId": id7,
    "relation": "amplifies", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id3, "dstId": id8,
    "relation": "enables", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id4, "dstId": id9,
    "relation": "validated-by", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id5, "dstId": id10,
    "relation": "measures", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id1, "dstId": id6,
    "relation": "inspires", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id2, "dstId": id9,
    "relation": "requires", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id3, "dstId": id10,
    "relation": "contributes-to", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id4, "dstId": id8,
    "relation": "aligns-with", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id7, "dstId": id9,
    "relation": "supports", "date": "09/20/2025"
})

res = db.query("linkIdeas", {
    "srcId": id6, "dstId": id5,
    "relation": "provides-data-for", "date": "09/20/2025"
})

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
    # net.show_buttons(filter_=['physics'])
    # net.set_options('var options = { interaction: {hover: true}, physics: {stabilization: true} }')

    html = net.generate_html()  # HTML string
    return html
