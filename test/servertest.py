# -*- coding: utf-8 -*-
'''
Created on 11/05/2011

@author: diacus
'''

from client.sadclient import NodeClient
from data.stream      import BlockStream
from lib.common       import Message
from os.path          import expanduser
 
def main():
    """
    Función principal de la prueba del servidor
    """
    print "Iniciando prueba de servidor"
    fname = expanduser('~/Dropbox/src/celda/file/calendario.cal')
    print "Enviando el 'bloque'", fname
    stream = BlockStream()
    stream.loadfromfile(fname)

    client = NodeClient( "http://192.168.86.99:4242" )
    print stream
    client.sendblock( stream )

    print "prueba terminada"

if __name__ == '__main__' :
    main()
