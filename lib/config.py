# -*- coding:utf-8 -*-
"""
Created on 02/06/2011

@author: diacus
"""

from ConfigParser import RawConfigParser
from db.pgdata    import PGDataBase as DataBase
from lib.common   import readmsu

class SADConfig(object):
    """
    classdocs
    """
    # Using the same state for all instances
    __state = {}

    def __init__(self):
        """
        Constructor
        """
        self.__dict__ = self.__state
    
    def setconfigfile(self, path):
        """
        Set the config file path
        @param path
        """
        self.__path = path

    def addoption(self, section, option, value):
        """
        add a config opiton
        @param section: Config section name
        @param opiton: Config option name
        @param value: Config option value
        """
        raise NotImplementedError
    
    def saveconfig(self):
        """
        Saves the current configuration values
        """
        raise NotImplementedError
    
    def loadconf(self):
        """
        Loads the configuration values from the given file path
        """
        if not self.__dict__.has_key( '__conf' ):
            self.__conf = RawConfigParser()
            self.__conf.read(self.__path)
            # Connecting to Database
            user           = self.__conf.get("DataBase", "user")
            passwd         = self.__conf.get("DataBase", "password")
            dbname         = self.__conf.get("DataBase", "dbname")
            
            self.__dbase   = DataBase(user, passwd, dbname)
            
            self.__address = self.__conf.get("General", "address")
            self.__port    = self.__conf.getint("General", "port")
            self.__storage = self.__conf.get("General", "storage")
            self.__msu     = readmsu(self.__conf.get("General", "msu"))
            
            self.__logfile = self.__conf.get("Log", "logfile")

            if self.__conf.has_section("IDA"):
                self.__idadis = self.__conf.get("IDA", "disperse")
                self.__idarec = self.__conf.get("IDA", "recover")

    def getdb(self):
        """
        @return : The system database instance.
        """
        return self.__dbase

    def getport(self):
        """
        @return The application port
        """
        return self.__port

    def getstoragepath(self):
        """
        @return The path where the data will be placed
        """
        return self.__storage

    def getmsu(self):
        """
        @return The maximum storage unit value
        """
        return self.__msu

    def getaddress(self):
        """
        @return The node ip addres or host name
        """
        return self.__address

    def getlogfile(self):
        """
        @return The log file path
        """
        return self.__logfile

    def getdispath(self):
        """docstring"""
        return self.__idadis

    def getrecpath(self):
        """docstring"""
        return self.__idarec



class SADClientConfig:

    """
    Client configuration class
    """

    __state = {}

    def __init__(self):
        """
        Class constructor
        """
        self.__dict__ = self.__state

    def setconfigfile(self, path):
        """
        Set the config file path
        @param path
        """
        self.__path = path

    def addoption(self, section, option, value):
        """
        add a config opiton
        @param section: Config section name
        @param opiton: Config option name
        @param value: Config option value
        """
        raise NotImplementedError

    def saveconfig(self):
        """
        Save the current configuration values
        """
        raise NotImplementedError
    
    def loadconf(self):
        """
        Loads the configuration values from the given file path
        """
        if not self.__dict__.has_key( '__conf' ):
            self.__conf = RawConfigParser()
            self.__conf.read(self.__path)
            
            self.__proxy     = self.__conf.get("General", "proxy")
            self.__downloads = self.__conf.get("General", "downloads")
            self.__maxtries  = self.__conf.getint("General","maxtries")	
            self.__logfile = self.__conf.get("Log", "logfile")

    def getdownloadspath(self):
        """
        @return The path where the files will be stored
        """
        return self.__downloads

    def getproxy(self):
        """
        @return The proxy's uri
        """
        return self.__proxy

    def getmaxtries(self):
        """
        @return How many times the user can type a worng passowrd
        """
        return self.__maxtries

    def getlogfile(self):
        """
        @return The log file path
        """
        return self.__logfile

