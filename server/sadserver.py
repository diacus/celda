# -*- coding:utf-8 -*-

"""
@file sadserver.py
sadserver module
"""

import os, logging
from data.message       import Message
from data.stream        import FileStream, FragmentStream, BlockStream
from lib.common         import MessagesENG as Messages, splitstream, \
    notimplementedfunction
from lib.config         import SADConfig
from lib.ida            import disperse, recover
from lib.saderror       import CorruptedFile
from server.sadnode     import Node, Handler
from xmlrpclib          import Fault

class ServerHandler(Handler):

    """
    Class for handle requests
    """

    def __init__(self):
        Handler.__init__(self)
        self._neighfrag  = self._dbase.selectvirtualspaces()
        self._neighfrag.choice()
        self._neighblock = self._dbase.selectvirtualspaces()
        self._neighblock.choice()
    
    def processfile( self, (check, sdata) ):
        """
        Splits a stream to a set of fragments and give them to other peers.

        @param (check, sdata): Where:

        * check is the stream's checksum
        * sdata is a dict for build a FileStream instance
        
        @raise CorruptedFile: Raise this exception if the given checksum doesn't
        match with the stream's checksum 
        """

        conf   = SADConfig()
        stream = FileStream()
        stream.load(sdata)
        data   = stream.getdata()
        
        if not check == stream.checksum():
            raise CorruptedFile
        
        if len(stream) > conf.getmsu():
            pieces = splitstream(data, conf.getmsu())
            msg = Messages.FileSplitUp % (stream.getname(), len(pieces) )
            print msg
            logging.info( msg )

        else:
            pieces = [data]
            msg = Messages.SmallFile % stream.getid()
            print msg
            logging.info( msg )

        for i, piece in enumerate(pieces):
            # Selecting next node
            node = self._neighfrag.nextval()
            # Packing the fragment stream
            frag = FragmentStream(
                stream.getid(),
                stream.getname(),
                i,
                stream.getservice(),
                piece
            )

            # Storing meta data
            frag.registerfragment(self._dbase, node.getid())

            if self.itsme( node ) :
                self._localprocessfragment(frag)
            else:
                # Sending fragment
                try:
                    msg = Messages.SendingFragTo % (
                        stream.getname(),
                        i,
                        node.getname(),
                        node.geturi()
                    )
                    # Logging transaction
                    print msg
                    logging.info(msg)
                    node.client.sendfragment(frag)
                except Fault, cf:
                    print cf
                    logging.error( str(cf) )


    def _localprocessfragment(self, fragment):
        """
        @param fragment: FragmentStream instance
        @see FragmentStream
        """
        
        serv = fragment.getservice()
        msg = Messages.SelectedService % serv
        print msg
        logging.info(msg)

        if serv == "copy":
            block = BlockStream(
                serv,
                fragment.getid(),
                fragment.getpos(),
                fragment.getdata(),
            )
            for b in [block, block]:
                node = self._neighblock.nextval()
                b.registerblock( self._dbase, node.getid())
                if self.itsme( node ) :
                    self._localprocessblock(b)
                else:
                    node.client.sendblock(b)

        elif serv == "IDA":
            ##
            # @todo utilizar IDA
            for i, b in enumerate( disperse( fragment ) ):
                node = self._neighblock.nextval()
                b.registerblock( self._dbase, node.getid() )
                if self.itsme( node ) :
                    self._localprocessblock(b)
                else:
                    node.client.sendblock(b)


    def processfragment(self, (check, fdata) ):
        """
        @param sdata FragmentStream instance data

        @raise CorruptedFile: Raise this exception if the given checksum
        doesn't match with the stream's checksum 
        """

        fragment = FragmentStream()
        fragment.load(fdata)

        if not check == fragment.checksum():
            del fragment
            raise CorruptedFile

        self._localprocessfragment(fragment)

    def _localprocessblock( self, block ):
        """
        @param block: FragmentStream instance
        """
        conf = SADConfig()
        bname = os.path.join( conf.getstoragepath(), block.getfilename() )
        msg = Messages.ProcessingBlock % str(block)
        logging.info(msg)
        print msg
        block.savetofile( bname )

    def processblock(self, (check, bdata)):
        """
        @param check: String. BlockStream's checksum
        @param bdata: String, BlockStream's data
        """

        block = BlockStream()
        block.load(bdata)

        if not check == block.checksum():
            raise CorruptedFile

        self._localprocessblock(block)

class Server ( Node ):
    """
    Inner node class
    """
    def __init__( self ):

        Node.__init__(self)
        self.__neighfrag = self._dbase.selectvirtualspaces()
        self.__neighidas = self._dbase.selectvirtualspaces()

        self._funcs[Message.SAVESTREAM]   = ServerHandler.processfile
        self._funcs[Message.SAVEFRAGMENT] = ServerHandler.processfragment
        self._funcs[Message.SAVEBLOCK]    = ServerHandler.processblock
        self._funcs[Message.LOADSTREAM]   = notimplementedfunction
        self._funcs[Message.LOADFRAGMENT] = notimplementedfunction
        self._funcs[Message.LOADBLOCK]    = notimplementedfunction

