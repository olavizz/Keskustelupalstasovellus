from db import db
from sqlalchemy.sql import text

def execute_schema(path):
    with open(path, 'r') as schema:
        sql = schema.read()
    db.session.execute(text(sql))
    db.session.commit()

def get_subjects():
    subjects = db.session.execute(text("SELECT * FROM topics"))
    return subjects

def get_discussion(topic_id):
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

    return messages, topic

def like(message_id, user_id):
    db.session.execute(text("""
        INSERT INTO likes (user_id, message_id, like_)
        VALUES (:user_id, :message_id, 1) 
        ON CONFLICT (user_id, message_id) DO UPDATE SET like_ = 1;
    """), {"user_id": user_id, "message_id": message_id})
    db.session.commit()
    return

def add_topic(topic):
    sql = text("INSERT INTO topics (name) VALUES (:topic)")
    db.session.execute(sql, {"topic":topic})
    db.session.commit()
    return

def send_message(topic_id, message, username):
    sql = text("SELECT id FROM users WHERE username = :username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    user_id = user.id
    sql = text("INSERT INTO discussion (message, sent_at, topic_id, user_id) VALUES (:message, CURRENT_TIMESTAMP, :topic_id, :user_id)")
    db.session.execute(sql, {"message":message, "topic_id":topic_id, "user_id":user_id})
    db.session.commit()
    return

def get_message_id(message_id):
    sql = text("SELECT * FROM discussion WHERE id = :message_id")
    result = db.session.execute(sql, {"message_id": message_id}).fetchone()
    
    if result:
        return result
    return None

def update_message(message_id, new_content):
    sql = text("UPDATE discussion SET message = :new_content WHERE id = :message_id")
    db.session.execute(sql, {"new_content": new_content, "message_id": message_id})
    db.session.commit()
    return

def delete_message(message_id):
    delete_likes_sql = text("DELETE FROM likes WHERE message_id = :message_id")
    db.session.execute(delete_likes_sql, {"message_id": message_id})
    sql = text("DELETE FROM discussion WHERE id = :message_id")
    db.session.execute(sql, {"message_id": message_id})
    db.session.commit()
    return

