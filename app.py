from flask import Flask, request, render_template
from database import database

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def get_data():
    students = None
    marks = None
    subject = None
    error = None

    if request.method == "POST":
        dept = request.form.get("dept").upper()
        year = request.form.get("year")
        semester = request.form.get("semester")
        batch = request.form.get("batch").upper()
        subject = request.form.get("subject").strip().upper()

        result = database(dept, year, semester, batch, subject)

        if isinstance(result, str): 
            error = result
        else:
            students, marks = result
    return render_template("index.html", students = students, marks = marks, sub = subject, error = error)

if __name__ == "__main__":
    app.run(debug=True)