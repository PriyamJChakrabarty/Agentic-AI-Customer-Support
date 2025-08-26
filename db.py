from datetime import date, time
from sqlalchemy import (
    create_engine, Column, Integer, String, Text, Boolean,
    Date, Time, ForeignKey
)
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

DATABASE_URL = "sqlite:///admission.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()


class College(Base):
    __tablename__ = "colleges"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    short_name = Column(String(64), nullable=False, unique=True)
    address = Column(Text, nullable=True)
    helpline_phone = Column(String(32), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(255), nullable=True)

    contacts = relationship("Contact", back_populates="college", cascade="all, delete-orphan")
    reporting_sessions = relationship("ReportingSession", back_populates="college", cascade="all, delete-orphan")
    deadlines = relationship("Deadline", back_populates="college", cascade="all, delete-orphan")
    required_documents = relationship("RequiredDocument", back_populates="college", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<College {self.short_name}>"

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(128), nullable=False)          # e.g., "Admissions Office", "Faculty Advisor"
    name = Column(String(128), nullable=False)
    phone = Column(String(32), nullable=True)
    email = Column(String(255), nullable=True)
    office_location = Column(String(255), nullable=True)
    hours = Column(String(128), nullable=True)          # e.g., "Mon–Fri, 10am–5pm"

    college = relationship("College", back_populates="contacts")

    def __repr__(self):
        return f"<Contact {self.role}: {self.name}>"

class ReportingSession(Base):
    __tablename__ = "reporting_sessions"
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    building = Column(String(128), nullable=False)
    room = Column(String(64), nullable=True)
    notes = Column(Text, nullable=True)

    college = relationship("College", back_populates="reporting_sessions")

    def __repr__(self):
        return f"<ReportingSession {self.date} {self.building} {self.room or ''}>"

class Deadline(Base):
    __tablename__ = "deadlines"
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(64), nullable=False)           # e.g., fee_payment, hostel_allotment
    due_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=True)

    college = relationship("College", back_populates="deadlines")

    def __repr__(self):
        return f"<Deadline {self.type} {self.due_date}>"

class RequiredDocument(Base):
    __tablename__ = "required_documents"
    id = Column(Integer, primary_key=True)
    college_id = Column(Integer, ForeignKey("colleges.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(128), nullable=False)          # e.g., "Admission Letter"
    description = Column(Text, nullable=True)
    is_mandatory = Column(Boolean, nullable=False, default=True)
    applicable_category = Column(String(64), nullable=False, default="ALL")

    college = relationship("College", back_populates="required_documents")

    def __repr__(self):
        return f"<RequiredDocument {self.name} [{self.applicable_category}]>"

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized and tables created.")
