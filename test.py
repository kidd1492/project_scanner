import json

file_path = "D:/finished-projects/expert_in_a_box"
with open("data/html.json", "r", encoding="UTF-8") as file:
    data = json.load(file)
    for item in data:
        triggers = item.get("triggers")
        for trigger in triggers:
            if "chatOutline()" in trigger.get("content"):
                print(trigger)