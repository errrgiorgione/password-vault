import sys, encrypter, manageDb, backup, manageLoginDb
from time import sleep
from base64 import b64decode
from hmac import compare_digest
from socket import gethostname, gethostbyname

def loginAccess(esito: int, endpoint: int, errore = 0):
    auth = f"{(name := gethostname())} - {gethostbyname(name)}"
    APIorIP = "I"
    codice = f"S,{APIorIP},{auth},{endpoint},{esito},{errore}"
    manageLoginDb.addLogin(codice)

def doubleCheckPassword(prompts: list[str]):
    responses = []
    for prompt in prompts:
        response = input(prompt)
        responses.append(response)
        obscure(prompt)
    return responses
def getMasterPassword(endpoint: int) -> str:
    print("To continue, you need to enter the Master Password. No checks will be performed on the Master Password.")
    prompts = ["Master Password: ", "Confirm Master Password: "]
    responses = doubleCheckPassword(prompts)
    password, confermaPassword = responses
    if password == confermaPassword:
        return password
    else:
        loginAccess(0, endpoint, 501)
        print("The given Master Passwords are not the same. Retry\n")
        getMasterPassword(endpoint)
        return

def timeOut(secs = 6):
    for x in range(secs, 0, -1):
        sys.stdout.write(f"\rThe password will stay visible for: {x} seconds   ")
        sleep(1)
    sys.stdout.write("\r" + " "*100)
    obscure("Time expired.")
def obscure(testo: str):
    sys.stdout.write("\033[F")  #Vai sopra
    sys.stdout.write("\r" + testo + " " * 150 + "\n") 
def creaPassword():
    print("ATTENTION: Once the password is given, it will not be visible in this screen anymore")

    masterPassword = getMasterPassword(2)
    print("\n")

    servizio = input("Which service is this password used for: ")
    prompts = ["Password: ", "Confirm password: "]
    responses = doubleCheckPassword(prompts)
    password, confermaPassword = responses
    if password != confermaPassword:
        loginAccess(0, 2, 500)
        print("[!] The given password are not the same\n")
        creaPassword()
        return
    
    password, salt, iv = encrypter.encrypt(bytes(password, "utf-8"), masterPassword, True)
    manageDb.writeOnDb(servizio, masterPassword, password, salt, iv)
    loginAccess(1, 2)

    print("Password saved successfully")

enumerateToIdDb = {}
def selezionaPassword(endpoint: int) -> int:
    id = input("Selected password: ")
    if not id.isnumeric():
        loginAccess(0, endpoint, 401)
        print("Make sure to enter a number")
        selezionaPassword(endpoint)
        return
    else:
        id = int(id)
        if id in enumerateToIdDb.keys():
            id = enumerateToIdDb[id]
            return id
        else:
            loginAccess(0, endpoint, 400)
            print("The chosen ID does not exist")
            selezionaPassword(endpoint)
            return
def mostraRecords():
    result = manageDb.getRows()
    nRows = len(result)
    if nRows:
        print("-"*100 + "\nSaved passwords: ")
        for i, row in enumerate(result,1):
            enumerateToIdDb[i] = row[0]
            print(f"\t{i}. {row[1]}") #row => ID,
        print("-"*100)
        return nRows
    else:
        print("No password available")
        return -1

def checkHMAC(dbPassword: bytes, masterPassword: str, salt: bytes, expectedHMAC: bytes) -> bool:
    actualHMAC = b64decode(manageDb.generateHMAC(dbPassword, masterPassword, salt))
    return compare_digest(actualHMAC, expectedHMAC)
def mostraPassword():
    masterPassword = getMasterPassword(1)
    print("It is not possible to show all passwords at once. Below is a list of stored passwords in this software, select the password you want to view\n")    
    nRows = mostraRecords()
    if nRows == -1: return
    id = selezionaPassword(1)
    passwordFromDb = manageDb.getRows(False, id)
    if not checkHMAC(b64decode(passwordFromDb[2]), masterPassword, b64decode(passwordFromDb[4]), b64decode(passwordFromDb[5])): 
        loginAccess(0, 1, 300)
        password = encrypter.randomPassword()
    else: 
        loginAccess(1, 1)
        password = encrypter.decrypt(masterPassword, True, False, passwordFromDb[2], passwordFromDb[3], passwordFromDb[4])
    print(f"{passwordFromDb[1]} 's password is: {password}")
    timeOut()

def deletePassword():
    print("ATTENTION: Deleting a password is not reversible")
    masterPassword = getMasterPassword(3) #solo un layer di sicurezza
    nRows = mostraRecords()
    if nRows == -1: return
    id = selezionaPassword(3)
    manageDb.deleteRow(id)
    print("Password deleted successfully")

def getBackup():
    masterpassword = getMasterPassword(4)
    dbContent, loginDbContent = backup.backUp()
    dbContent, iv, salt = encrypter.encrypt(dbContent, masterpassword, True)
    loginDbContent, loginIv, loginSalt = encrypter.encrypt(loginDbContent, masterpassword, True)
    backup.setBackup(dbContent, iv, salt, loginDbContent, loginIv, loginSalt)
    print("Backup created successfully")

def exit():
    return 1

opzioni = {
    1: mostraPassword,
    2: creaPassword,
    3: deletePassword,
    4: getBackup,
    5: exit
}

print("Password manager software")
stop = 0
while stop != 1:
    scelta = input('''
    OPTIONS
    1. Show password
    2. Add password
    3. Delete passwod
    4. Create a backup
    5. Exit

Chosen option: ''')

    if not scelta.isnumeric():
        print("Make sure to enter a number")
    else:
        scelta = int(scelta)
        if scelta <= 0 or scelta > 6:
            print("The chosen option does not exist")
        else:
            stop = opzioni[scelta]()