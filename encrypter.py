from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode
from secrets import choice
from random import shuffle
import string

def createSalt(n = 32) -> bytes:
    sale = get_random_bytes(n)
    return sale

def createKey(password: str, salt = None, extra = False) -> bytes | list[bytes]:
    """Password dev'essere string. Salt dev'essere bytes"""
    if not salt: salt = createSalt()
    chiave = PBKDF2(password, salt, dkLen=32, count=1000000)
    if not extra: return chiave
    else: return [chiave, salt]

def encrypt(message: bytes, masterPassword: str, extra = False) -> bytes | list[bytes]:
    """Key dev'essere bytes. Extra specifica se ritornare anche key e cipher.iv"""
    if not extra: key = createKey(masterPassword)
    else: key, salt = createKey(masterPassword, extra=True)
    cipher = AES.new(key, AES.MODE_CBC)
    data = cipher.encrypt(pad(message, AES.block_size))
    if not extra: return data
    else: return [data, cipher.iv, salt]

#b64, keepRawBytes sono usati per il readBackup, di base True
def decrypt(masterPassword: str, b64: bool, keepRawBytes: bool, *args) -> str: #ciphertext, iv, salt
    if b64: ciphertext, iv, salt = [b64decode(arg) for arg in args]
    else: ciphertext, iv, salt = [arg for arg in args]
    key = createKey(masterPassword, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    if keepRawBytes: password = unpad(cipher.decrypt(ciphertext), AES.block_size)
    else: password = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
    return password

def randomPassword(n = 10):
    upLetters = list(string.ascii_uppercase)
    lowLetters = list(string.ascii_lowercase)
    numbers = list(string.digits)
    special = list(string.punctuation)
    chars = upLetters + lowLetters + numbers + special

    password = [
        choice(upLetters),
        choice(lowLetters),
        choice(numbers),
        choice(special)
    ]
    password += ''.join(choice(chars) for _ in range(n-len(password)))
    shuffle(password) #muove gli elementi

    return ''.join(password)