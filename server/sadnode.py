# -*- coding: utf-8 -*- 
"""
@file sadnode.py

sadnode module
"""

from SocketServer       import ThreadingMixIn
from SimpleXMLRPCServer import SimpleXMLRPCServer
from xmlrpclib          import Fault
from lib.config         import SADConfig
from data.message       import Message
from lib.common         import MessagesENG as Messages

import logging

class NodeListener(ThreadingMixIn, SimpleXMLRPCServer):
    """
    Class for handle multiple requests at the same time
    """
    pass
        

class Handler:
    """
    Generic request handler
    """

    def __init__(self):
        """
        Class constructor
        """
        conf = SADConfig()
        self._host      = conf.getaddress()
        self._port      = conf.getport()
        self._storage   = conf.getstoragepath()
        self._dbase     = conf.getdb()
        self._msu       = conf.getmsu()

    def getdb(self):
        """
        @return the instance's data base controller
        """
        return self._dbase

    def getmsu(self):
        """
        @return the maximum storage unit value
        """
        return self._msu

    def geturi(self):
        """
        @return the node uri
        """
        return "%s:%d" % (self._host, self._port)

    def itsme( self, vspace ):
        """
        @return True if host is the same uri than the instance's, False
        otherwise
        """
        return self.geturi() == vspace.geturi()

    __str__ = geturi

    
class Node:

    """
    Generic node class
    """
    def __init__(self):
        """
        Class constructor   
        """

        conf = SADConfig()

        self._host    = conf.getaddress()
        self._port    = conf.getport()
        self._storage = conf.getstoragepath()
        self._dbase   = conf.getdb()
        self._msu     = conf.getmsu()
        self._handler = None
        self._funcs   = dict()

    def start( self ):
        """
        Starts the server
        """
        srv = NodeListener(
            (self._host, self._port),
            logRequests=False,
            allow_none=True
        )

        srv.register_instance( self )
        print "Starting service"
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            print "\nSystem halt."

    def _strdata(self, data):
        """
        @param data: Object. Contains the data recived
        @return String. a printable representation of the recived data
        """
        strdata = ""
        if type(data) == dict:
            for (k, v) in data.items():
                strdata += "%-25s: %s\n" % (str(k), repr(v))
        elif type(data) in [list, tuple]:
            strdata += "List recived\n"
            for item in data:
                strdata += self._strdata(item) + "\n"
        else:
            strdata += str(data) + "\n"

        return strdata

    def attend( self, mtype, message ):
        """
        Method used for invoke the handler when a request is recived
        @param mtype: The request code
        @param message: the request's data
        """

        msg = Messages.RequestRecived % str(mtype)
        print msg
        logging.info(msg)
        print Messages.DataRecived % self._strdata(message)

        res = ( Message.FAILURE, Messages.Notimplemented )
        try:
            res = self._funcs[mtype](self._handler, message)
            msg = Messages.RequestProcessed % str(mtype)
            print msg
            logging.info(msg)

        except KeyError:
            msg = Messages.UnsupportedReq % (mtype)
            print msg
            logging.error(msg)

        except Fault, f:
            msg = Messages.FaultRaise % (f.faultCode, f.faultString)
            print msg
            logging.error(msg)

        return res

    def sethandler( self, handler ):
        """
        Sets the node's request handler
        @param handler
        """
        self._handler = handler

    def ping(self):
        """
        Testing if the server still alive
        """

        msg = "%s:%d -- I'm still alive" % (self._host, self._port)
        print msg
        return msg

