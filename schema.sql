
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    created_at TIMESTAMP,
    UNIQUE(username)
);
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS discussion (
    id SERIAL PRIMARY KEY,
    message TEXT,
    sent_at TIMESTAMP,
    topic_id INT REFERENCES topics(id),
    user_id INT REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS likes (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    like_ INTEGER CHECK (like_ IN  (1, -1)), 
    message_id INT REFERENCES discussion(id),
    UNIQUE(user_id, message_id)

);

CREATE TABLE IF NOT EXISTS profiles (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    username TEXT,
    bio TEXT,
    signup_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    hometown TEXT
);


INSERT INTO topics (name) VALUES ('Koodaus')
ON CONFLICT (name) DO NOTHING;

INSERT INTO topics (name) VALUES ('Urheilu')
ON CONFLICT (name) DO NOTHING;

INSERT INTO topics (name) VALUES ('Politiikka')
ON CONFLICT (name) DO NOTHING;

INSERT INTO topics (name) VALUES ('Opiskelu')
ON CONFLICT (name) DO NOTHING;

--DROP TABLE IF EXISTS users, comments, discussion, likes, topics CASCADE;


