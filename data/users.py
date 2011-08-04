# -*- coding:utf-8 -*-
"""
Created on 31/05/2011

@author: diacus
"""

from data.message import Packet

class SADUser(Packet):
    """
    Represents a user, extends Packet class
    @see Packet
    """


    def __init__(self, uid, nick, passwd, fullname, email, createdon):
        """
        SADUser class constructor
        """
        Packet.__init__(self)
        self.__id = uid
        self.__nick = nick
        self.__passwd = passwd
        self.__fullname = fullname
        self.__email = email
        self.__since = createdon
        
        self.__servs = list()
        
    def setnick(self, nick):
        """
        Updates the user's name
        @param nick: String. The new user's name
        """
        self.__nick = nick
        
    def setpasswd(self, passwd):
        """
        Updates the user's password
        @param passwd: String. The new user's password
        """
        self.__passwd = passwd
        
    def setfullname(self, fullname):
        """
        Updates the user's full name
        @param fullname: String The new user's full name
        """
        self.__fullname = fullname
        
    def setemail(self, email):
        """
        Updates the user's e-mail address
        @param email: String. The new user's e-mail address
        """
        self.__email = email
        
    def getid(self):
        """
        @return Integer. The user's id
        """
        return self.__id
    
    def getnick(self):
        """
        @return String. The user's name
        """
        return self.__nick
    
    def getfullname(self):
        """
        @return String. The user's full name
        """
        return self.__fullname
    
    def getemail(self):
        """
        @return String. The user's e-mail address
        """
        return self.__email
    
    def getservices(self):
        """
        @return list. The available services
        """
        return self.__servs
    
    def getpasswd(self):
        """
        @return String. The user's password
        """
        return self.__passwd
    
    def update(self, dbase):
        """
        Updates the current user's state into the given data base
        @param dbase: PGDataBase instance
        @see db.pgdata
        """
        dbase.updateuser(self)

class SADFile(Packet):
    """
    SADFile Class: File descriptor class
    """
    
    def __init__(self, fid, name, size, version, since):
        """
        Something
        """
        Packet.__init__(self)
        self.__fid     = fid
        self.__name    = name
        self.__size    = size
        self.__version = version
        self.__since   = since  
        
    def __str__(self):
        """
        Something
        """
        return " * %7d  %7d  %s" % (self.__version, self.__size, self.__name)
    

