#!/bin/python

import hashlib

# input_str = ip
# salt = port
def hash_raw(input_str: str, _salt: int) -> bytes:
    "Возвращаю байты хеша"
    salt = hex(_salt)
    input_str = input_str.replace(' ', '').replace('.', '')
    mix_variable = salt.encode() + input_str.encode()
    hash_from_ip_port: str = hashlib.sha1(mix_variable).hexdigest()
    return hash_from_ip_port.encode('utf-8')[:32]
