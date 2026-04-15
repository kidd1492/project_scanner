def to_mermaid(trace, diagram_type="sequence"):
    if not trace:
        return ""
    if diagram_type == "sequence":
        return to_sequence(trace)
    return to_flow(trace)


def sanitize(s):
    """Make IDs safe for Mermaid syntax."""
    return (
        str(s)
        .replace(":", "_")
        .replace("/", "_")
        .replace(".", "_")
        .replace(" ", "_")
        .replace("(", "_")
        .replace(")", "_")
    )


def to_sequence(trace):
    """
    Convert trace edges into a Mermaid sequence diagram.
    """
    lines = ["sequenceDiagram"]

    edges = trace.get("edges", [])
    root = sanitize(trace.get("root", "root"))

    if not edges:
        lines.append(f"Note over {root}: single node")
        return "\n".join(lines)

    for edge in edges:
        src = sanitize(edge["from"])
        dst = sanitize(edge["to"])
        lines.append(f"{src} ->> {dst}: calls")

    return "\n".join(lines)


def to_flow(trace):
    """
    Convert trace edges into a Mermaid flowchart.
    """
    lines = ["flowchart TD"]

    edges = trace.get("edges", [])
    root = sanitize(trace.get("root", "root"))

    if not edges:
        lines.append(f"{root}((root))")
        return "\n".join(lines)

    for edge in edges:
        src = sanitize(edge["from"])
        dst = sanitize(edge["to"])
        lines.append(f"{src} --> {dst}")

    return "\n".join(lines)
