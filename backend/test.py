import helix

# Connect to a local helix instance
db = helix.Client(local=True, verbose=True, port=6969)

# Note that the query name is case sensitive
id1 = db.query('addIdea', {"text": "This is the first piece of data"})[0]['n']['id']
print(id1)
id2 = db.query('addIdea', {"text": "This is the second piece of data"})[0]['n']['id']
print(id2)
res = db.query("linkIdeas", {"srcId": id1, "dstId": id2, "relation": "they are related"})
print(res)