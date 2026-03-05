PRAGMA foreign_keys = ON;

CREATE TABLE stats (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    streak INTEGER NOT NULL DEFAULT 0,
    total_sessions INTEGER NOT NULL DEFAULT 0,
    last_completed_date TEXT
);

CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    completed_at TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL
);

CREATE TABLE plants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plant_name TEXT NOT NULL,
    sessions_required INTEGER NOT NULL,
    sessions_completed INTEGER NOT NULL DEFAULT 0,
    completed boolean NOT NULL DEFAULT 0
);