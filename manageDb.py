import sqlite3, hmac
from base64 import b64encode
from hashlib import sha256
from encrypter import createKey

def generateHMAC(text: bytes, masterPassword: str, salt: bytes) -> str:
    key = createKey(masterPassword, salt)
    hmacTag = hmac.new(key, text, sha256).digest()
    return b64encode(hmacTag).decode()

def openDb() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    connection = sqlite3.connect("database\db.db", check_same_thread=False)
    cursor = connection.cursor()
    return [connection, cursor]
def closeDb(connection: sqlite3.Connection):
    connection.commit()
    connection.close()

def writeOnDb(servizio: str, masterPassword: str, *args):
    values = []
    HMACValue = generateHMAC(args[0], masterPassword, args[-1])
    for arg in args: #ciphertext (password), iv, salt
        arg = b64encode(arg).decode()
        values.append(arg)

    connection, cursor = openDb()
    query = "INSERT INTO passwords (servizio, ciphertext, iv, salt, HMAC) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(query, (servizio, values[0], values[1], values[2], HMACValue))
    closeDb(connection)

def getRows(namesOnly = True, id = 0) -> list:
    connection, cursor = openDb()
    if namesOnly:
        query = "SELECT ID, servizio FROM passwords"
        cursor.execute(query)
        result = cursor.fetchall()
    else:
        query = "SELECT * FROM passwords WHERE ID = ?"
        cursor.execute(query, (id, ))
        result = list(cursor.fetchone())
    
    closeDb(connection)
    return result

def deleteRow(id: int):
    connection, cursor = openDb()
    query = "DELETE FROM passwords WHERE ID = ?"
    cursor.execute(query, (id, ))
    closeDb(connection)
