# core/ir_system/typed_ir_adapter.py
from typing import Dict, Any, List
from .typed_ir import ProjectIR, IRFile, Route


def route_from_dict(d: Dict[str, Any]) -> Route:
    return Route(
        name=d.get("name", ""),
        route=d.get("route", ""),
        args=d.get("args", []) or [],
        calls=d.get("calls", []) or [],
        returns=d.get("returns"),
        file=d.get("file", ""),
        source=d.get("source", ""),
        line=d.get("line", 0),
        symbol_id=d.get("symbol_id", ""),
    )


def file_from_dict(d: Dict[str, Any]) -> IRFile:
    routes: List[Route] = [route_from_dict(r) for r in d.get("routes", [])]

    return IRFile(
        path=d.get("path", ""),
        source=d.get("source", ""),
        type=d.get("type", ""),
        routes=routes,
    )


def project_ir_from_dict(raw: Dict[str, Any]) -> ProjectIR:
    files = [file_from_dict(f) for f in raw.get("files", [])]

    return ProjectIR(
        project_name=raw.get("project_name", ""),
        total_files=raw.get("total_files", 0),
        root=raw.get("root", ""),
        file_types=raw.get("file_types", []),
        files=files,
    )



'''TODO get here ->
@dataclass
class ProjectIR:
    files: list[FileIR]
    metadata: ProjectMetadata

    @staticmethod
    def from_dict(d: dict) -> "ProjectIR":
        return ProjectIR(
            files=[FileIR.from_dict(f) for f in d["files"]],
            metadata=ProjectMetadata.from_dict(d["metadata"])
        )

    def to_dict(self) -> dict:
        return {
            "files": [f.to_dict() for f in self.files],
            "metadata": self.metadata.to_dict()
        }
'''