# -*- coding:utf-8 -*-

'''
Created on 02/06/2011

@author: diacus
'''

import hashlib

def byMD5(stream):
    return hashlib.md5(stream).hexdigest()


def getCheckSum(stream):
    """
    @return: The stream's check sum
    """
    getHash = {
        "md5" : byMD5
    }
    algorithm = "md5"
    return getHash[algorithm](stream)
