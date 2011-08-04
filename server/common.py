# -*- coding:utf-8
"""
Created on 31/05/2011

@author: diacus
"""

from client.sadclient import NodeClient


class VirtualSpace:
    """
    classdocs
    """

    def __init__(self, vid, name, host, size, port = 4242):
        """
        Constructor
        @param vid
        @param name: String. The virtual space's name
        @param host: String. The virtual space's host name or ip address
        @param size: Integer. The virtual space's storage capacity
        @param port: Integer. The virtual space's listenig port
        """
        self.__id   = vid
        self.__name = name
        self.__host = host
        self.__size = size
        self.__port = port
        self.client = NodeClient( self.geturi() )
        
    def setname(self, name):
        """
        Updates the virtual space name
        @param name: The new virtual space name
        """
        self.__name = name
        
    def sethost(self, host):
        """
        Updates the vidtual space's host name or ip address
        @param host: The new host name or ip address
        """
        self.__host = host
        
    def setsize(self, size):
        """
        Updates the current virtual space cpacity
        @param size: The new virtual space capacity
        """
        self.__size = size
        
    def setport(self, port):
        """
        Updates the current virtual space's listening port
        @port: the new port
        """
        self.__port = port
    
    def getid(self):
        """
        @return the virtual space id
        """
        return self.__id
    
    def getname(self):
        """
        @return The virtual space name
        """
        return self.__name
    
    def gethost(self):
        """
        @return The virtual space's host name or ip address
        """
        return self.__host
    
    def getsize(self):
        """
        @return The virtual space's capacity
        """
        return self.__size
        
    def geturi(self):
        """
        @return: The virtual space's URI
        """
        return "%s:%d" % (self.__host, self.__port)
    
    def update(self, dbase):
        """
        Updates the virtual space's data into the given data base
        @param dbase: Data base controller instance
        """
        dbase.updateVirtualSpace(
            self.__id,
            self.__name,
            self.__host,
            self.__size
        )

    __str__ = geturi

    def __del__(self):
        """
        Virtual Space destructor
        """
        del self.client
    
