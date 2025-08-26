# test_query.py
from db import SessionLocal, College, Contact, ReportingSession, Deadline, RequiredDocument

def main():
    session = SessionLocal()

    college = session.query(College).filter(College.short_name == "IIITA").one_or_none()
    if not college:
        print("❌ IIITA not found. Run `python seed_data.py` first.")
        return

    print("\n===== COLLEGE =====")
    print(f"Name: {college.name}")
    print(f"Short: {college.short_name}")
    print(f"Address: {college.address}")
    print(f"Helpline: {college.helpline_phone}")
    print(f"Email: {college.email}")
    print(f"Website: {college.website}")

    print("\n===== CONTACTS =====")
    for c in college.contacts:
        print(f"- {c.role}: {c.name} | {c.phone} | {c.email} | {c.office_location} | {c.hours}")

    print("\n===== REPORTING SESSIONS =====")
    for s in college.reporting_sessions:
        st = s.start_time.strftime('%H:%M') if s.start_time else "-"
        et = s.end_time.strftime('%H:%M') if s.end_time else "-"
        print(f"- {s.date} | {st}-{et} | {s.building} {s.room or ''} | {s.notes or ''}")

    print("\n===== DEADLINES =====")
    for d in college.deadlines:
        print(f"- {d.type}: {d.due_date} | {d.notes or ''}")

    print("\n===== REQUIRED DOCUMENTS =====")
    for doc in college.required_documents:
        flag = "Mandatory" if doc.is_mandatory else "Optional"
        print(f"- {doc.name} [{flag}; {doc.applicable_category}] | {doc.description or ''}")

    session.close()

if __name__ == "__main__":
    main()
