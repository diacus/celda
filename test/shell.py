# -*- coding:utf-8 -*-

from client.sadclient import Client, ClientDisconnected
from cmd import Cmd
import sys

class Shell(Cmd):
    prompt = "celda:> "
    def __init__(self, store):
        Cmd.__init__(self)
        self.__storage = store
        self.__server = ""
    
    def do_connect(self, arg):
        self.__server = arg
        
    def do_get(self, arg):
        try:
            c = Client(self.__storage)
            c.get(arg, self.__server)
        except ClientDisconnected, e:
            print "No se ha establecido ninguna conexión", e
        except Exception, e:
            print "ha ocurrido un error", e
        
    def do_post(self, arg):
        try:
            c = Client(self.__storage)
            c.post(arg, self.__server)
        except ClientDisconnected, e:
            print "No se ha establecido la conexión", e
        except Exception, e:
            print "ha ocurrido un error", e
    
    def do_exit(self, arg):
        sys.exit()
    
    do_EOF = do_exit