from flask import Flask, render_template, request, redirect, session
import numpy as np
import pickle
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# ================= LOAD MODEL =================
model = pickle.load(open("model.pkl", "rb"))
features_name = pickle.load(open("features.pkl", "rb"))

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # History table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT,
        age REAL,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= HOME =================
@app.route("/")
def home():
    return render_template("home.html")


# ================= REGISTER =================
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()

            cur.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                        (name, email, password))

            conn.commit()
            conn.close()

            return redirect("/login")

        except:
            return "User already exists!"

    return render_template("register.html")


# ================= LOGIN =================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = cur.fetchone()

        conn.close()

        if user:
            # 👉 IMPORTANT: email store karo (history ke liye)
            session["user"] = user[1]   # name
            session["email"] = user[2]  # email

            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" in session:

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        # 👉 history fetch
        cur.execute("SELECT age, result FROM history WHERE user_email=?", (session["email"],))
        history = cur.fetchall()

        conn.close()

        return render_template("dashboard.html", user=session["user"], history=history)

    return redirect("/login")
# ================= View All History =================
@app.route("/history")
def history_page():
    if "user" in session:

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT age, result FROM history WHERE user_email=?", (session["email"],))
        history = cur.fetchall()

        conn.close()

        return render_template("history.html", history=history, user=session["user"])

    return redirect("/login")
# ================= About  =================
@app.route("/about")
def about():
    return render_template("about.html")


# ================= TEST PAGE =================
@app.route("/test")
def test():
    if "user" in session:
        return render_template("index.html")
    return redirect("/login")


# ================= PREDICTION =================
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    try:
        data = {}

        for name in features_name:
            data[name] = float(request.form.get(name, 0))

        final = [list(data.values())]

        prediction = model.predict(final)

        if prediction[0] == 0:
            result = "⚠️ High Risk of Heart Disease"
        else:
            result = "✅ No Heart Disease"

        # 👉 SAVE HISTORY
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO history (user_email, age, result) VALUES (?, ?, ?)",
            (session["email"], data.get("age"), result)
        )

        conn.commit()
        conn.close()

        return render_template("result.html", prediction=result)

    except Exception as e:
        return f"Error: {str(e)}"


# ================= LOGOUT =================
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)