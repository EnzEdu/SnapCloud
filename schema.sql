CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    description TEXT,
    creation_date TEXT NOT NULL,
    profile_picture TEXT
);

CREATE TABLE IF NOT EXISTS audios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    filepath TEXT NOT NULL,
    description TEXT,
    genre TEXT,
    tags TEXT,
    user_id INTEGER NOT NULL,
    upload_date TEXT NOT NULL,
    mime_type TEXT NOT NULL,
    size INTEGER NOT NULL,
    length INTEGER NOT NULL,
    sampling_rate TEXT NOT NULL,
    bit_rate TEXT NOT NULL,
    num_channels INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
);