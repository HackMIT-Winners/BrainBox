
// Insert a node (with text we’ll embed)
QUERY addIdea(text: String) =>
  n <- AddN<Idea>({text: text})
  RETURN n

// Link two nodes
QUERY linkIdeas(srcId: ID, dstId: ID, relation: String) =>
  t1 <- N<Idea>(srcId)
  t2 <- N<Idea>(dstId)
  e <- AddE<Link>(
    {Relation: relation}
  )::From(srcId)::To(dstId)
  RETURN e