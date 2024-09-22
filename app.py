from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL") 
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

def execute_schema(path):
    with open(path, 'r') as schema:
        sql = schema.read()
    db.session.execute(text(sql))
    db.session.commit()

##@app.before_request
def base_for_db():
    execute_schema('schema.sql')


@app.route("/")
def index():
    return render_template("index.html") 


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    print(hash_value)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password)")
    db.session.execute(sql, {"username":username, "password":hash_value})
    db.session.commit()
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return redirect("/404")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            return redirect("/")
        else:
            return redirect("/404")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/subjects")
def subjects():
    subjects = db.session.execute(text("SELECT * FROM topics"))
    result = subjects.fetchall()
    print(result)
    return render_template("subjects.html", topics=result)

@app.route("/subjects/testi1")
def testi1():
    return render_template("testi1.html")

@app.route("/subjects/<int:topic_id>")
def forum(topic_id):
    result = db.session.execute(text("SELECT * FROM discussion where topic_id = :topic_id"), {"topic_id": topic_id})
    messages = result.fetchall()
    print(messages)

    topic = db.session.execute(text("SELECT * FROM topics WHERE id = :topic_id"), {"topic_id": topic_id}).fetchone()
    return render_template("Forum.html", messages=messages, topic=topic)


@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/newtopic", methods=["POST"])
def newtopic():
    topic = request.form["topic"]
    sql = text("INSERT INTO topics (name) VALUES (:topic)")
    db.session.execute(sql, {"topic":topic})
    db.session.commit()
    return redirect("/subjects")

@app.route("/send", methods=["POST"])
def send():
    topic_id = request.form["topic_id"]
    message = request.form["message"]
    sql = text("INSERT INTO discussion (message, sent_at, topic_id) VALUES (:message, CURRENT_TIMESTAMP, :topic_id)")
    db.session.execute(sql, {"message":message, "topic_id": topic_id})
    db.session.commit()
    return redirect(f"/subjects/{topic_id}")