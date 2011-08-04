#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
Client test
"""

from client.sadclient import NodeClient
from data.message     import Message
from data.stream      import BlockStream
from os.path          import expanduser
from db.pgdata        import PGDataBase as DB

def main():
    """
    Test main function
    """
    
    print "Iniciando prueba para base de datos"
    datos = DB( 'postgres', 'radeck86', 'celda')
    fname = expanduser('~/Dropbox/src/celda/file/calendario.cal')
    print "Enviando el 'bloque'", fname
    stream = BlockStream()
    stream.loadfromfile(fname)
    print stream

    stream.registerblock( datos, 2 )

    print "prueba finalizado"


if __name__ == '__main__':
    main()



