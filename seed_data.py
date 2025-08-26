
from datetime import date, time
from db import SessionLocal, init_db, College, Contact, ReportingSession, Deadline, RequiredDocument

def seed():
    init_db()
    session = SessionLocal()

    
    college = session.query(College).filter(College.short_name == "IIITA").one_or_none()
    if college:
        session.delete(college)
        session.commit()

    college = College(
        name="Indian Institute of Information Technology Allahabad",
        short_name="IIITA",
        address="Jhalwa, Allahabad, Uttar Pradesh 211015",
        helpline_phone="+91-532-292-2000",
        email="admissions@iiita.ac.in",
        website="https://www.iiita.ac.in"
    )
    session.add(college)
    session.flush()  # to get college.id

    # Contacts
    contacts = [
        Contact(
            college_id=college.id,
            role="Admissions Office",
            name="Admissions Helpdesk",
            phone="+91-532-292-2000",
            email="admissions@iiita.ac.in",
            office_location="Academic Block, Ground Floor",
            hours="Mon–Fri, 10:00–17:00"
        ),
        Contact(
            college_id=college.id,
            role="Hostel Warden",
            name="Hostel Office",
            phone="+91-532-292-2100",
            email="hostel@iiita.ac.in",
            office_location="Hostel Admin Office",
            hours="Mon–Sat, 10:00–17:00"
        ),
    ]
    session.add_all(contacts)

    # Reporting Sessions (physical reporting)
    sessions = [
        ReportingSession(
            college_id=college.id,
            date=date(2025, 8, 15),
            start_time=time(9, 0),
            end_time=time(12, 0),
            building="Academic Block",
            room="Room 101",
            notes="Bring original documents and 2 photocopies."
        ),
        ReportingSession(
            college_id=college.id,
            date=date(2025, 8, 16),
            start_time=time(9, 0),
            end_time=time(12, 0),
            building="Academic Block",
            room="Room 102",
            notes="Late reporting window."
        ),
    ]
    session.add_all(sessions)

    # Deadlines
    deadlines = [
        Deadline(
            college_id=college.id,
            type="fee_payment",
            due_date=date(2025, 8, 10),
            notes="Complete payment via the student portal."
        ),
        Deadline(
            college_id=college.id,
            type="hostel_allotment",
            due_date=date(2025, 8, 20),
            notes="Upload allocation preference by the due date."
        ),
        Deadline(
            college_id=college.id,
            type="document_verification",
            due_date=date(2025, 8, 15),
            notes="Verification during physical reporting."
        ),
    ]
    session.add_all(deadlines)

    # Required Documents
    docs = [
        RequiredDocument(
            college_id=college.id,
            name="Admission Letter",
            description="Official institute-issued admission letter.",
            is_mandatory=True,
            applicable_category="ALL"
        ),
        RequiredDocument(
            college_id=college.id,
            name="Class 10 Marksheet",
            description="Original + photocopies.",
            is_mandatory=True,
            applicable_category="ALL"
        ),
        RequiredDocument(
            college_id=college.id,
            name="Class 12 Marksheet",
            description="Original + photocopies.",
            is_mandatory=True,
            applicable_category="ALL"
        ),
        RequiredDocument(
            college_id=college.id,
            name="JEE Rank Card",
            description="Printout of final rank/provisional allotment.",
            is_mandatory=True,
            applicable_category="ALL"
        ),
        RequiredDocument(
            college_id=college.id,
            name="Passport-size Photos",
            description="4 recent photos.",
            is_mandatory=True,
            applicable_category="ALL"
        ),
        RequiredDocument(
            college_id=college.id,
            name="Category Certificate",
            description="Required if applicable (SC/ST/OBC/EWS).",
            is_mandatory=False,
            applicable_category="SC/ST/OBC/EWS"
        ),
    ]
    session.add_all(docs)

    session.commit()
    session.close()
    print("✅ Seeded IIITA dummy data.")

if __name__ == "__main__":
    seed()
