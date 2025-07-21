from encrypter import decrypt
import sys

def obscure(testo: str):
    sys.stdout.write("\033[F")  #Vai sopra
    sys.stdout.write("\r" + testo + " " * 60 + "\n") 
def doubleCheckPassword(prompts: list[str]):
    responses = []
    for prompt in prompts:
        response = input(prompt)
        responses.append(response)
        obscure(prompt)
    return responses
def getMasterPassword():
    print("To continue, you need to enter the Master Password. No checks will be performed on the Master Password.")
    prompts = ["Master Password: ", "Confirm Master Password: "]
    responses = doubleCheckPassword(prompts)
    password, confermaPassword = responses
    if password == confermaPassword:
        return password
    else:
        print("The given Master Passwords are not the same. Retry\n")
        getMasterPassword()
        return

masterPassword = getMasterPassword()

print("Make sure this executable is in the same folder as the BACKUP files")
with open(r"databasebackup.db", "rb") as f:
    dbContent = f.read()
with open(r"loginDatabasebackup.db", "rb") as f:
    loginDbContent = f.read()
with open(r"infobackup.db", "rb") as f:
    iv = f.read(16)
    salt = f.read(32)
    loginIv = f.read(16) #quanti bytes leggere, non il numero del byte
    loginSalt = f.read(32)
dbContent = decrypt(masterPassword, False, True, dbContent, iv, salt)
loginDbContent = decrypt(masterPassword, False, True, loginDbContent, loginIv, loginSalt)

with open("restoredDatabase.db", "wb") as f:
    f.write(dbContent)
with open("restoredLoginDatabase.db", "wb") as f:
    f.write(loginDbContent)