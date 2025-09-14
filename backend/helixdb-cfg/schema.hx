// Define a node type
N::Idea {
  user: String,
  text: String,
  embed: [F32],
  date: String
}

// Define an edge type
E::Link {
    From: Idea,
    To: Idea,
    Properties: {
        relation: String,
        date: String
    }
}

