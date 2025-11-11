from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pandas as pd
import pickle, json, os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # used for session login

# === Load CSV or pickle dataset ===
try:
    with open("untitled8.pkl", "rb") as f:
        data = pickle.load(f)
except Exception:
    data = pd.read_csv("Customers_data_info_2025.csv")

data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")

# === Load or create user store ===
USER_FILE = "users.json"
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump([], f)


def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


# === ROUTES ===

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        gmail = request.form["gmail"]
        phone = request.form["phone"]
        password = request.form["password"]

        users = load_users()
        if any(u["phone"] == phone for u in users):
            return "⚠️ User already exists! Try logging in."

        users.append({"gmail": gmail, "phone": phone, "password": password})
        save_users(users)
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        phone = request.form["phone"]
        password = request.form["password"]

        users = load_users()
        user = next((u for u in users if u["phone"] == phone and u["password"] == password), None)

        if user:
            session["phone"] = phone
            return redirect(url_for("dashboard"))
        else:
            return "❌ Invalid credentials. Try again."
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "phone" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.pop("phone", None)
    return redirect(url_for("login"))


# === FETCH DETAILS BASED ON PHONE ===

@app.route("/manage")
def manage():
    phone = session.get("phone")
    user_data = data[data["phone_number"].astype(str) == str(phone)]
    records = user_data[["cycle_brand_and_model", "gear/non_gear"]].drop_duplicates().to_dict(orient="records")
    return render_template("manage.html", records=records)


@app.route("/service")
def service():
    phone = session.get("phone")
    user_data = data[data["phone_number"].astype(str) == str(phone)]
    records = user_data[["parts", "replace", "service_date", "service_type", "store"]].to_dict(orient="records")
    return render_template("service.html", records=records)


@app.route("/purchase")
def purchase():
    phone = session.get("phone")
    user_data = data[data["phone_number"].astype(str) == str(phone)]
    records = user_data[["cycle_brand_and_model", "date_of_purchase", "gmail", "invoice_number", "name", "phone_number", "store"]].to_dict(orient="records")
    return render_template("purchase.html", records=records)


if __name__ == "__main__":
    app.run(debug=True)
