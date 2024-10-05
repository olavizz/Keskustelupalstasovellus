
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    created_at TIMESTAMP
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

CREATE TABLE IF NOT EXISTS comments (
    id SERIAL PRIMARY KEY,
    comment TEXT,
    message_id INT REFERENCES discussion(id),
    user_id INT REFERENCES users(id)
);

INSERT INTO topics (name) VALUES ('Koodaus')
ON CONFLICT (name) DO NOTHING;

INSERT INTO topics (name) VALUES ('Urheilu')
ON CONFLICT (name) DO NOTHING;

INSERT INTO topics (name) VALUES ('Politiikka')
ON CONFLICT (name) DO NOTHING;

INSERT INTO topics (name) VALUES ('Opiskelu')
ON CONFLICT (name) DO NOTHING;

