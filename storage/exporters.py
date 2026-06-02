import csv
import io
import json

def schedule_to_json(schedule):
    return json.dumps(schedule, indent = 4)

def schedule_to_csv(schedule):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Month",
        "Book",
        "Minutes",
        "Partial"
    ])

    for month in schedule:
        for entry in month["entries"]:
            writer.writerow([
                month["month"],
                entry["title"],
                entry["minutes"],
                entry["partial"]
            ])
    return output.getvalue()

def schedule_to_markdown(schedule):
    lines = ["# Audiobook Schedule", ""]
    for month in schedule:
        lines.append(f"## Month {month['month']}")
        lines.append("")
        for entry in month["entries"]:
            lines.append(
                f"- {entry['title']} "
                f"({entry['minutes']} min)"
            )
        lines.append("")
    return "\n".join(lines)