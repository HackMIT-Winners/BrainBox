import numpy as np

def cosine_edge_weight(node_u: np.ndarray, node_v: np.ndarray) -> float:
    # normalize
    u = node_u / (np.linalg.norm(node_u) + 1e-12)
    v = node_v / (np.linalg.norm(node_v) + 1e-12)
    
    # cosine similarity in [-1,1]
    cos_sim = float(np.dot(u, v))
    
    # rescale to [0,1]
    weight = (cos_sim + 1.0) / 2.0
    return weight
