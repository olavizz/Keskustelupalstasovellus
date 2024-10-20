from db import db
from sqlalchemy.sql import text

def get_profile_id(user_id):
    sql = text("SELECT * FROM profiles WHERE user_id = :user_id")
    result = db.session.execute(sql, { "user_id": user_id })
    profile = result.fetchone()
    return profile

def update_profile(user_id, bio, hometown):
    sql = text("""
        UPDATE profiles 
        SET bio = :bio, hometown = :hometown
        WHERE user_id = :user_id
    """)
    db.session.execute(sql, {"bio": bio, "hometown": hometown, "user_id": user_id})
    db.session.commit()
    return