import sqlite3
from datetime import datetime

def openDb() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect("database\logindb.db", check_same_thread=False)
    cursor = connection.cursor()
    return [connection, cursor]
def closeDb(connection: sqlite3.Connection):
    connection.commit()
    connection.close() 

def analyzeCodice(codice: str) -> list:
    opzioni = {
        1: "Show password",
        2: "Add password",
        3: "Delete password",
        4: "Create a backup"
        #5: "Mostra nomi di tutte le password"
    }
    
    codice = codice.split(",")
    info = [None] * 8
    for i, part in enumerate(codice, 0):
        if not i: info[0] = "API" if part == "A" else "Software"
        elif i == 1: #si rifà al "APIorIP" dove specifica se si è a disposizione di un'API or un'IP
            if part == "A": info[1] = codice[i+1]; info[2] = ""
            else: info[1] = ""; info[2] = codice[i+1] #codice[i+1] = auth (API o IP)
        elif i == 4: info[4] = opzioni[int(part)]
        elif i == 3 or i == 5 or i == 7: info[i] = part
        elif i == 6: info[6] = f"Err {part}" if part != "0" else ""
    
    return info

def addLogin(codice: str):
    #codice = f"A,{APIorIP},{auth},{endpoint},{esito},{errore}"
    connection, cursor = openDb()

    info = analyzeCodice(codice)
    query = "INSERT INTO loginAttempts (mezzo, APIKey, IP, orario, endpointService, esito, errore, tentativiOggi) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    connection.execute(query, (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7]))
    
    closeDb(connection)

def getLoginAttempts(APIOrIP: str):
    connection, cursor = openDb()
    todayStart = datetime.now().strftime("%Y-%m-%d") + " 00:00:00"
    cursor.execute("""
        SELECT COUNT(*) FROM loginAttempts
        WHERE 
            (APIKey = ? OR IP = ?) AND
            orario >= ?
    """, (APIOrIP, APIOrIP, todayStart))
    result = cursor.fetchone()
    closeDb(connection)
    return result[0] if result else 0
