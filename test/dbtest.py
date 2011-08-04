#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
Created on 13/05/2011

@author: diacus
"""

import sys, os, hashlib
sys.path.append("..")
from cmd        import Cmd
from db.pgdata  import PGDataBase as DataBase
from lib.common import DataBaseCreator

try:
    from psycopg2 import OperationalError
except ImportError, e:
    print "Couldn't import OperationalError:", e
    sys.exit(0)
    


class SHClient(Cmd):
    
    prompt = "dbtest:> "
    def __init__(self):
        Cmd.__init__(self)
        self.__db = None
        
    def do_connect(self, arg):
        try:
            self.__db = DataBase("postgres","postgres","celda")
        except OperationalError, e:
            sys.stderr.write(str(e)+"\n")
        
    def do_dbinstall(self,arg):
        if self.__db :
            dbc = DataBaseCreator()
            dbc.reset(self.__db)
        else:
            sys.stderr.write("Data base disconnected.\n")
            
    def do_adduser(self, arg):
        passwd = raw_input("password:> ")
        name = raw_input("fullname:> ")
        email = raw_input("e-mail:> ")
        service = int(raw_input('level service:> '))
        
        self.__db.addUser(arg, passwd, name, email, service)
        
    def do_addVirtualSpace(self, arg):
        measure = {'k':1, 'm':1024, 'g':1048576, 't':1073741824}
        host  = raw_input("host:> ")
        sSize = raw_input("size:> ").lower()
        size = float(sSize[:-1]) * measure[ sSize[-1] ]
        self.__db.addVirtualSpace(arg, host, size)
        
    def do_finger(self, arg):
        user = None
        try:
            id = int(arg)
            user = self.__db.selectUser(uid=id)
        except:
            user = self.__db.selectUser(email=arg)
        finally:
            print user
        
    def do_store(self, arg):
        if os.path.isfile(arg) :
            file = os.path.basename(arg)
            f = open(arg, "rb")
            body = f.read()
            size = len(body)
            hash = hashlib.md5(body)
            self.__db.storeFile(file, hash.hexdigest(), 1, 1, size, 1)
        else:
            print "File", arg, "not found."
            
    def do_exit(self, arg):
        print "Good Bye"
        sys.exit()
    
    do_EOF = do_exit

def main():
    console = SHClient()
    console.cmdloop()

if __name__ == "__main__":
    main()