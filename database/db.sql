CREATE TABLE passwords (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    servizio TEXT,
    ciphertext TEXT,
    iv TEXT,
    salt TEXT,
    HMAC TExt
)