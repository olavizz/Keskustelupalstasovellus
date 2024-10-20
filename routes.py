from app import app
from flask import flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from os import getenv
import users
import discussion
import profiles
from werkzeug.security import check_password_hash, generate_password_hash
import secrets



@app.before_request
def base_for_db():
    discussion.execute_schema('schema.sql')
    if 'username' not in session and request.endpoint not in ['login', 'signup', 'index', 'new']:
        flash("Kirjaudu sisään käyttääksesi palvelua")
        return redirect("/")

@app.route("/")
def index():
    if session.get("username"):
        subject_result = discussion.get_subjects()
        print(subject_result)
        return render_template("index.html", topics=subject_result)
    else:
        return render_template("index.html") 

@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    password = request.form["password"]
    users.execute_signup(username, password)
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    user = users.check_login(username)

    if not user:
        flash("Väärä käyttäjätunnus tai salasana.")
        return redirect("/")
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user.id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("Väärä käyttäjätunnus tai salasana.")
            return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

#@app.route("/subjects")
#def subjects():
 #   subjects = db.session.execute(text("SELECT * FROM topics"))
  ## print(result)
    #return render_template("subjects.html", topics=result)

@app.route("/subjects/<int:topic_id>")
def forum(topic_id):
    messages, topic = discussion.get_discussion(topic_id)
    return render_template("forum.html", messages=messages, topic=topic)

@app.route("/like/<int:message_id>", methods=["POST"])
def likes(message_id):
    if session["csrf_token"] != request.form["csrf_token"]:
        return redirect(403)
    user_id = session.get("user_id")
    print(user_id)
    discussion.like(message_id, user_id)
    topic_id = request.form["topic_id"]
    return redirect(f"/subjects/{topic_id}")

##@app.route("/answer/<int:message_id>", methods=["POST"])
#def answer(message_id):
 #   comment = request.form["answer"]
  #  topic_id = request.form["topic_id"]
  #  user_id = session.get("user_id")
  #  sql = text("""INSERT INTO comments (comment, message_id, user_id) VALUES (:comment, :message_id, :user_id)""")
  #  db.session.execute(sql, {"comment":comment, "message_id":message_id, "user_id":user_id})
  #  db.session.commit()
  #  return redirect(f"/subjects/{topic_id}")



@app.route("/new")
def new():
    return render_template("new.html")

@app.route("/newtopic", methods=["POST"])
def newtopic():
    if session["csrf_token"] != request.form["csrf_token"]:
        return redirect(403)
    topic = request.form["topic"]
    discussion.add_topic(topic)
    return redirect("/subjects")

@app.route("/send", methods=["POST"])
def send():
    if session["csrf_token"] != request.form["csrf_token"]:
        return redirect(403)
    topic_id = request.form["topic_id"]
    message = request.form["message"]
    username = session["username"]
    discussion.send_message(topic_id, message, username)
    return redirect(f"/subjects/{topic_id}")

@app.route("/edit/<int:message_id>", methods=["POST"])
def edit_message(message_id):
    message = discussion.get_message_id(message_id)
    if session.get("user_id") != message.user_id:
        flash("Sinulla ei ole oikeutta muokata tätä viestiä.")
        return redirect("/")
    return render_template("edit_message.html", message=message)

@app.route("/update/<int:message_id>", methods=["POST"])
def update_message(message_id):
    if session.get("csrf_token") != request.form.get("csrf_token"):
        return redirect(403)
    
    message = discussion.get_message_id(message_id)
    print(message)

    if session.get("user_id") != message.user_id:
        return redirect("/")

    new_content = request.form["message"]
    discussion.update_message(message_id, new_content)    
    return redirect(f"/subjects/{message.topic_id}")

@app.route("/delete/<int:message_id>", methods=["POST"])
def delete(message_id):
    if session.get("csrf_token") != request.form.get("csrf_token"):
        return redirect(403)
    topic_id = request.form["topic_id"]
    message = discussion.get_message_id(message_id)

    if not message:
        flash("Viestiä ei löytynyt.")
        return redirect("/")

    if session.get("user_id") != message.user_id:
        return redirect("/")
    
    discussion.delete_message(message_id)
    return redirect(f"/subjects/{topic_id}")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Sinun täytyy olla kirjautuneena päästäksesi profiiliin.")
        return redirect("/")

    user_id = session["user_id"]
    profile_data = profiles.get_profile_id(user_id)
    return render_template("profile.html", profile=profile_data)