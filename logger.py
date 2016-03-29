# -*- coding: utf-8 -*-
import sys

def log(msg, fd):
    if fd == 'err':
        sys.err(msg)
    elif fd == 'out':
        print(msg)
    else:
        raise TypeError('TypeError: fd is either not a string, or an unknown descriptor')