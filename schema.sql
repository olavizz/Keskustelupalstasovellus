
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    created_at TIMESTAMP
);
CREATE TABLE IF NOT EXISTS topics (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS discussion (
    id SERIAL PRIMARY KEY,
    message TEXT,
    sent_at TIMESTAMP,
    topic_id INT REFERENCES topics(id),
    user_id INT REFERENCES users(id)
);

INSERT INTO topics (name) VALUES ('Koodaus');
INSERT INTO topics (name) VALUES ('Urheilu');
INSERT INTO topics (name) VALUES ('Politiikka');
INSERT INTO topics (name) VALUES ('Opiskelu');

DROP TABLE IF EXISTS users, topics, discussion CASCADE;