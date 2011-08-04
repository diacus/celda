#!/usr/bin/python
# -*- coding:utf-8 -*-

from SimpleXMLRPCServer import SimpleXMLRPCServer
from data.message import Message
# from server.sadproxy import Proxy, SADBroker
from server.sadserver import Proxy, ProxyHandler
from lib.config import SADConfig

def main():

	confpath = "/etc/celda/celdad.conf"
	conf = SADConfig()
	conf.setConfigfile(confpath)
	conf.loadConf()

	handler = ProxyHandler()
	proxy = Proxy()
	proxy.setHandler(handler)
	proxy.start()

if __name__ == "__main__":
	main()

