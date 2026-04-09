import re
from pathlib import Path

# Detect function declarations
FUNCTION_PATTERN = r"""
    (?:function\s+(\w+)\s*\() |
    (?:const\s+(\w+)\s*=\s*\([^)]*\)\s*=>) |
    (?:async\s+function\s+(\w+)\s*\()
"""

# Detect any line containing fetch(
API_CALL_PATTERN = r"fetch\s*\("


def extract_function_body(content, start_index):
    """Extract full function body using brace counting."""
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


def analyze_files(file_list):
    results = []

    for file in file_list:
        file = file.replace("\\", "/")

        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all functions in the file
        for match in re.finditer(FUNCTION_PATTERN, content, re.VERBOSE):
            func_name = next((m for m in match.groups() if m), None)

            # Extract full function body
            func_body = extract_function_body(content, match.end())

            # Default: no API call
            api_call = ""

            # Scan body line-by-line for fetch(
            for line in func_body.splitlines():
                if re.search(API_CALL_PATTERN, line):
                    api_call = line.strip()
                    break

            results.append({
                "file": file,
                "function": func_name,
                "api_calls": api_call
            })

    return results
