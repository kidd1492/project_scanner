# trace/trace_builder.py

def normalize_id(node):
    node_type = node.get("type") or "node"
    node_id = node.get("id") or "unknown"
    node_id = str(node_id).replace(" ", "_").replace("/", "_")
    return f"{node_type}:{node_id}"


def build(raw_tree):
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


class TraceBuilder:
    """Thin OO wrapper around the existing build() function."""

    def build_trace(self, project_name: str, trigger: str, raw_tree=None):
        if raw_tree is None:
            return {
                "project": project_name,
                "trigger": trigger,
                "nodes": [],
                "edges": [],
            }

        return build(raw_tree)
