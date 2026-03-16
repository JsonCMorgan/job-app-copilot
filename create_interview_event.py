import datetime
import os
company_name = input("Company ")
date_str = input("Date of Interview (YYYY-MM-DD): ")
time_str = input("Time of Interview (HH:MM): ")
location = input("Location of Interview: ")
contact_name = input("Contact Name: ")
contact_email = input("Contact Email: ")
contact_phone = input("Contact Phone: ")
interview_type = input("Interview Type: ")
start_dt = datetime.datetime.strptime(date_str + " " + time_str, "%Y-%m-%d %H:%M")
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
safe_company = company_name.replace(" ", "_")
os.makedirs("outputs", exist_ok=True)
output_path = os.path.join("outputs", f"Interview_{safe_company}_{date_str}.ics")
with open(output_path, "w") as f:
    f.write(ics_string)
print(f"Saved to {output_path}")