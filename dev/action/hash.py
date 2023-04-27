#!/bin/python

import hashlib

# input_str = ip
# salt = port
def hash_raw(input_str: str, _salt: int):
    salt = hex(_salt)
    return str(hashlib.sha1(salt.encode() + input_str.replace(' ', '').replace('.', '').encode()).hexdigest())
