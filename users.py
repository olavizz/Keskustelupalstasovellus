from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def execute_signup(username, password):
    hash_value = generate_password_hash(password)
    sql = text("INSERT INTO users (username, password) VALUES (:username, :password) RETURNING id")
    result = db.session.execute(sql, {"username":username, "password":hash_value})
    user_id = result.fetchone()[0]

    user_sql = text("INSERT INTO profiles (user_id, username) VALUES (:user_id, :username)")
    db.session.execute(user_sql, {"user_id": user_id, "username": username})
    db.session.commit()
    return

def check_login(username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    return user