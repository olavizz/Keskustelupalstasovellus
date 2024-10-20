from db import db
from sqlalchemy.sql import text

def get_profile_id(user_id):
    sql = text("SELECT * FROM profiles WHERE user_id = : user_id")
    profile = db.session.execute(sql, { "user_id": user_id })
    return profile

def update_profile(user_id):
    pass