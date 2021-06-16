""" Password Manager App for CPSC 329 Spring 2021

functions for the app

Authors: Erin Paslawski, Ryan Pang"""

# for adding the hashing functions, password storage IO, etc
import base64
import os
import re

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

l33t_dict = {
    'a': '@',
    'I': '1',
    'Z': '2',
    'e': '3',
    'A': '4',
    's': '5',
    'S': '$',
    'O': '0',
    'i': '!',
    '#': 'H',
    'x': '*',
    'G': '6',
    'T': '7',
    'B': '8',
    'C': '(',
    'c': '<'
}


# for adding the hashing functions, password storage IO, etc
def add_password(row, enc):
    print(enc)
    f = Fernet(enc)
    # append line
    file = open("passwords.txt", "a")
    file.write(f.encrypt(bytes(row[0] + "," + row[1] + "," + row[2], encoding='utf-8')).decode("utf-8") + "\n")


def return_leet(pswrd):
    if pswrd is None:
        return "Empty Password"
    else:
        pswrd.replace('a', '@')
        pswrd.replace('I', '1')
        pswrd.replace('Z', '2')
        pswrd.replace('e', '3')
        pswrd.replace('A', '4')
        pswrd.replace('s', '5')
        pswrd.replace('S', '$')
        pswrd.replace('O', '0')
        pswrd.replace('i', '!')
        pswrd.replace('#', 'H')
        pswrd.replace('x', '*')
        pswrd.replace('G', '6')
        pswrd.replace('T', '7')
        pswrd.replace('B', '8')
        pswrd.replace('C', '(')
        pswrd.replace('c', '<')
        return pswrd


def writeToFile():
    fw = open("passwords.txt", "w")
    pass
    # TODO


def initPWFile(mpw):
    file = open("passwords.txt", "w")
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
    file = open("passwords.txt", "r").readlines()
    f = Fernet(file[0].encode('utf8', 'strict'))
    return f.decrypt(file[1].encode('utf8', 'strict')) == b'Open Sesame!'


def get_list(mpw):
    res = []
    file = open("passwords.txt", "r").readlines()
    f = Fernet(file[0].encode('utf8', 'strict'))
    for cred in file[2:]:
        res.append(f.decrypt(cred.encode('utf8', 'strict')).decode('utf-8').split(","))
    return res


def get_key():
    file = open("passwords.txt", "r").readlines()
    return file[0].encode('utf8', 'strict')


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

    if pswrd_tally > 4:
        return "Strong"
    elif pswrd_tally > 2:
        return "Medium"
    else:
        return "Weak"
