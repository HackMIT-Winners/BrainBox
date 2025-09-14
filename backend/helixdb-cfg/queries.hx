
// Insert a node (with text we’ll embed)
QUERY addIdea(user: String, text: String, embed: [F32], date: String) =>
  n <- AddN<Idea>({user: user, text: text, embed: embed, date: date})
  RETURN n

// Link two nodes
QUERY linkIdeas(srcId: ID, dstId: ID, relation: String, date: String) =>
  t1 <- N<Idea>(srcId)
  t2 <- N<Idea>(dstId)
  e <- AddE<Link>(
    {relation: relation,
    date: date}
  )::From(srcId)::To(dstId)
  RETURN e

QUERY getAllIdeas () =>
  // Select all continent nodes
  ideas <- N<Idea>
  RETURN ideas

QUERY getAllConnectedIdeas (parent_id: ID) =>
    // Select continent node with given ID
    idea <- N<Idea>(parent_id)

    // Select all countries linked to the continent
    ideas <- idea::Out<Link>
    RETURN ideas
