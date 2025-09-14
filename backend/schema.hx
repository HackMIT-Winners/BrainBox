// Define a node type
N::Idea {
  text: String 
}

// Define an edge type
E::Link {
    From: Idea,
    To: Idea,
    Properties: {
        Relation: String
    }
}

