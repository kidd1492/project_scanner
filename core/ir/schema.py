# core/ir/schema.py

ProjectIR = {
    "project": {
        "name": str,
        "root": str,
        "file_types": [
            {
                "type": str,          # "py", "js", "html", ...
                "count": int,
            }
        ],
        "analysis_counts": {
            "html_triggers": int,
            "js_functions": int,
            "api_routes": int,
            "classes": int,
            "python_functions": int,
            # future: c_functions, php_routes, etc.
        },
    },

    "files": [
        {
            "path": str,
            "language": str,         # "python", "javascript", "html", ...
            "kind": str,             # "source", "template", "config", ...

            "functions": [
                {
                    "name": str,
                    "qualified_name": str,   # module.func or Class.method
                    "lineno": int | None,
                    "end_lineno": int | None,
                    "calls": list[str],      # list of call identifiers
                    "is_route_handler": bool,
                    "route": str | None,     # "/project/<path:term>"
                    "http_methods": list[str] | None,
                    "returns": str | None,   # unparsed or summarized
                }
            ],

            "classes": [
                {
                    "name": str,
                    "qualified_name": str,
                    "lineno": int | None,
                    "methods": list[str],    # references into functions[]
                }
            ],

            "routes": [
                {
                    "route": str,
                    "function": str,         # qualified_name
                    "file": str,
                    "http_methods": list[str] | None,
                }
            ],

            "triggers": [
                {
                    "type": str,            # "dom_event", "cli", "cron"
                    "event": str | None,    # "click", "submit"
                    "selector": str | None, # "#scanButton"
                    "handler": str,         # JS function name
                    "file": str,
                }
            ],

            "api_calls": [
                {
                    "raw": str,             # e.g. "fetch('/analysis/${PROJECT_NAME}/${type}')"
                    "normalized_path": str, # "/analysis/<project_name>/<analysis_type>"
                    "method": str | None,   # "GET", "POST"
                    "file": str,
                    "function": str,        # JS function name
                    "lineno": int | None,
                }
            ],
        }
    ]
}
