CREATE TABLE loginAttempts (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    mezzo TEXT, -- indica se è stata usata l'"API" o il "SOFTWARE"
    APIKey TEXT,
    IP TEXT,
    orario TIMESTAMP,
    endpointService TEXT, -- specifica cosa ha fatto
    esito BOOLEAN, -- 1 = si, 0 = no
    errore TEXT, -- se esito = 0, specifica l'errore (usando dei codici) per motivare il rifiuto del login
    tentativiOggi INTEGER -- numero di accessi nella stessa giornati
)