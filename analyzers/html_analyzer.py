import re


def analyze_files(file_list):
    results = []

    TRIGGER_PATTERN = r'on(click|change|input|submit)\s*=\s*["\']([^"\']+)["\']'

    for file in file_list:
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

            # Extract UI triggers
            for match in re.findall(TRIGGER_PATTERN, content):
                event, func = match
                results.append({
                    "event": event,
                    "function": func,
                    "file": file,
                })

    return results