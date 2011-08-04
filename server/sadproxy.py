# -*- coding:utf-8 -*-
"""
Created on 25/05/2011

@author: diacus
"""

import logging
from data.message       import Message
from data.stream        import FileStream
from lib.common         import MessagesENG as Messages, notimplementedfunction
from server.sadnode     import Node, Handler

class ProxyHandler(Handler):
    """
    Proxy request handler class
    """

    def __init__(self):
        """
        Proxy Handler constructor
        """
        Handler.__init__(self)
        self._neighbors = self._dbase.selectvirtualspaces()

    def connect( self, (user, passwd) ):
        """
        Open a connection to the server
        @param (user, passwd): a touple that contains the user name, and user
        password
        """
        print Messages.StartingConnect
        msg = Messages.TryingLogin % (user)
        print msg
        logging.info(msg)
        usr = self._dbase.selectuser(nick=user)
        res = None
        if passwd == usr.getpasswd():
            res = Message.SUCCESS, usr.getid()
            msg = Messages.UserConnected % (user)
            print msg
            logging.info(msg)
        else:
            res = Message.FAILURE, 0
            msg = Messages.UserRefused % (user)
            print msg
            logging.error(msg)
        return res 

    def storestream(self, sdata ):
        """
        Logs a file into the proxy and send it to the server where it'll be
        stored
        @param sdata:
        @return: Current File's version.
        """
        stream = FileStream()
        stream.load(sdata)

        node = self._neighbors.nextval()
        # Recording operation.
        # sid : File's id
        # ver: File's current version
        sid, ver = stream.registerfile( self._dbase, node.getid() )
        # Sending stream
        node.client.sendfile( stream )
        msg = Messages.SendingFileTo % (stream.getname(), node.getname(),
            node.geturi(), ver)
        print msg
        logging.info(msg)
        return Message.SUCCESS, ver

    def loadstream( self, fname ):
        pass


    def listfiles(self, uid):
        """
        @param uid: User id
        @return A list with the user's stored files
        """
        user = self._dbase.selectuser(uid)
        msg = Messages.ListingFiles % user.getnick()
        lstfiles = self._dbase.selectuserfiles(uid)
        strings = [ str(f) for f in lstfiles ]
        print msg
        logging.info(msg)
        return Message.SUCCESS, strings

    def listservices(self, uid):
        """
        Lists the available services for the given user.
        @param uid: Integer. User's id
        @return A list that contains the available services
        """
        user  = self._dbase.selectuser(uid)
        servs = self._dbase.selectuserservices(uid)
        msg   = Messages.ListingServs % user.getnick()
        print msg
        logging.info(msg)
        code = Message.SUCCESS if servs else Message.FAILURE
        return code, servs


class Proxy ( Node ):
    """
    Celda Proxy class
    """

    def __init__(self):
        """
        Constructor class
        """

        Node.__init__(self)

        self._funcs[Message.SAVESTREAM]   = ProxyHandler.storestream
        self._funcs[Message.LISTFILES]    = ProxyHandler.listfiles
        self._funcs[Message.LISTSERVS]    = ProxyHandler.listservices
        self._funcs[Message.CONNECT]      = ProxyHandler.connect
        self._funcs[Message.LOADSTREAM]   = ProxyHandler.loadstream
        self._funcs[Message.ADDUSER]      = notimplementedfunction
        self._funcs[Message.DISUSER]      = notimplementedfunction
        self._funcs[Message.ADDGROUP]     = notimplementedfunction
        self._funcs[Message.DELGROUP]     = notimplementedfunction
        self._funcs[Message.ADDNODE]      = notimplementedfunction

