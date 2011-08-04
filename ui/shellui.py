# -*- coding:utf-8 -*-

"""
Created on 25/05/2011

@author: diacus
"""

import os, sys
from cmd              import Cmd
from client.sadclient import Client
from data.message     import Message
from lib.common       import MessagesENG as Messages

class SADShell(Cmd):
    """
    Command line based user interface for the celda distributed storage system.
    """
    
    prompt = "celda:> "

    def __init__(self):
        """
        SADShell Constructor
        """
        Cmd.__init__(self)

    def setclient(self, cnt):
        """
        Sets the user interface client
        @param cnt: Client instance
        @see Client
        """
        self._client = cnt
        
    def do_post(self, arg):
        """
        Command post definition
        @param arg: String. Path to a file
        """
        code, services = self._client.listservices()
        if code == Message.SUCCESS:
            print "Pleas select a storage mode:"
            for (k, serv) in enumerate(services):
                print " (%d) %s" % (k + 1, serv)

            choice = False
            while not choice:
                try:
                    s = int( raw_input("service: ")) - 1
                    service = services[s]
                    choice = True
                except TypeError, err:
                    print err
                    print "Type an integer please"
                except IndexError, irr:
                    print irr

            try:
                code, ver = self._client.storefile(arg, service)
                if code == Message.SUCCESS:
                    print Messages.FileSaved % (os.path.basename(arg), ver)
                else:
                    print Messages.FileNotSaved % (os.path.basename(arg))
            except IOError, e:
                print e
        else:
            print Messages.NoServsAvailable
        
    def help_post(self):
        """
        Help function for the post command
        """
        susage = """Usage: post <file>
        Stores <file> at celda
        """
        print susage
    
    def do_get(self, arg):
        """
        Command get definition
        @param arg:
        """
        try:
            self._client.get(arg)
        except:
            print "Error"
        
    def help_get(self):
        """
        Help function for the get command
        """
        print "Ask for a file"
        
    def do_lls(self, arg):
        """
        Command lls definition. Lists a local directory
        @param arg: Directory to list its content
        """
        if not arg:
            arg = os.path.curdir
        for item in os.listdir(arg):
            print item
            
    def help_lls(self):
        """
        """
        print "Prints the local folder content"
            
    def do_ls(self,arg):
        """
        """
        code, lstfiles = self._client.listfiles()
        if code == Message.SUCCESS and lstfiles:
            print "   Version  Size     Name"
            for f in lstfiles:
                print f
            
    def help_ls(self):
        """
        """
        print "List the files stored at the system."
    
    def do_cd(self,arg):
        """
        """
        try:
            if arg == '':
                arg = '~'
            os.chdir(os.path.expanduser(arg))
        except OSError, e:
            print e
    
    def help_cd(self):
        """
        """
        print "Change the current local directory"
        
    def do_pwd(self, arg):
        """
        """
        print os.path.abspath(os.path.curdir)
        
    def help_pwd(self):
        """
        """
        print "Prints the current directory's path"
    
    def do_adduser(self, arg):
        """
        """
        print Messages.Notimplemented
        
    def help_adduser(self):
        """
        """
        print "Create a new user"
        
    def do_addgroup(self, arg):
        """
        """
        print Messages.Notimplemented
        
    def help_addgroup(self):
        """
        """
        print "Create a new group"
    
    def do_whoami(self,arg):
        """
        """
        print self._client.getusername()
        
    def help_whoami(self):
        """
        """
        print "Prints the current user name"
    
    def do_exit(self, arg):
        """
        """
        print "Good Bye"
        self._client.disconnect()
        sys.exit()
        
    def help_exit(self):
        """
        """
        print "Ends the current sesion."
    
    do_EOF = do_exit

    def do_clear(self, arg):
        """
        Clears the screen
        """
        del arg
        os.system('clear')
