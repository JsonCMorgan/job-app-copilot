import datetime
import os
import re
from typing import Optional

from user_utils import get_user_paths
from email_utils import offer_email_output


def _parse_datetime(date_str: str, time_str: str) -> Optional[datetime.datetime]:
    """Validate YYYY-MM-DD and HH:MM, return combined datetime or None."""
    try:
        return datetime.datetime.strptime(
            date_str.strip() + " " + time_str.strip(), "%Y-%m-%d %H:%M"
        )
    except ValueError:
        return None


def _sanitize_company(s: str) -> str:
    """Safe filename from company name."""
    if not s or not s.strip():
        return "interview"
    safe = re.sub(r'[<>:"/\\|?*.\s]', '_', s.strip())
    safe = re.sub(r'_+', '_', safe).strip('_')
    return safe.lower() if safe else "interview"


def main():
    _, outputs_dir = get_user_paths()
    company_name = input("Company: ").strip() or "Company"
    while True:
        date_str = input("Date of Interview (YYYY-MM-DD): ")
        time_str = input("Time of Interview (HH:MM): ")
        start_dt = _parse_datetime(date_str, time_str)
        if start_dt is not None:
            break
        print("Invalid date or time. Use YYYY-MM-DD and HH:MM (e.g. 2025-03-25 14:30)")
    location = input("Location of Interview: ")
    contact_name = input("Contact Name: ")
    contact_email = input("Contact Email: ")
    contact_phone = input("Contact Phone: ")
    interview_type = input("Interview Type: ")
    end_dt = start_dt + datetime.timedelta(hours=1)
    dtstart_str = start_dt.strftime("%Y%m%dT%H%M%S")
    dtend_str = end_dt.strftime("%Y%m%dT%H%M%S")
    ics_string = f"""BEGIN:VCALENDAR
VERSION:2.0
BEGIN:VEVENT
DTSTART:{dtstart_str}
DTEND:{dtend_str}
SUMMARY:Interview at {company_name} ({interview_type})
LOCATION:{location}
DESCRIPTION:Contact: {contact_name}, Email: {contact_email}, Phone: {contact_phone}
END:VEVENT
END:VCALENDAR"""
    safe_company = _sanitize_company(company_name)
    output_path = os.path.join(outputs_dir, f"Interview_{safe_company}_{date_str}.ics")
    with open(output_path, "w") as f:
        f.write(ics_string)
    print(f"Saved to {output_path}")
    summary = f"""Interview at {company_name} ({interview_type})
Date: {date_str}
Time: {time_str}
Location: {location}
Contact: {contact_name} | {contact_email} | {contact_phone}

The .ics attachment can be opened to add this event to your calendar."""
    ics_filename = f"Interview_{safe_company}_{date_str}.ics"
    offer_email_output(summary, f"Interview - {company_name} ({date_str})", attachment_content=ics_string, attachment_filename=ics_filename)


if __name__ == "__main__":
    main()
