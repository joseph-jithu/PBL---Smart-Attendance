from flask import Flask, render_template, request, redirect, session
import mysql.connector
import subprocess
import sys

app = Flask(__name__)
app.secret_key = "secretkey"


# ✅ Database Connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="pict12345",
        database="attendance_system"
    )


# 🔐 LOGIN PAGE
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "<h2>Invalid Credentials</h2>"

    return render_template("login.html")


# 📊 DASHBOARD
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM attendance ORDER BY timestamp DESC")
    records = cursor.fetchall()

    return render_template("dashboard.html", records=records)


# ▶️ START ATTENDANCE (NO PAGE RELOAD)
@app.route("/start", methods=["POST"])
def start():
    if "user" not in session:
        return redirect("/")

    subject = request.form["subject"]

    # 🔥 Run face recognition in background
    subprocess.Popen([
        sys.executable,
        "recognize.py",
        subject
    ])

    # ✅ No redirect → keeps loading message visible
    return "", 204


# 🚪 LOGOUT
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


# 🚀 RUN APP
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)