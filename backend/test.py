import helix
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Connect to a local helix instance
db = helix.Client(local=True, verbose=True, port=6969)

client = OpenAI(api_key=api_key)

def get_embedding(text, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding

embed1 = get_embedding("We need more marketing to promote our AI agents")
print("Embedding 1:", embed1)
e1 = []
# Note that the query name is case sensitive
id1 = db.query('addIdea', {"user": "jeff", 
                           "text": "We need more marketting to promote our AI agents",
                           "embed": e1,
                           "date": "09/14/2025"})[0]['n']['id']
print(id1)

e2 = []
id2 = db.query('addIdea', {"user": "lisa", 
                           "text": "Agreed, one idea is to create a social media campaign",
                           "embed": e2,
                           "date": "09/14/2025"})[0]['n']['id']
print(id2)

res = db.query("linkIdeas", {"srcId": id1, "dstId": id2, "relation": "they are related", "date": "09/14/2025"})
print(res)
