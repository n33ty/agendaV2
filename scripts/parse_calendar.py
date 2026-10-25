
#!/usr/bin/env python3
"""Convertit le calendrier UCLouvain en JSON."""
import json
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from icalendar import Calendar

BRUSSELS = ZoneInfo("Europe/Brussels")


def text_value(component, key):
    value = component.get(key)
    if value is None:
        return ""
    value = str(value)
    return (
        value.replace(r"\n", "\n")
        .replace(r"\N", "\n")
        .replace(r"\,", ",")
        .replace(r"\;", ";")
        .replace(r"\\", "\\")
        .strip()
    )


def local_datetime(prop):
    if prop is None:
        return None
    value = prop.dt
    if isinstance(value, date) and not isinstance(value, datetime):
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=BRUSSELS)
    return value.astimezone(BRUSSELS)


def parse_description(description):
    lines = [line.strip() for line in description.splitlines() if line.strip()]
    code = lines[0] if lines else ""
    teacher = ""
    for line in reversed(lines[1:]):
        if not any(marker in line.lower() for marker in ("h -", "h–", "h –", " - ")) and not line.lower().startswith("http"):
            teacher = line
            break
    return code, teacher


def main():
    if len(sys.argv) != 3:
        raise SystemExit("Usage: parse_calendar.py INPUT.ics OUTPUT.json")

    source, destination = map(Path, sys.argv[1:])
    raw = source.read_bytes()

    if b"BEGIN:VCALENDAR" not in raw or b"END:VCALENDAR" not in raw:
        raise SystemExit("Le fichier téléchargé n'est pas un calendrier valide.")

    calendar = Calendar.from_ical(raw)
    events = []
    seen = set()

    for component in calendar.walk("VEVENT"):
        if str(component.get("STATUS", "")).upper() == "CANCELLED":
            continue

        start = local_datetime(component.get("DTSTART"))
        end = local_datetime(component.get("DTEND"))

        if not start or not end or end <= start:
            continue

        uid = text_value(component, "UID")
        if not uid:
            uid = f"{start.isoformat()}|{text_value(component, 'SUMMARY')}|{text_value(component, 'LOCATION')}"

        if uid in seen:
            continue
        seen.add(uid)

        description = text_value(component, "DESCRIPTION")
        code, teacher = parse_description(description)

        events.append({
            "uid": uid,
            "title": text_value(component, "SUMMARY") or "Cours UCLouvain",
            "date": start.date().isoformat(),
            "start": start.strftime("%H:%M"),
            "end": end.strftime("%H:%M"),
            "startDateTime": start.isoformat(),
            "endDateTime": end.isoformat(),
            "location": text_value(component, "LOCATION"),
            "courseCode": code,
            "teacher": teacher,
        })

    events.sort(key=lambda event: (event["date"], event["start"], event["title"]))

    if not events:
        raise SystemExit("Aucun cours valide trouvé : le JSON ne sera pas remplacé.")

    output = {"timezone": "Europe/Brussels", "events": events}
    destination.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(output, ensure_ascii=False, indent=2) + "\n"

    if destination.exists() and destination.read_text(encoding="utf-8") == serialized:
        print(f"Aucun changement : {len(events)} cours déjà à jour.")
    else:
        destination.write_text(serialized, encoding="utf-8")
        print(f"JSON généré : {len(events)} cours.")


if __name__ == "__main__":
    main()
