#!/bin/python

import hashlib
import base64
import re

def hash_raw(input_str: str, _salt: int) -> bytes:
    # input_str = ip
    # salt = port
    "Возвращаю байты хеша"
    salt = hex(_salt)
    input_str = input_str.replace(' ', '').replace('.', '')
    mix_variable = salt.encode() + input_str.encode()
    hash_from_ip_port: str = hashlib.sha1(mix_variable).hexdigest()
    return base64.urlsafe_b64encode(hash_from_ip_port.encode('utf-8')[:32])

def hash_to_user_name(input_str: str, _salt: int) -> str:
    # input_str = f"{self.login}{self.password}"
    # salt = port
    salt = hex(_salt)
    _str = re.sub(r'[^a-zA-Zа-яА-Я]', '', input_str)
    mix_variable = salt.encode() + _str.encode()
    hash_from_ip_port: str = hashlib.sha1(mix_variable).hexdigest()
    return hash_from_ip_port[:10]