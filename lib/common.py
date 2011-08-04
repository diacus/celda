# -*- coding:utf-8 -*-
"""
Created on 11/05/2011

@author: diacus
"""

import re

from lib.saderror import SADError
from data.message import Message
from random       import choice

class MessagesENG:
    """
    List of messages for the standard output and log files
    """

    def __init__(self):
        """
        Empty constructor
        """
        pass

    CantConnectDB     = "Data Base connection refused, check if your " +\
        "service is online."
    Connecting        = "Connecting to the proxy: %s ..."
    ConnectionRefused = "Connection refused."
    CreateTable       = "Creating Table: %s."
    CreateUser        = "Creating user: %s."
    DataRecived       = "Data recived:\n%s"
    Dispersed         = "%s fragment dispersed"
    Dispersing        = "Dispersing %s fragment"
    FaultRaise        = "Fault %d ocurred: %s."
    FileNotSaved      = "The file '%s' has not been saved."
    FileSaved         = "The file '%s' has been saved. Current version: %d."
    FileSplitUp       = "The file %s was split up in %d fragments."
    InvalidOption     = "Wrong option."
    ListingFiles      = "Listing %s's files."
    ListingServs      = "Listing %s's available services."
    MissingServer     = "You must type an URL."
    MissingUser       = "You must type an user name."
    MuchMistakes      = "You've made so much mistakes. Good bye."
    NoIDALinux64      = "There's no IDA module for Linux x86_64 architecture."
    NoIDAWin32        = "There's no IDA module for Windows 32 bits."
    NoServsAvailable  = "There's no storage services available. Sorry."
    Notimplemented    = "This function has not been implemented yet."
    ProcessingBlock   = "Processing block %s."
    ProcessingFrag    = "Processing fragment %s."
    RequestProcessed  = "Request processed: %s."
    RequestRecived    = "Request recived: %s."
    SelectedService   = "Selected service: %s."
    SelUsrID          = "Selecting user by id: %d"
    SelUsrMail        = "Selecting user by e-mail address: %s"
    SelUsrNick        = "Selecting user by name: %s"
    SendingFileTo     = "Sending file '%s' to %s virtual space (%s). current" +\
        " version: %d."
    SendingFragTo     = "Sending %s file's fragment number %d to %s virtual " +\
        "space (%s)."
    ServerError       = "Server error [%s]: %s"
    ServiceHalt       = "Service Halt."
    SmallFile         = "The file %s is smaller than MSU."
    StartingConnect   = "Starting connection protocol."
    TryAgain          = "Sorry, try again please."
    TryingConnection  = "Trying to connecto to the server: %s"
    TryingLogin       = "%s user is trying to login."
    UnknownError      = "Unknown Error."
    UnsupportedReq    = "Unsupported Request %d."
    UserConnected     = "The user %s has connected to the system."
    UserRefused       = "Connection refused for %s user."

def readmachinesfile(fname):
    """
    @param fname: Machines file name
    @return: A list with the machines road 
    """
    machines = []
    com      = re.compile("^[^#\\s]")
    fdata    = open(fname,"r")
    for line in filter(com.match, fdata.readlines()):
        name, host, port, size = line.split()
        machines.append((name, host, int(port), int(size)))
    fdata.close()
    return machines

def readusersfile(fname):
    """
    @param fname: Users file name 
    """
    users = []
    
    com   = re.compile("^[^#]")
    fdata = open(fname,"r")
    
    for line in filter(com.match, fdata.readlines()):
        a, b, c, d, e = line.split()
        users.append( ( a, b, c, d, int(e) ) )
    fdata.close()
        
    return users

def readmsu( msu = "1m" ):
    """
    @param msu: String that represents a storage measure 
    """
    measure = {'b': 1, 'k': 1024, 'm' : 1048576, 'g': 1073741824 }
    scale = measure[msu[-1].lower()]
    return int(msu[:-1]) * scale

def splitstream( stream = "", msu = 1048576 ):
    """
    Splits stream into tokens lesser than msu bytes
    @return the tokens list
    """
    tokens = list()
    while stream :
        tokens.append(stream[:msu])
        stream = stream[msu:]
    
    return tokens

def notimplementedfunction( mtype, message ):
    """
    Empty function for not implemented services
    @param mtype: Message's type
    @param message: Message's content
    """
    print "Message type:", mtype
    print "Message data:", str(message)
    return ( Message.FAILURE, SADError.NOTIMPLEMENTED )

class CycleQueue(list) :
    """
    A simple circular queue
    
    @see: list
    """
    
    def __init__(self, content = None):
        """
        Constructor class
        @param content: list class instance
        """
        if content == None:
            content = list()
        list.__init__(self, content)
        self.__size = len(self)
        self.__index = choice(range(self.__size)) if self.__size else 0
        
    def choice(self):
        """docstring for choice"""
        self.__index = choice( range(self.__size)) if self.__size else 0

    def nextval(self):
        """
        @return: The next value at the queue
        """
        val = self[self.__index]
        self.__index = (self.__index + 1) % len(self)
        return val
        
    def currentpos(self):
        """
        @return Current value of the CycleQueue instance
        """
        return self.__index

    def current(self):
        """
        @return The CycleQueue current item
        """
        return self[self.__index]
    
