#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : HuYuan
# @File    : tools.py

from django import forms
from webssh import models
import time
import random
import hashlib
import os
from boamp.settings import BASE_DIR


class ValidationData(forms.ModelForm):
    class Meta:
        model = models.HostTmp
        exclude = ['datetime']


def unique():
    ctime = str(time.time())
    salt = str(random.random())
    m = hashlib.md5(bytes(salt, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


def get_key_obj(pkeyobj, pkey_file=None, pkey_obj=None, password=None):
    if pkey_file:
        with open(pkey_file) as fo:
            try:
                pkey = pkeyobj.from_private_key(fo, password=password)
                return pkey
            except:
                pass
    else:
        try:
            filename = os.path.join(BASE_DIR,"webssh/tools/key/Identity_temp")
            with open(filename,'w') as f:
                f.write(pkey_obj.getvalue())
            pkey = pkeyobj.from_private_key_file(filename=filename, password=password)
            #pkey = pkeyobj.from_private_key(pkey_obj, password=password)
            #print("aaaaaaaaaaaaaaa",pkey)
            os.remove(filename)
            return pkey
        except:
            pkey_obj.seek(0)
