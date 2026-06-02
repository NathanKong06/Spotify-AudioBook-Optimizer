import csv
import io
import json

def schedule_to_json(schedule: list) -> str:
    """
    Serializes a schedule (list of months with entries) into a JSON string.
    Args:
        schedule (list): A list of dictionaries, each representing a month with its entries.
    Returns:
        str: A JSON-formatted string representing the schedule.
    """
    return json.dumps(schedule, indent = 4)

def schedule_to_csv(schedule: list) -> str:
    """
    Serializes a schedule (list of months with entries) into a CSV string.
    Args:
        schedule (list): A list of dictionaries, each representing a month with its entries.
    Returns:
        str: A CSV-formatted string representing the schedule.
    """
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

def schedule_to_markdown(schedule: list) -> str:
    """
    Serializes a schedule (list of months with entries) into a Markdown string.
    Args:
        schedule (list): A list of dictionaries, each representing a month with its entries.
    Returns:
        str: A Markdown-formatted string representing the schedule.
    """
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