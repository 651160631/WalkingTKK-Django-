#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick

from cryptography.fernet import Fernet


class Prpcrypt():
    def __init__(self):
        self.key = b'wdix98DyJkAwtL2Au52Dl-IviK0Od1Ntpyaj00008888'

    def encrypt(self, text):
        f = Fernet(self.key)
        token = f.encrypt(bytes(text, encoding="utf-8"))
        token = str(token, encoding="utf-8")
        return token

    #解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        f = Fernet(self.key)
        token = f.decrypt(bytes(text, encoding="utf-8"))
        token = str(token, encoding="utf-8")
        return token
