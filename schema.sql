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

-- Table for the classes
CREATE TABLE Classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

-- Table for linking classes to games
CREATE TABLE Game_classes (
    id INTEGER PRIMARY KEY,
    game_id INTEGER REFERENCES Games(id) ON DELETE CASCADE,
    title TEXT,
    value TEXT
);

-- Table for the game images
CREATE TABLE Images (
    id INTEGER PRIMARY KEY,
    game_id INTEGER REFERENCES Games(id) ON DELETE CASCADE,
    image BLOB
)

CREATE INDEX idx_game_reviews_id ON Reviews (game_id); -- Index for matching reviews to games
CREATE INDEX idx_user_game ON Games (user_id); -- Index for matching users to games