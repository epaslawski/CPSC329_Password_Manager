""" Password Manager App for CPSC 329 Spring 2021

functions for the app

Authors: Erin Paslawski, Ryan Pang, Mohit Bhatia"""

# for adding the hashing functions, password storage IO, etc
import base64
import os
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

lock :Fernet

def cred_buffer_to_file(cred_buffer):
    global lock
    f = lock
    #Take first 2 lines from password file
    byte_buffer = open("passwords.txt","r").read().splitlines()[:2]
    for cred in cred_buffer:
        byte_buffer.append(f.encrypt(bytes(cred[0] + "," + cred[1] + "," + cred[2], encoding='UTF-8')).decode("UTF-8") + "\n")
    with open("passwords.txt", "w") as file:
        file.writelines(byte_buffer)

# for adding the hashing functions, password storage IO, etc
def enc_to_file(index, row):
    # retrieve the locking mechanism
    global lock
    f = lock
    #append line
    bytephrase = f.encrypt(bytes(row[0] + "," + row[1] + "," + row[2], encoding='UTF-8')).decode("UTF-8")
    with open("passwords.txt", "a") as file:
        file.write(bytephrase + "\n")

def return_leet(pswrd):
    pass
    # TODO

def write_to_file():
    fw = open("passwords.txt", "w")
    pass
    # TODO

def init_pw_file(mpw):
    salt = base64.b64encode(os.urandom(16))
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(bytes(mpw, 'UTF-8')))
    f = Fernet(key)
    token = f.encrypt(b"Open Sesame!")
    with open("passwords.txt", "x") as file:
        file.write(salt.decode("UTF-8") + "\n")
        file.write(token.decode("UTF-8") + "\n")

def check_mpw(mpw):
    file = open("passwords.txt","r").read().splitlines()
    salt = file[0].encode(encoding='UTF-8')
    token = file[1].encode(encoding='UTF-8')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    global lock
    key = base64.urlsafe_b64encode(kdf.derive(bytes(mpw, 'UTF-8')))
    f = Fernet(key)
    lock = f # store the locking mechanism
    return f.decrypt(token) == b'Open Sesame!'

def get_list():
    # retrieve the locking mechanism
    global lock
    res = []

    #open the save file
    file = open("passwords.txt","r").read().splitlines()
    
    f = lock
    for cred in file[2:]:
        res.append(f.decrypt(cred.encode('utf8', 'strict')).decode('UTF-8').split(","))
    return res

