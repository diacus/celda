# -*- coding:utf-8 -*-

"""
@file sadclient.py

Client class both client application and permanent peers.
"""

import hashlib, logging, os
from data.message import Message
from data.stream  import FileStream 
from lib.common   import MessagesENG as Messages
from xmlrpclib    import ServerProxy, Fault

class RawClient:

    """
    Generic client class
    """

    def __init__(self, uri):
        """
        RawClient constructor

        @param uri: celda's Proxy URI
        """
        self._uri = str(uri)
        self._proxy = ServerProxy(uri)

    def _send(self, mtype, arg):
        """
        Sends a message to the server
        """
        res = Message.FAILURE, ["Error"]
        msg = Messages.TryingConnection % self._uri
        logging.info(msg)
        try:
            res = self._proxy.attend(mtype, arg)
        except Fault, f:
            msg = Messages.ServerError % (self._uri, f.faultString)
            print msg
            logging.error(msg)
            res = Message.FAILURE, f.faultString
        return res

    def ping(self):
        """
        Tests if the server is running
        """
        return self._proxy.ping()

    def __str__(self):
        """
        @return Client's string form
        """

        return "Client for %s host" % (self._uri)

class Client(RawClient):

    """
    User application client class
    @see RawClient
    """

    def __init__(self, uri, downloads):
        """
        Client constructor

        @param uri: String. celda's Proxy URI
        @param downloads: String. Downloads path
        """
        RawClient.__init__(self, uri)
        self._uid = 0
        self._uname = ""
        self._downloads = downloads

    def connect(self, user, password ):
        """
        @param user: The user name
        @param password: The user's password
        """

        msg = Messages.Connecting % self._uri
        print msg

        upwd = hashlib.md5(password).hexdigest()
        code, self._uid = self._send( Message.CONNECT, (user, upwd) )
        if self._uid > 0:
            self._uname = user
            msg = "Starting session for user " + user
            logging.info(msg)
        else:
            msg = "Accesss denied for user " + user
            logging.error(msg)
        return code

    def disconnect(self):
        """
        Ends the current client sesion
        """
        msg = "Ending session for user " + self._uname
        self._uid = 0
        logging.info(msg)

    def storefile( self, fname, service ):
        """
        Send a file to the proxy for storing
        @param fname: String. Contains the file's name
        @param service: String. Contains the storage service
        @return A touple that contains the request's status and the file's curren
        version
        """
        s = FileStream(os.path.basename(fname), self._uid, self._uid, service)
        s.loadfromfile(fname)
        code, ver = self._send( Message.SAVESTREAM, s.serialize() )
        return code, ver

    def getfile( self, fname ):
        """
        Asks for a file
        @param fname: String. file's base name
        @return A FileStream instance that contains the requested file
        """
        conf = Config()
        fpath  = os.path.join( self._downloads, fname )
        result = FileStream()
        code, data = self._send( Message.LOADSTREAM, fname )
        result.load(data)
        result.savetofile(fpath)
        print "Done"


    def isconnected(self):
        """
        @return True if the client's user id is bigger than 0, False otherwhise
        """
        return self._uid > 0
    
    def listfiles(self):
        """
        List the user's files
        """
        code, lstfiles = self._send( Message.LISTFILES, self._uid )
        return code, lstfiles

    def listservices(self):
        """
        @return list. The services available for the given user
        """
        code, lstservs = self._send( Message.LISTSERVS, self._uid )
        return code, lstservs

    def getusername(self):
        """
        @return The current user's name
        """
        return self._uname

        
    # def get( self, filename):
    #     path = os.path.join(os.path.curdir,filename)
    #     data = self._proxy.get(filename,self._uid).data
    #     f = open(path, "wb")
    #     f.write(data)
    #     f.close()
    #     
    # def sendStream(self, id, stream, type, fname, owner, peer):
    #     """
    #     Send a stream to a given peer.
    #     
    #     @param id: Stream's id.
    #     @param stream: Stream's data.
    #     @param type: Stream's type (fragment or disperse). 
    #     """
    #     if stream :
    #         # This method is not implemented yet
    #         self._proxy.recive(id, Binary(stream), type, fname, owner)
    #     else:
    #         raise EmptyStream
    #     

class NodeClient(RawClient):

    """
    Node application client class
    @see RawClient
    """

    def __init__(self, uri):
        """
        NodeClient constructor
        @param uri: String, contains the server URI in this format:
        protocol://host:port
        """
        RawClient.__init__(self, uri)


    def sendfile(self, ffile):
        """
        Sends an opened file to the node
        @param ffile: FileStream instance
        """
        cont = ffile.checksum(), ffile.serialize()
        return self._send( Message.SAVESTREAM, cont )

    def requestfile(self, fname, uid):
        """
        Asks for the file named fname, which owner is the uid user.

        @param fname: String, contains the requested file name
        @param uid: Integer, contains the owner's user id
        @return A FileStream instance that contains the file requested
        """
        pass

    def sendfragment(self, fragment):
        """
        Sends a fragment
        @param fragment: FragmentStream instance
        @see FragmentStream
        """
        cont = fragment.checksum(), fragment.serialize()
        return self._send( Message.SAVEFRAGMENT, cont )

    def sendblock(self, block):
        """
        Sends a block
        @param block: BlockStream instance
        @see BlockStream
        """
        cont = block.checksum(), block.serialize()
        return self._send( Message.SAVEBLOCK, cont )

