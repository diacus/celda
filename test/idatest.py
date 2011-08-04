#!/usr/bin/python
# -*- coding:utf-8 -*-

"""
File: idatest.py
Author: diacus
Description: Testing IDA
"""

import logging, os, shlex, subprocess
from client.sadclient import NodeClient
from data.stream      import BlockStream, FragmentStream
from lib.config       import SADConfig

def main():
    """docstring for main"""
    fname = "/home/diacus/Dropbox/src/celda/file/opensuse.pdf"
    fconf = "/etc/celda/celdad.conf"

    conf = SADConfig()
    conf.setconfigfile(fconf)
    conf.loadconf()

    dis, rec = conf.getidapath()
    path     = conf.getstoragepath()

    server = "http://192.168.86.99:4242"
    client = NodeClient(server)

    logging.basicConfig(
        format='%(asctime)s -- %(levelname)-8s %(message)s',
        filename="test.log",
        level=logging.DEBUG
    )

    fragment = FragmentStream(1, 0, "IDA")
    fragment.loadfromfile(fname)
