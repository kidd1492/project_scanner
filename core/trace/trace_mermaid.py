def to_mermaid(trace, diagram_type="sequence"):
    if diagram_type == "sequence":
        return to_sequence(trace)
    return to_flow(trace)


def to_sequence(trace):
    """
    Convert trace edges into a Mermaid sequence diagram.
    """
    lines = ["sequenceDiagram"]

    for edge in trace["edges"]:
        src = edge["from"]
        dst = edge["to"]
        lines.append(f"    {src} ->> {dst}: calls")

    return "\n".join(lines)


def to_flow(trace):
    """
    Convert trace edges into a Mermaid flowchart.
    """
    lines = ["flowchart TD"]

    for edge in trace["edges"]:
        src = edge["from"]
        dst = edge["to"]
        lines.append(f"    {src} --> {dst}")

    return "\n".join(lines)
