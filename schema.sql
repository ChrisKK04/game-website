-- Includes the database layout for the website

-- Table for the users
CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

-- Table for the games
CREATE TABLE Games (
    id INTEGER PRIMARY KEY,
    title TEXT,
    user_id INTEGER REFERENCES Users(id),
    description TEXT,
    uploaded_at TEXT
);

-- Table for the reviews
CREATE TABLE Reviews (
    id INTEGER PRIMARY KEY,
    content TEXT,
    score INTEGER,
    sent_at TEXT,
    user_id INTEGER REFERENCES Users(id),
    game_id INTEGER REFERENCES Games(id)
);