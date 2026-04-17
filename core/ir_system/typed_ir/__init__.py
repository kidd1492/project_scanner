# Export ProjectIR (moved to its own file)
from .project_ir import ProjectIR

# Export the remaining IR classes (still in typed_ir.py for now)
from .typed_ir import (
    Route,
    IRClass,
    IRMethod,
    IRFunction,
    IRFile,
    IRJSFunction,
    IREvent,
)

