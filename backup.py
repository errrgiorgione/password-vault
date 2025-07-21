import os
from shutil import copyfile, make_archive, rmtree

backupFolderPath = r"backup"

def setBackup(db: bytes, iv: bytes, salt: bytes, loginDb: bytes, loginIv: bytes, loginSalt: bytes):
    if not os.path.exists(backupFolderPath):
        os.makedirs(backupFolderPath)
    with open(f"{backupFolderPath}\databasebackup.db", "wb") as f:
        f.write(db)
    with open(f"{backupFolderPath}\loginDatabasebackup.db", "wb") as f:
        f.write(loginDb)
    with open(f"{backupFolderPath}\infobackup.db", "wb") as f:
        f.write(iv)
        f.write(salt)    
        f.write(loginIv)
        f.write(loginSalt)
    copyfile("readBackup.exe", r"backup\readBackup.exe")
    make_archive("backupZip", 'zip', "backup")
    rmtree("backup")

def backUp():
    with open(r"database\db.db", "rb") as original:
        passwordData = original.read()

    with open(r"database\logindb.db", "rb") as original:
        loginData = original.read()

    return passwordData, loginData