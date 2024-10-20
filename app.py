from flask import Flask
from flask import flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL") 
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)
csrf = CSRFProtect(app)

def execute_schema(path):
    with open(path, 'r') as schema:
        sql = schema.read()
    db.session.execute(text(sql))
    db.session.commit()



@app.before_request
def base_for_db():
    execute_schema('schema.sql')
    if 'username' not in session and request.endpoint not in ['login', 'signup', 'index', 'new']:
        flash("Kirjaudu sisään käyttääksesi palvelua")
        return redirect("/")


@app.route("/")
def index():
    if session.get("username"):
        subjects = db.session.execute(text("SELECT * FROM topics"))

        subject_result = subjects.fetchall()
        print(subject_result)
        return render_template("index.html", topics=subject_result)
    else:
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
        flash("Väärä käyttäjätunnus tai salasana.")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            return redirect("/")
        else:
            flash("Väärä käyttäjätunnus tai salasana.")
            return redirect("/")


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
    result = db.session.execute(text("""
        SELECT d.id as message_id, d.message, d.sent_at, u.username, COUNT(l.id) as like_count
        FROM discussion d
        JOIN users u ON d.user_id = u.id
        LEFT JOIN likes l ON d.id = l.message_id AND l.like_ = 1
        WHERE d.topic_id = :topic_id
        GROUP BY d.id, u.username
        ORDER BY d.sent_at DESC
    """), {"topic_id": topic_id})

    messages = result.fetchall()
    print(messages)

    topic = db.session.execute(text("SELECT * FROM topics WHERE id = :topic_id"), {"topic_id": topic_id}).fetchone()
    return render_template("forum.html", messages=messages, topic=topic)

@app.route("/like/<int:message_id>", methods=["POST"])
def likes(message_id):
    user_id = session.get("user_id")
    print(user_id)
    topic_id = request.form["topic_id"]
    db.session.execute(text("""
        INSERT INTO likes (user_id, message_id, like_)
        VALUES (:user_id, :message_id, 1) 
        ON CONFLICT (user_id, message_id) DO UPDATE SET like_ = 1;
    """), {"user_id": user_id, "message_id": message_id})
    db.session.commit()
    return redirect(f"/subjects/{topic_id}")

@app.route("/answer/<int:message_id>", methods=["POST"])
def answer(message_id):
    comment = request.form["answer"]
    topic_id = request.form["topic_id"]
    user_id = session.get("user_id")
    sql = text("""INSERT INTO comments (comment, message_id, user_id) VALUES (:comment, :message_id, :user_id)""")
    db.session.execute(sql, {"comment":comment, "message_id":message_id, "user_id":user_id})
    db.session.commit()
    return redirect(f"/subjects/{topic_id}")



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
    username = session["username"]
    sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    user_id = user.id
    sql = text("INSERT INTO discussion (message, sent_at, topic_id, user_id) VALUES (:message, CURRENT_TIMESTAMP, :topic_id, :user_id)")
    db.session.execute(sql, {"message":message, "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return redirect(f"/subjects/{topic_id}")