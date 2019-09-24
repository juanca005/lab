#!/usr/bin/python
# -*- coding: utf-8 -*-

#CLIENTE

from socket import *
s = socket(AF_INET,SOCK_STREAM)
s.connect(("www.python.org",80))
s.send("GET /index.html HTTP/1.0\n\n")
data = s.recv(10000)
s.close()