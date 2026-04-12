def to_mermaid(trace, diagram_type="sequence"):
    if not trace:
        return ""
    if diagram_type == "sequence":
        return to_sequence(trace)
    return to_flow(trace)


def to_sequence(trace):
    """
    Convert trace edges into a Mermaid sequence diagram.
    """
    lines = ["sequenceDiagram"]

    edges = trace.get("edges", [])
    root = trace.get("root", "root")

    if not edges:
        lines.append(f"Note over {root}: single node")
        return "\n".join(lines)

    for edge in edges:
        src = edge["from"]
        dst = edge["to"]
        lines.append(f"{src} ->> {dst}: calls")

    return "\n".join(lines)


def to_flow(trace):
    """
    Convert trace edges into a Mermaid flowchart.
    """
    lines = ["flowchart TD"]

    edges = trace.get("edges", [])
    root = trace.get("root", "root")

    if not edges:
        lines.append(f"{root}((root))")
        return "\n".join(lines)

    for edge in edges:
        src = edge["from"]
        dst = edge["to"]
        lines.append(f"{src} --> {dst}")

    return "\n".join(lines)
