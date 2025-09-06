from marshmallow import Schema, fields, validate

class CollegeCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=2, max=200))

class StudentCreateSchema(Schema):
    college_id = fields.Int(required=True)
    roll_no = fields.Str(required=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)

class EventCreateSchema(Schema):
    college_id = fields.Int(required=True)
    title = fields.Str(required=True)
    event_type = fields.Str(required=True)
    start_time = fields.DateTime(required=True)
    end_time = fields.DateTime(required=True)
    location = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)

class RegisterSchema(Schema):
    student_id = fields.Int(required=True)
    event_id = fields.Int(required=True)

class AttendanceSchema(Schema):
    student_id = fields.Int(required=True)
    event_id = fields.Int(required=True)
    present = fields.Bool(required=True)

class FeedbackSchema(Schema):
    student_id = fields.Int(required=True)
    event_id = fields.Int(required=True)
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    comment = fields.Str(required=False, allow_none=True)
