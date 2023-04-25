#!/bin/python

import hashlib

def hash_raw(input_str: str):
    salt = hex(199010)
    return hashlib.sha1(salt.encode() + input_str.replase(' ', '').encode()).hexdigest()

# new_pass = input('Введите пароль: ')
# hashed_password = hash_password(new_pass)
# print('Hash строка: ' + hashed_password)