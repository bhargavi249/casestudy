from datetime import date
from uuid import uuid4

from flask import Flask, render_template, request

app = Flask(__name__)

LEAVE_TYPES = [
    "Casual Leave",
    "Sick Leave",
    "Earned Leave",
    "Personal Leave"
]

DEPARTMENTS = [
    "Engineering",
    "Human Resources",
    "Finance",
    "Marketing",
    "Operations",
    "Customer Support",
    "Other"
]


@app.get("/")
def home():
    return render_template(
        "register.html",
        leave_types=LEAVE_TYPES,
        departments=DEPARTMENTS,
        today=date.today().isoformat(),
        data={}
    )


@app.post("/submit")
def submit():
    fields = [
        "employee_name",
        "employee_id",
        "department",
        "leave_type",
        "start_date",
        "end_date",
        "reason"
    ]

    data = {
        field: request.form.get(field, "").strip()
        for field in fields
    }

    errors = []

    if len(data["employee_name"]) < 2:
        errors.append("Enter your full name.")

    if not data["employee_id"]:
        errors.append("Enter your employee ID.")

    if data["department"] not in DEPARTMENTS:
        errors.append("Choose a department.")

    if data["leave_type"] not in LEAVE_TYPES:
        errors.append("Choose a leave category.")

    if len(data["reason"]) < 10:
        errors.append(
            "Reason must contain at least 10 characters."
        )

    try:
        start = date.fromisoformat(data["start_date"])
        end = date.fromisoformat(data["end_date"])

        if start < date.today():
            errors.append("The start date cannot be in the past.")

        if end < start:
            errors.append(
                "The end date must be on or after the start date."
            )

        days = (end - start).days + 1

    except ValueError:
        errors.append("Enter valid start and end dates.")
        start = None
        end = None
        days = 0

    if errors:
        return render_template(
            "register.html",
            leave_types=LEAVE_TYPES,
            departments=DEPARTMENTS,
            today=date.today().isoformat(),
            data=data,
            errors=errors
        ), 400

    request_id = f"LR-{uuid4().hex[:8].upper()}"

    return render_template(
        "success.html",
        data=data,
        days=days,
        start=start.strftime("%d %b %Y"),
        end=end.strftime("%d %b %Y"),
        request_id=request_id
    )


if __name__ == "__main__":
    app.run(debug=True)