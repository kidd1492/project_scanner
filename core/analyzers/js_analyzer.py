import re
from pathlib import Path

# Detect function declarations
FUNCTION_PATTERN = re.compile(
    r"""
    # function foo() { ... }
    function\s+(\w+)\s*\(

    |

    # const foo = () => { ... }
    const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{

    |

    # let foo = function() { ... }
    (?:let|var)\s+(\w+)\s*=\s*function\s*\(

    |

    # async function foo() { ... }
    async\s+function\s+(\w+)\s*\(
    """,
    re.VERBOSE
)

# Detect fetch() anywhere
API_CALL_PATTERN = re.compile(r"fetch\s*\(")


class JSAnalyzer:
    def __init__(self):
        self.file_type = "js"
        self.results = []

    def analyze_files(self, file_list):
        self.results = []

        for file in file_list:
            file = file.replace("\\", "/")
            content = Path(file).read_text(encoding="utf-8", errors="ignore")

            for match in FUNCTION_PATTERN.finditer(content):
                func_name = next((g for g in match.groups() if g), None)

                # Extract function body
                func_body = self._extract_function_body(content, match.end())

                # Detect fetch() inside the function
                api_call = self._find_fetch(func_body)

                self.results.append({
                    "file": file,
                    "file_type": self.file_type,
                    "function": func_name,
                    "api_calls": api_call,
                    "source": file.split('/')[-1]
                })

        return self.results

    # ---------------------------------------------------------
    # Extract full function body using brace counting
    # ---------------------------------------------------------
    def _extract_function_body(self, content, start_index):
        brace_count = 0
        body = []
        started = False

        for i in range(start_index, len(content)):
            c = content[i]

            if c == "{":
                brace_count += 1
                started = True

            if started:
                body.append(c)

            if c == "}":
                brace_count -= 1
                if brace_count == 0 and started:
                    break

        return "".join(body)

    # ---------------------------------------------------------
    # Detect fetch() inside the function body
    # ---------------------------------------------------------
    def _find_fetch(self, func_body):
        for line in func_body.splitlines():
            if API_CALL_PATTERN.search(line):
                return line.strip()
        return ""
