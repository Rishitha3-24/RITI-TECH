from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

# ✅ Create DB tables when the app starts (Flask 3.x compatible)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    logged_in = "email" in session
    return render_template("index.html", logged_in=logged_in, email=session.get("email"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # ✅ Use sha256 (correct name in Flask)
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session["email"] = user.email
            return redirect(url_for("index"))
        else:
            return "Invalid credentials. Try again."

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
