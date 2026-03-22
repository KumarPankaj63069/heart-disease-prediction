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
def get_db():
    return sqlite3.connect("database.db", timeout=10, check_same_thread=False)

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

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
        try:
            conn = get_db()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (request.form["name"], request.form["email"], request.form["password"])
            )

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
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (request.form["email"], request.form["password"])
        )
        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            session["email"] = user[2]
            return redirect("/dashboard")
        else:
            return "Invalid Email or Password"

    return render_template("login.html")

# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT age, result FROM history WHERE user_email=?",
            (session["email"],)
        )
        history = cur.fetchall()
        conn.close()

        return render_template("dashboard.html", user=session["user"], history=history)

    return redirect("/login")

# ================= HISTORY =================
@app.route("/history")
def history_page():
    if "user" in session:
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT age, result FROM history WHERE user_email=?",
            (session["email"],)
        )
        history = cur.fetchall()
        conn.close()

        return render_template("history.html", history=history, user=session["user"])

    return redirect("/login")

# ================= ABOUT =================
@app.route("/about")
def about():
    return render_template("about.html")

# ================= TEST PAGE =================
@app.route("/test")
def test():
    if "user" in session:
        return render_template("index.html")
    return redirect("/login")

@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    try:
        data = {}

        # form data collect
        for name in features_name:
            value = request.form.get(name)
            data[name] = float(value) if value else 0

        # 🔥 FIXED ORDER (MOST IMPORTANT)
        final = np.array([[
            data["age"],
            data["sex"],
            data["cp"],
            data["trestbps"],
            data["chol"],
            data["fbs"],
            data["thalach"],
            data["exang"]
        ]])

        # ML prediction
        prediction = model.predict(final)[0]

        if prediction == 0:
          result = "⚠️ High Risk of Heart Disease"
        else:
          result = "✅ No Heart Disease"

        # save history
        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO history (user_email, age, result) VALUES (?, ?, ?)",
            (session["email"], data.get("age", 0), result)
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