""" Password Manager App for CPSC 329 Spring 2021

functions for the app

Authors: Erin Paslawski, Ryan Pang, Mohit Bhatia, Jiarong Xu"""

# for adding the hashing functions, password storage IO, etc
import base64
import os
import re
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
    byte_buffer = list(map(lambda x : x + "\n", byte_buffer ))
    
    for cred in cred_buffer:
        byte_buffer.append(f.encrypt(bytes(cred[0] + "," + cred[1] + "," + cred[2], encoding='UTF-8')).decode("UTF-8") + "\n")
    print(byte_buffer)
    with open("passwords.txt", "w") as file:
        file.writelines(byte_buffer)

def save_password_file(cred_buffer, dir):
    global lock
    f = lock
    #Take first 2 lines from password file
    byte_buffer = open("passwords.txt","r").read().splitlines()[:2]
    byte_buffer = list(map(lambda x : x + "\n", byte_buffer ))
    
    for cred in cred_buffer:
        byte_buffer.append(f.encrypt(bytes(cred[0] + "," + cred[1] + "," + cred[2], encoding='UTF-8')).decode("UTF-8") + "\n")
    print(byte_buffer)
    with open(dir, "w") as file:
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


def check_strength(pswrd):
    if pswrd is None:
        return "Weak"
    pswrd_tally=0
    if len(pswrd) > 9:
        pswrd_tally = pswrd_tally + 1
    if re.search(r'\d', pswrd) is not None:
        pswrd_tally = pswrd_tally + 1
    if re.search(r'[A-Z]', pswrd) is not None:
        pswrd_tally = pswrd_tally + 1
    if re.search(r'[a-z]', pswrd) is not None:
        pswrd_tally = pswrd_tally + 1
    if re.search(r'\W', pswrd) is not None:
        pswrd_tally = pswrd_tally + 1
    print(pswrd)
    if pswrd_tally > 4:
        return "Strong"
    elif pswrd_tally > 2:
        return "Medium"
    else:
        return "Weak"


def return_leet(pswrd):
    rrtn_pswrd = ""
    if pswrd is None:
        return "Empty Password"
    else:
        for element in pswrd:
            if element == 'a':
                rrtn_pswrd = rrtn_pswrd + '@'
            elif element == 'I':
                rrtn_pswrd = rrtn_pswrd + '1'
            elif element == 'Z':
                rrtn_pswrd = rrtn_pswrd + '2'
            elif element == 'e':
                rrtn_pswrd = rrtn_pswrd + '3'
            elif element == 'A':
                rrtn_pswrd = rrtn_pswrd + '4'
            elif element == 's':
                rrtn_pswrd = rrtn_pswrd + '5'
            elif element == 'S':
                rrtn_pswrd = rrtn_pswrd + '$'
            elif element == 'O':
                rrtn_pswrd = rrtn_pswrd + '0'
            elif element == 'i':
                rrtn_pswrd = rrtn_pswrd + '!'
            elif element == 'H':
                rrtn_pswrd = rrtn_pswrd + '#'
            elif element == 'x':
                rrtn_pswrd = rrtn_pswrd + '*'
            elif element == 'G':
                rrtn_pswrd = rrtn_pswrd + '6'
            elif element == 'T':
                rrtn_pswrd = rrtn_pswrd + '7'
            elif element == 'B':
                rrtn_pswrd = rrtn_pswrd + '8'
            elif element == 'C':
                rrtn_pswrd = rrtn_pswrd + '('
            elif element == 'c':
                rrtn_pswrd = rrtn_pswrd + '<'
            else:
                rrtn_pswrd = rrtn_pswrd + element
        print(pswrd)
        return rrtn_pswrd

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
