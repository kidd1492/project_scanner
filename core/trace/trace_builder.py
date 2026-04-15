def build(raw_tree):
    """
    Convert raw resolver output into a structured trace object.
    raw_tree is:
    { "id": "...", "type": "...", "meta": {...}, "children": [ ... ] }
    """
    if not raw_tree:
        return {"root": None, "nodes": [], "edges": []}

    nodes = []
    edges = []

    def walk(node, parent_id=None):
        node_id = normalize_id(node)

        nodes.append({
            "id": node_id,
            "type": node.get("type") or "node",
            "meta": node.get("meta") or {},
        })

        if parent_id:
            edges.append({"from": parent_id, "to": node_id})

        for child in node.get("children") or []:
            walk(child, node_id)

    walk(raw_tree)

    return {
        "root": normalize_id(raw_tree),
        "nodes": nodes,
        "edges": edges,
    }


def normalize_id(node):
    """Convert node into a stable ID string."""
    node_type = node.get("type") or "node"
    node_id = node.get("id") or "unknown"

    # Clean up weird characters
    node_id = str(node_id).replace(" ", "_").replace("/", "_")

    return f"{node_type}:{node_id}"
