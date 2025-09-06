from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

from models import Base, College, Student, Event, Registration, Feedback

engine = create_engine("sqlite:///campus.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = SessionLocal()

# Colleges
c1 = College(name="Tech University")
c2 = College(name="Global Institute")
session.add_all([c1, c2])
session.commit()

# Students
s1 = Student(college_id=c1.id, roll_no="TU101", name="Alice", email="alice@example.com")
s2 = Student(college_id=c1.id, roll_no="TU102", name="Bob", email="bob@example.com")
s3 = Student(college_id=c2.id, roll_no="GI201", name="Charlie", email="charlie@example.com")
session.add_all([s1, s2, s3])
session.commit()

# Events
e1 = Event(college_id=c1.id, title="AI Workshop", event_type="Workshop",
           start_time=datetime.utcnow(), end_time=datetime.utcnow()+timedelta(hours=2),
           location="Hall A", description="Intro to AI")
e2 = Event(college_id=c2.id, title="Tech Fest", event_type="Fest",
           start_time=datetime.utcnow(), end_time=datetime.utcnow()+timedelta(hours=5),
           location="Auditorium", description="Annual Fest")
session.add_all([e1, e2])
session.commit()

# Registrations
r1 = Registration(student_id=s1.id, event_id=e1.id, attended=True, checkin_time=datetime.utcnow())
r2 = Registration(student_id=s2.id, event_id=e1.id, attended=False)
r3 = Registration(student_id=s3.id, event_id=e2.id, attended=True, checkin_time=datetime.utcnow())
session.add_all([r1, r2, r3])
session.commit()

# Feedback
f1 = Feedback(student_id=s1.id, event_id=e1.id, rating=5, comment="Great!")
f2 = Feedback(student_id=s3.id, event_id=e2.id, rating=4, comment="Good event")
session.add_all([f1, f2])
session.commit()

print("Seed complete")
