def build(raw_tree):
    """
    Convert raw resolver output into a structured trace object.
    """
    nodes = []
    edges = []

    def walk(node, parent_id=None):
        node_id = normalize_id(node)
        nodes.append({
            "id": node_id,
            "type": node["type"],
            "meta": node.get("meta", {})
        })

        if parent_id:
            edges.append({"from": parent_id, "to": node_id})

        for child in node.get("children", []):
            walk(child, node_id)

    walk(raw_tree)

    return {
        "root": normalize_id(raw_tree),
        "nodes": nodes,
        "edges": edges
    }


def normalize_id(node):
    """Convert node into a stable ID string."""
    return f"{node['type']}:{node['id']}"
