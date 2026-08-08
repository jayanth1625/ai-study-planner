from flask import Flask, render_template, request
from datetime import date, datetime, timedelta

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/planner")
def planner():
    return render_template("planner.html")


@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    exam_date_text = request.form.get("exam_date")
    study_hours = float(request.form.get("study_hours"))

    subject_names = request.form.getlist("subject")
    difficulties = request.form.getlist("difficulty")

    exam_date = datetime.strptime(
        exam_date_text, "%Y-%m-%d"
    ).date()

    today = date.today()

    days_remaining = (exam_date - today).days

    if days_remaining <= 0:
        return "Please select a future exam date."

    subjects = []

    for name, difficulty in zip(subject_names, difficulties):

        if difficulty == "Hard":
            weight = 3
        elif difficulty == "Medium":
            weight = 2
        else:
            weight = 1

        subjects.append({
            "name": name,
            "difficulty": difficulty,
            "weight": weight
        })

    total_weight = sum(
        subject["weight"] for subject in subjects
    )

    for subject in subjects:

        subject["daily_hours"] = round(
            (subject["weight"] / total_weight) * study_hours,
            2
        )

    schedule = []

    for day_number in range(1, days_remaining + 1):

        current_date = today + timedelta(days=day_number)

        day_subjects = []

        for subject in subjects:

            day_subjects.append({
                "name": subject["name"],
                "difficulty": subject["difficulty"],
                "hours": subject["daily_hours"]
            })

        schedule.append({
            "day": day_number,
            "date": current_date.strftime("%d %b %Y"),
            "subjects": day_subjects
        })

    return render_template(
        "plan.html",
        exam_date=exam_date.strftime("%d %b %Y"),
        study_hours=study_hours,
        subjects=subjects,
        schedule=schedule,
        days_remaining=days_remaining
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=80, debug=True)
