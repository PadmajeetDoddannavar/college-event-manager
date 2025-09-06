from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, College, Student, Event, Registration, Feedback
from schemas import (
    CollegeCreateSchema, StudentCreateSchema, EventCreateSchema,
    RegisterSchema, AttendanceSchema, FeedbackSchema
)

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Database
engine = create_engine("sqlite:///campus.db", echo=False)
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)


# ---------------- UI ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin_portal():
    return render_template("admin.html")


# ---------------- API ROUTES ----------------
@app.route("/colleges", methods=["POST"])
def add_college():
    data = request.json
    schema = CollegeCreateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    session = SessionLocal()
    college = College(**data)
    session.add(college)
    session.commit()
    return jsonify({"id": college.id, "name": college.name})


@app.route("/students", methods=["POST"])
def add_student():
    data = request.json
    schema = StudentCreateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    session = SessionLocal()
    student = Student(**data)
    session.add(student)
    session.commit()
    return jsonify({"id": student.id, "name": student.name})


@app.route("/events", methods=["POST"])
def add_event():
    data = request.json
    schema = EventCreateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    session = SessionLocal()
    event = Event(**data)
    session.add(event)
    session.commit()
    return jsonify({"id": event.id, "title": event.title})


@app.route("/events", methods=["GET"])
def list_events():
    session = SessionLocal()
    events = session.query(Event).all()
    return jsonify([
        {
            "id": e.id,
            "title": e.title,
            "event_type": e.event_type,
            "start_time": e.start_time.isoformat(),
            "end_time": e.end_time.isoformat(),
            "location": e.location,
            "college": e.college.name
        }
        for e in events
    ])


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    schema = RegisterSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    session = SessionLocal()
    reg = Registration(**data)
    session.add(reg)
    session.commit()
    return jsonify({"id": reg.id})


@app.route("/attendance", methods=["POST"])
def mark_attendance():
    data = request.json
    schema = AttendanceSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    session = SessionLocal()
    reg = session.query(Registration).filter_by(
        student_id=data["student_id"], event_id=data["event_id"]
    ).first()
    if not reg:
        return jsonify({"error": "Not registered"}), 404
    reg.attended = data["present"]
    reg.checkin_time = datetime.utcnow() if data["present"] else None
    session.commit()
    return jsonify({"message": "Attendance updated"})


@app.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.json
    schema = FeedbackSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify(errors), 400
    session = SessionLocal()
    fb = Feedback(**data)
    session.add(fb)
    session.commit()
    return jsonify({"id": fb.id, "rating": fb.rating})


# ---------------- REPORT ROUTES ----------------
@app.route("/reports/event-popularity")
def report_event_popularity():
    session = SessionLocal()
    q = (
        session.query(Event.title, func.count(Registration.id).label("registrations"))
        .join(Registration, Registration.event_id == Event.id, isouter=True)
        .group_by(Event.id)
    )
    return jsonify([{ "event": row.title, "registrations": row.registrations } for row in q])


@app.route("/reports/student-participation")
def report_student_participation():
    session = SessionLocal()
    q = (
        session.query(Student.name, func.count(Registration.id).label("events"))
        .join(Registration, Registration.student_id == Student.id, isouter=True)
        .group_by(Student.id)
    )
    return jsonify([{ "student": row.name, "events": row.events } for row in q])


@app.route("/reports/average-feedback")
def report_avg_feedback():
    event_id = request.args.get("event_id", type=int)
    session = SessionLocal()
    q = session.query(func.avg(Feedback.rating)).filter(Feedback.event_id == event_id).scalar()
    return jsonify({"event_id": event_id, "avg_rating": round(q, 2) if q else None})


@app.route("/reports/top-active")
def report_top_active():
    limit = request.args.get("limit", 3, type=int)
    session = SessionLocal()
    q = (
        session.query(Student.name, func.count(Registration.id).label("cnt"))
        .join(Registration, Registration.student_id == Student.id)
        .group_by(Student.id)
        .order_by(func.count(Registration.id).desc())
        .limit(limit)
    )
    return jsonify([{ "student": row.name, "registrations": row.cnt } for row in q])


if __name__ == "__main__":
    app.run(debug=True)
