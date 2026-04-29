# Project Scanner:  
## Overview:  


This project is a modular, extensible static‑analysis and developer‑productivity platform 
designed to understand, document, and visualize the internal structure of any codebase.


By pointing the system at a project directory, it:

- automatically scans the filesystem,  
- analyzes each file based on its type,  
- generates a rich set of JSON reports describing the project’s architecture,  
    - routes,  
    - functions,  
    - classes,  
    - triggers,  
    - internal call relationships. 

At its core, the platform acts as a developer console for understanding complex projects 
Offering deep insights into how UI elements, JavaScript functions, backend routes, service 
classes, and core Python functions connect to one another. The system is built around a clean, 
domain‑driven architecture with dedicated layers for analysis, services, routing, and UI, making 
it easy to extend and evolve. 


The application includes a multi‑page dashboard that transforms raw analysis data into 
interactive visualizations, documentation templates, AI‑powered insights, and security 
evaluations. It is designed not just to scan code, but to help developers reason about 
architecture, trace execution flows, generate diagrams, improve documentation, and 
identify potential risks.
 
 ```
 project_scanner_refactor/
│
├── domain/
│   ├── __init__.py
│   │
│   └── analysis/
│       ├── analyzer_manager.py
│       ├── builder.py
│       ├── project_ir.py
│       ├── project_service.py
│       │
│       ├── analysis_objects/
│       │   ├── ir_class.py
│       │   ├── ir_event.py
│       │   ├── ir_function.py
│       │   ├── ir_js_function.py
│       │   ├── ir_method.py
│       │   ├── ir_route.py
│       │   └── __init__.py
│       │
│       ├── analyzers/
│       │   ├── base_analyzer.py
│       │   ├── html_analyzer.py
│       │   ├── js_analyzer.py
│       │   ├── python_analyzer.py
│       │   ├── python_extractors.py
│       │   └── __init__.py
│       │
│       └── file_object/
│           ├── ir_file.py
│           └── __init__.py
│
├── infrastructure/
│   ├── __init__.py
│   │
│   ├── cache_system/
│   │   ├── typed_ir_cache.py
│   │   └── __init__.py
│   │
│   └── file_system/
│       ├── file_handling.py
│       └── __init__.py
│
├── utilities/
│   ├── file_discovery.py
│   └── __init__.py
│
└── test.py
```