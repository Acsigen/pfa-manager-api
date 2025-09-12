CREATE TABLE IF NOT EXISTS clients (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    contact_person TEXT NOT NULL,
    country TEXT NOT NULL,
    phone_number TEXT,
    onrc_no TEXT NOT NULL,
    cui TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    UNIQUE(onrc_no,cui)
);