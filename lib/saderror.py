# -*- coding:utf-8 -*-

"""
Created on 25/05/2011

@author: diacus
"""

from xmlrpclib import Fault

class SADError:
    """
    This class contains definitions of error codes
    """
    FILENOTFOUND       = 100
    EMPTYSTREAM        = 101
    CLIENTDISCONNECTED = 102
    NOTIMPLEMENTED     = 103
    CORRUPTEDFILE      = 104
    CONNECTIONERROR    = 105

class FileNotFound(Fault):
    """
    An exception that is raised if the requested file is not found.
    @see: Fault
    """
    def __init__(self,message):
        Fault.__init__(self, SADError.FILENOTFOUND, message)
        
class EmptyStream(Fault):
    
    def __init__(self, message):
        Fault.__init__(self, SADError.EMPTYSTREAM, message)
        
class ClientDisconnected(Fault):
    def __init__(self, message):
        Fault.__init__(self, SADError.CLIENTDISCONNECTED, message)
               
class CorruptedFile(Fault):
    def __init__(self, message):
        Fault.__init__(self, SADError.CORRUPTEDFILE, message)
        
class ConnectionError(Fault):
    def __init__(self, message):
        Fault.__init__(self, SADError.CONNECTIONERROR, message)

