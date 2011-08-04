# -*- coding:utf-8 -*-

"""
@author diacus
"""

from xmlrpclib    import Binary
from lib.saderror import EmptyStream
from lib.hash     import getCheckSum
from data.message import Packet

class Stream(Packet):
    """
    Generic class that represent a data stream.
    """

    def __init__(self, data = ''):
        """
        Class constructor
        @param data: Stream's content
        """
        Packet.__init__(self)
        self._data = Binary(data)
        self._checksum = getCheckSum(data)

    def savetofile(self, name):
        """
        Save the Stream's content to a file
        @param name: Target file's name
        """
        if self._data:
            fdata = open(name,'wb')
            fdata.write(self._data.data)
            fdata.close()
        else:
            raise EmptyStream

    def loadfromfile(self, name):
        """
        Load the Stream's content from a file
        @param name:
        """
        fdata = open(name,'rb')
        self._data = Binary(fdata.read())
        fdata.close()
        self._checksum = getCheckSum(self._data.data)

    def getdata(self):
        """
        @return The stream's data
        """
        return self._data.data

    def checksum(self):
        """
        @return The stream's checksum
        """
        return self._checksum

    def __len__(self):
        """
        @return The Stream's size
        """
        return len( self._data.data )


class FileStream(Stream):
    """
    Class that represents an opened file
    @see Stream
    """

    def __init__(self, name='', owner=None, group=None, serv = "", data = ""):
        """
        Class constructor
        @param name: File base name
        @param owner: Owner's id
        @param group: Owner's group id
        @param data: File's content
        """
        Stream.__init__(self, data)
        self.__name    = str(name)
        self.__owner   = owner
        self.__group   = group
        self.__service = serv
        self.__id      = 0

    def getname(self):
        """
        @return The file name
        """
        return self.__name

    def getowner(self):
        """
        @return The file's owner id
        """
        return self.__owner

    def getgroup(self):
        """
        @return The owner's group id
        """
        return self.__group

    def getid(self):
        """
        @return The file id
        """
        return self.__id

    def getservice(self):
        """
        @return The storage service
        """
        return self.__service

    def setname(self, name):
        """
        Updates the file name
        @param name
        """
        self.__name = name

    def setowner(self, owner):
        """
        Updates the file's owner id
        @param owner
        """
        self.__owner = owner

    def setgroup(self, group):
        """
        Updates the owner's group id
        @param owner
        """
        self.__group = group

    def setid(self, fid):
        """
        Updates the file id
        @param fid
        """
        self.__id = fid

    def registerfile( self, dbase, host ):
        """
        @param db: PGDataBase instance. Database controller instance
        @param host: Integer. node's id where the file will be processed
        """
        ver, self.__id =  dbase.storefile(
            self.__name,
            self.checksum(),
            self.__service,
            self.__owner,
            self.__group,
            len( self._data.data ),
            host
        )

        return ver, self.__id

class FragmentStream(Stream):

    """
    Class that represents a file fragment.
    @see Stream
    """

    def __init__( self, fileid = 0, fname = "", pos = 0, service = "", data = "" ):
        """
        FileStream's constructor
        @param fileid: File's id 
        @param fname: String File's name
        @param pos: Fragment's position at the file
        @param data: Fragment's content
        """
        Stream.__init__(self, data)
        self.__fileid  = fileid
        self.__fname   = fname
        self.__pos     = pos
        self.__service = service
        self.__id      = 0

    def getfileid(self):
        """
        @return The Fragment's file id
        """
        return self.__fileid

    def setfileid(self, fid):
        """
        Updates the Fragment's file id
        @param fid
        """
        self.__fileid = fid

    def getfilename(self):
        """docstring for getfilename"""
        return self.__fname

    def setfilename(self, fname):
        """docstring for getfilename"""
        self.__fname = fname

    def getpos(self):
        """
        @return the Fragment's position in the file
        """
        return self.__pos

    def setpos(self, pos):
        """
        Updates the Fragment's position in th file
        @param pos
        """
        self.__pos = pos

    def getid(self):
        """
        @return The Fragment's id
        """
        return self.__id

    def getservice(self):
        """
        @return String. storage service
        """
        return self.__service

    def registerfragment(self, dbase, host):
        """
        @param db: Database controller instance
        @param host: node's id where the fragment will be processed
        """
        self.__id = dbase.storefragment(
            self.__fname,
            self.__fileid,
            self.__pos,
            self._checksum,
            len( self._data.data ),
            host
        )
        
        return self.__id

class BlockStream(Stream):
    """Class that represents a block stream (copy or ida disperse)"""
    def __init__(self, fname = "", btype = "copy", fragid = 0,  pos = 0, data = "" ):
        """
        BlockStream Class constructor
        @param btype: String. The block type: Copy, IDA, etc.
        @param fragid: Integer. The frament where
        """
        Stream.__init__(self, data)
        self.__id    = 0
        self.__type  = btype
        self.__fname = fname
        self.__fid   = fragid
        self.__pos   = pos

    def __cmp__(self, other):
        """Compasres two BlockStream Instances"""
        
        res = self.__fid - other.getfragid()
        return res if res else self.__pos - other.getposition()
    
    def gettype(self):
        """@return The Block's type"""
        return self.__type

    def getfilename(self):
        """docstring for getfilename"""
        return self.__fname

    def setfilename(self, fname):
        """docstring for getfilename"""
        self.__fname = fname

    def getfragid(self):
        """@return the fragment's id where the block belongs"""
        return self.__fid

    def getposition(self):
        """@return the block's position"""
        return self.__pos

    def registerblock(self, dbase, host):
        """
        @param db: Database controller instance
        @param host: node's id where the fragment will be processed
        """
        self.__id = dbase.storeblock(
            self.__fname,
            self.__fid,
            self.__type,
            self.__pos,
            self._checksum,
            host,
            len( self._data.data )
        )
        
        return self.__id
