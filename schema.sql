-- Includes the database layout for the website

-- Table for the users
CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB,
    developer INTEGER -- 0 = user 1 = developer
);

-- Table for the games
CREATE TABLE Games (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    uploaded_at TEXT,
    user_id INTEGER REFERENCES Users(id)
);

-- Table for the reviews
CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES Users(id),
    game_id INTEGER REFERENCES Games(id) ON DELETE CASCADE,
    score INTEGER
);