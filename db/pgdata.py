# -*- coding:utf-8 -*-

"""
Created on 13/05/2011
@file pgdata.py
@author: Diego Rodrigo Guzmán Santamaría
@email: dr.guzsant@gmail.com
"""

import logging, sys
from lib.common    import MessagesENG as Messages, CycleQueue
from server.common import VirtualSpace
from data.users    import SADUser, SADFile
try:
    import psycopg2
except ImportError, e:
    print "Couldn't import psycopg2 module"
    sys.exit()

def dbsetup(database):
    """
    Creates the data base tables
    @param database: A data base controller instance
    """
    tables = { 
        'services': """
        DROP TABLE IF EXISTS services CASCADE;
        CREATE TABLE services(
            sid SERIAL PRIMARY KEY,
            name VARCHAR(50),
            available BOOLEAN NOT NULL DEFAULT True,
            description TEXT
        )
        """,
        'users' : """
        DROP TABLE IF EXISTS users CASCADE;
        CREATE TABLE users (
            uid SERIAL PRIMARY KEY,
            nick VARCHAR(20) UNIQUE NOT NULL,
            password VARCHAR(32) NOT NULL,
            fullname VARCHAR(100) NOT NULL,
            email VARCHAR(50) UNIQUE NOT NULL,
            createdon DATE NOT NULL DEFAULT CURRENT_DATE,
            enabled BOOLEAN NOT NULL DEFAULT True
        )
        """,
        'usr2srv':"""
        DROP TABLE IF EXISTS usr2srv CASCADE;
        CREATE TABLE usr2srv (
            usr INTEGER REFERENCES users (uid),
            service INTEGER REFERENCES services (sid),
            PRIMARY KEY(usr,service)
        )
        """,
        'groups': """
        DROP TABLE IF EXISTS groups CASCADE;
        CREATE TABLE groups(
            gid SERIAL PRIMARY KEY,
            name VARCHAR(20) NOT NULL,
            owner INTEGER REFERENCES users (uid)
        )
        """,
        'membership' : """
        DROP TABLE IF EXISTS membership CASCADE;
        CREATE TABLE membership (
            uid INTEGER REFERENCES users  (uid),
            gid INTEGER REFERENCES groups (gid),
            PRIMARY KEY (uid,gid)
        )
        """,
        "virtualspaces" : """
        DROP TABLE IF EXISTS virtualspaces CASCADE;
        CREATE TABLE virtualspaces (
            vsid SERIAL PRIMARY KEY,
            label VARCHAR(30),
            host VARCHAR(30),
            port INTEGER,
            size INTEGER
        )
        """,
        "files" : """
        DROP TABLE IF EXISTS files CASCADE;
        CREATE TABLE files(
            fid SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            hash VARCHAR(32) NOT NULL,
            service VARCHAR(25) NOT NULL,
            owner INTEGER REFERENCES users  (uid),
            gid INTEGER REFERENCES groups (gid),
            size INTEGER NOT NULL,
            version INTEGER NOT NULL,
            host integer REFERENCES virtualspaces (vsid),
            createdon DATE NOT NULL DEFAULT CURRENT_DATE,
            topversion BOOLEAN DEFAULT True
        )
        """, 
        "fragments" :"""
        DROP TABLE IF EXISTS fragments CASCADE;
        CREATE TABLE fragments(
            fid SERIAL PRIMARY KEY,
            fname TEXT,
            file INTEGER NOT NULL,
            pos INTEGER NOT NULL,
            hash VARCHAR(32) NOT NULL,
            host INTEGER REFERENCES virtualspaces (vsid),
            size INTEGER NOT NULL,
            createdon DATE NOT NULL DEFAULT CURRENT_DATE
        )
        """,
        "blocks":"""
        DROP TABLE IF EXISTS blocks CASCADE;
        CREATE TABLE blocks(
            fname TEXT,
            bid SERIAL PRIMARY KEY,
            fragment INTEGER NOT NULL,
            btype VARCHAR(256) NOT NULL,
            pos INTEGER NOT NULL,
            hash VARCHAR(32) NOT NULL,
            host INTEGER REFERENCES virtualspaces (vsid),
            size INTEGER NOT NULL,
            createdon DATE NOT NULL DEFAULT CURRENT_DATE
        )
        """
    }
    
    order = [
        "services",
        "users",
        "usr2srv",
        "groups",
        "membership",
        "virtualspaces",
        "files",
        "fragments",
        "blocks"
    ]
    for tname in order:
        print Messages.CreateTable % tname
        database.query(tables[tname])

class PGDataBase:
    """
    Data base abstraction layer
    """

    def __init__( self, user, passwd, dbname ):
        """
        Constructor
        @param user: Data base user
        @param passwd: Data base user's passowrd
        @param dbname: Data base name
        """
        self.__user   = user
        self.__passwd = passwd
        self.__dbname = dbname
        try:
            self.__conn   = psycopg2.connect(
                "dbname=%s user=%s password=%s" %
                (dbname, user, passwd)
            )
            self.__cursor = self.__conn.cursor()
        except psycopg2.Error, err:
            print err
            print Messages.CantConnectDB
            sys.exit(1)

    def select( self, table, fields = () ):
        """
        Performs a SELECT query into the data base
        @param table: Sting, conains the table name
        @param fields: String touple, contains the fields names
        @return This methis is not implemeted yet
        """
        raise NotImplementedError

    def selectservices(self):
        """
        Selects all the service names
        """
        return map( lambda x: x[0], self.query("SELECT name FROM services"))

    def selectuserservices(self, uid):
        """
        Asks to data base the available services for the given user
        @param uid: Integer. The user's id
        @return A list that contains the service names availables for the given
        user.
        """
        q = """
        SELECT s.name FROM services AS s, users AS u, usr2srv AS o
        WHERE u.uid = o.usr AND o.service = s.sid AND u.uid = %d"""
        return map( lambda x : x[0], self.query(q % (uid) ))

    def adduser(self, nick, password, fullname, email, service = 1 ):
        """
        Add a new user.
        
        @param nick:     The user's login name.
        @param password: The user's password.
        @param fullname: The user's full name.
        @param email:    The user's e-mail address (must be unique).
        @param service:  A number that indicates QoS for the new user.
        """
        query = """INSERT INTO users
        (nick,password,fullname,email)
        VALUES(%s,MD5(%s),%s,%s)"""
        user = (nick, password, fullname, email) 
        self.__cursor.execute(query, user)
        
        self.__cursor.execute("SELECT uid FROM users WHERE email = '%s'"
                                % (email))
        uid = self.__cursor.fetchone()[0]
        msg = Messages.CreateUser % nick
        print msg
        logging.info(msg)
        self.__conn.commit()
        
        gid = self.addgroup(nick, uid)
        self.adduser2group(uid, gid)
        self.bringservice2user(uid, service)
        return uid


    def disableuser(self, uid):
        """
        Disable a user account.
        @param uid: User's account id
        """
        query = "UPDATE users SET enabled = False WHERE uid = %s"
        self.__cursor.execute(query,(uid,))
        self.__conn.commit() 

    def enableuser(self, uid):
        """
        Enable a user account.
        @param uid: User's account id
        """
        query = "UPDATE users SET enabled = True WHERE uid = %s"
        self.__cursor.execute(query,(uid,))
        self.__conn.commit()

    def updateuser(self, uid, nick, passwd, fullname, email):
        """
        Updates the user's data
        @param uid:      Integer. User's id
        @param nick:     String. User's name
        @param passwd: String. User's password
        @param fullname: String. User's fullname
        @param email:    String. User's e-mail address
        """

        q = """UPDATE users SET nick = %s, password = %s, fullname = %s, email =
        %s WHERE uid = %d"""

        self.query( q % (nick, passwd, fullname, email, uid) )

    def selectusers(self):
        """
        @return: A list that contains all the enabled users.
        """
        users = []
        self.__cursor.execute(
            """SELECT uid,nick,password,fullname,email,createdon FROM users
            WHERE enabled = 'True' ORDER BY fullname"""
        )
        
        for uid, nick, passwd, name, email, since in self.__cursor.fetchall():
            users.append(SADUser(uid, nick, passwd, name, email, since))
        
        return users

    def selectuser(self, uid = None, nick = None, email = None):
        """
        Selects a user's record by its uid or email field.
        @param uid:   User's ID
        @param nick:  User's nick name
        @param email: User's e-mail address.
        @return:      A tuple that contains the user's data if there's a
        record that matches. None otherwise. 
        """

        q = """SELECT uid, nick, password, fullname, email, createdon FROM
        users WHERE """
        user = None

        if uid :
            msg =  Messages.SelUsrID % uid
            q += "uid = %d AND enabled = True" % uid 

        elif nick:
            msg = Messages.SelUsrNick % nick
            q += "nick = '%s' AND enabled = True" % nick

        elif email:
            msg = Messages.SelUsrMail % email
            q += "email = '%s' AND enabled = True" % email
            
        self.__cursor.execute( q )
        print msg
        logging.info(msg)

        if uid or email or nick:
            uid, nick, passwd, name, mail, since = self.__cursor.fetchone()
            user = SADUser(uid, nick, passwd, name, mail, since)
            
        return user
        

    def addvirtualspace(self, label, host, port, size):
        """
        Register a virtual storage space
        
        @param label: String, The virtual space's alias.
        @param host:  String, The virtual space's ip address or host name.
        @param port:  Integer. The virtual space's listening port
        @param size:  The virtual space's storage capacity  
        """
        query = """INSERT INTO virtualspaces
        (label, host, port, size)
        VALUES (%s,%s, %s, %s)
        """
        self.__cursor.execute(query, (label, host, port, size) )
        self.__conn.commit()

    def replacevirtualspace(self, vid, host):
        """
        Replaces a virtual space's host
        @param id: The virtual space's ID.
        @param host: The virtual space's ip address or host name.  
        """
        cond  = " WHERE vsid = %d" % vid
        query = "UPDATE virtualspaces SET host = %s" + cond
        self.__cursor.execute(query, (host,))
        self.__conn.commit()
        
    def selectvirtualspaces(self):
        """
        Selects all virtual spaces from the data base.
        @return: A CycleQueue instans that contains the virtual spaces. 
        """
        result = CycleQueue()
        query = "SELECT * FROM virtualspaces"
        self.__cursor.execute(query)
        for vid, name, host, port, size in self.__cursor.fetchall() :
            result.append(VirtualSpace(vid, name, host, size, port))
        return result

    def updatevirtualspace(self, vid, name, host, port, size):
        """
        Updates the virtual space's data.
        @param id: Virtual space's id.
        @param name: Virtual space's name.
        @param host: Virtual space's ip address or host name
        @param port: Virtual space's listening port
        @param size: Virtual space's capacity    
        """
        query = """UPDATE virtualspaces SET label = '%s', host = '%s',
        port = %d, size = %d WHERE vsid = %d"""
        
        self.__cursor.execute(query % (name, host, port, size, vid))
        self.__conn.commit()
        
    def addgroup(self, group, uid):
        """
        Add a new working group
        @param group: The new group's name
        @param uid: Owner's ID
        @return: The new group's ID
        """
        query = "INSERT INTO groups (name,owner) VALUES (%s,%s)"
        self.__cursor.execute(query, (group, uid))
        query = "SELECT gid FROM groups WHERE name = '%s'" % group
        self.__cursor.execute(query)
        gid = self.__cursor.fetchone()[0]
        self.__conn.commit()
        return gid
        
    def delgroup(self, gid):
        """
        Deletes a group.
        @param gid: The working group's id that will be destroyed. 
        """
        query = "DELETE FROM groups WHERE gid = %s"
        self.__cursor.execute(query,(gid,))
        self.__conn.commit()
        
    def adduser2group(self, uid, gid):
        """
        Adds a user to the given group
        @param uid: User id
        @param gid: Group id
        """
        query = "INSERT INTO membership (uid,gid) VALUES(%s,%s)"
        self.__cursor.execute( query, (uid, gid) )
        self.__conn.commit()
        
    def addservice(self, name, description = "" ):
        """
        Add a new service to the system
        @param name: Service's name
        @param description: Service's description.  
        """
        query = "INSERT INTO services (name,description) VALUES(%s,%s)"
        self.__cursor.execute(query, (name, description))
        self.__conn.commit()
        sid = self.query("SELECT last_value FROM services_sid_seq")[0][0]
        return sid


    def bringservice2user(self, usr, sid):
        """
        Brings a service to the given user
        @param usr: User id
        @param sid: Service id
        """
        query = "INSERT INTO usr2srv (usr,service) VALUES (%s,%s)"
        self.__cursor.execute(query, (usr, sid))
        self.__conn.commit()

    def disableservice(self, sid):
        """
        Suspend a service
        @param sid: Service id
        """
        query = "UPDATE services SET available = False WHERE sid = %d" % sid
        self.__cursor.execute(query)
        self.__conn.commit()
        

    def storefile(self, name, fhash, service, owner, gid, size, host ): 
        """
        Records a file into the database
        @param name:  String. File's name.
        @param fhash:  String. File's body's hash.
        @param service: String. Storage service
        @param owner: Integer. Owner's user id.
        @param gid:   Integer. Owner's group id.
        @param size:  Integer. File's size (in bytes)
        @param host:  Integer. Virtual space where the file will be processed.
        @return: A touple that contains the current file's version and the
        register's id.
        """
        fid = self.query("SELECT last_value FROM virtualspaces_vsid_seq")[0][0]
        
        self.__cursor.execute(
            "SELECT version FROM files WHERE name = '%s' AND topversion = True"
            % name)
        result = self.__cursor.fetchone()
        if not result == None :
            version = result[0] + 1
        else:
            version = 1
            
        self.__cursor.execute(
            """UPDATE files SET topversion = False
            WHERE name = '%s' AND topversion = True""" % name)
        
        query = """INSERT INTO files (name,hash,service,owner,gid,size,version,host)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
        ffile = (name, fhash, service, owner, gid, size, version, host)
        self.__cursor.execute(query, ffile)
        self.__conn.commit()
        # print "U %25s - revision %5d" % (name,version)
        return fid, version

    def selectfile(self, fid, uid):
        """
        @param fid:
        @param uid: 
        """
        raise NotImplementedError

    def selectuserfiles(self, uid):
        """
        Search the file list of the given user
        @param uid: The user id
        @return A list with the user's files
        """
        
        files = []
        query = """SELECT fid,name,size,version,createdon FROM FILES
        WHERE owner = %d AND topversion = True ORDER BY name""" % uid
        self.__cursor.execute(query)
        
        for (fid, name, size, ver, dte) in self.__cursor.fetchall():            
            files.append(SADFile(fid, name, size, ver, dte))
            
        return files

    def storefragment(self, fname, ffile, pos, fhash, size, host):
        
        """
        Records a fragment into the database.
        @param fname: String.  Fragment's file name.
        @param ffile: Integer. Fragment's file id.
        @param pos:   Integer. Fragment's position in the file.
        @param hash:  String.  Fragment's checksum
        @param size:  Integer. Fragment's size.
        @param host:  String.  Host id where the fragment will be stored. 
        
        @return: The Fragment's id.   
        """
        fid = self.query("SELECT last_value FROM fragments_fid_seq")[0][0]
        query = """INSERT INTO fragments (fname, file,pos,hash,size,host)
        VALUES(%s,%s,%s,%s,%s,%s)
        """
        fragment = (fname, ffile, pos, fhash, size, host)
        self.__cursor.execute(query, fragment)
        self.__conn.commit()
        
        return fid

    def storeblock(self, fname, fragment, btype, pos, fhash, host, size):
        """
        Records a Block into the database.

        @param fname:    String.  Block's file name.
        @param fragment: Integer. Block's fragment id.
        @param btype:    String.  Represents the block's type.
        @param pos:      Integer. Block's position in the fragment
        @param hash:     String.  Block's checksum
        @param host:     Integer. Host id where the IDA will be stored. 
        @param size:     Integer. Block's size.
        
        @return: The Block's id.   
        """
        bid = self.query("SELECT last_value FROM blocks_bid_seq")[0][0]
        query = """INSERT INTO blocks (fname, fragment,btype,pos,hash,host,size)
        VALUES(%s,%s,%s,%s,%s,%s,%s)
        """
        block = (fname, fragment, btype, pos, fhash, host, size)
        self.__cursor.execute(query, block)
        self.__conn.commit()
        
        return bid

    def droptable(self, table):
        """
        Drops a given table.
        @param table: Table's name to drop. 
        """
        self.__cursor.execute("DROP TABLE IF EXISTS %s CASCADE" % table)
        self.__conn.commit()

    def query(self, qry):
        """
        Method used for execute a query string in the database server.
        @param qry: String that contains the query
        @return: The query's result
        """
        res = None
        self.__cursor.execute(qry)
        try:
            res = self.__cursor.fetchall()
        except psycopg2.Error, err:
            del err
        self.__conn.commit()
        return res


