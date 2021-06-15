import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# for adding the hashing functions, password storage IO, etc
def add_password(row, enc):
    print(enc)
    f = Fernet(enc)
    #append line
    file = open("passwords.txt","a")
    file.write(f.encrypt(bytes(row[0] + "," + row[1] + "," + row[2], encoding='utf-8')).decode("utf-8")+"\n")

def return_leet(pswrd):
    pass
    # TODO

def writeToFile():
    fw = open("passwords.txt", "w")
    pass
    # TODO

def initPWFile(mpw):
    file = open("passwords.txt","w")
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(mpw))
    f = Fernet(key)
    token = f.encrypt(b"Open Sesame!")
    file.writelines([key.decode("utf-8") + "\n", token.decode("utf-8") + "\n"])

def check_mpw(mpw):
    file = open("passwords.txt","r").readlines()
    f = Fernet(file[0].encode('utf8', 'strict'))
    return f.decrypt(file[1].encode('utf8', 'strict')) == b'Open Sesame!'

def get_list(mpw):
    res = []
    file = open("passwords.txt","r").readlines()
    f = Fernet(file[0].encode('utf8', 'strict'))
    for cred in file[2:]:
        res.append(f.decrypt(cred.encode('utf8', 'strict')).decode('utf-8').split(","))
    return res

def get_key():
    file = open("passwords.txt","r").readlines()
    return file[0].encode('utf8', 'strict')
