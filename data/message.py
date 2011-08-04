# -*- coding:utf-8 -*-

"""
File: message.py
Author: Diego Rodrigo Guzmán
"""

class Message:
    
    """
    Message codes
    """

    def __init__(self):
        pass

    ######################################################################
    # Request types
    ######################################################################

    # Messages for store files
    SAVESTREAM   = 1000
    SAVEFRAGMENT = 1001
    SAVEBLOCK    = 1002
    SAVECOPY     = 1003
    # Messages for recover files
    LOADSTREAM   = 1004
    LOADFRAGMENT = 1005	
    LOADBLOCK    = 1006

    ADDUSER      = 1010
    DISUSER      = 1011
    ADDGROUP     = 1012
    DELGROUP     = 1013
    ADDNODE      = 1014
    LISTFILES    = 1015
    LISTSERVS    = 1016

    CONNECT      = 1100
    DISCONNECT   = 1100

    ######################################################################
    # Response types
    ######################################################################

    SUCCESS       = 2000
    FAILURE       = 2001
    ACCESS_DENIED = 2002

class Packet:

    """
    Class Packet
    """

    def __init__(self):
        pass

    def serialize(self):
        """
        @return A copy of the instance's state as a dict
        """
        return dict(self.__dict__)

    def load(self, data):
        """
        Stores a new state
        @param data: dict. contains the new instance's state
        """
        self.__dict__ = dict(data)

