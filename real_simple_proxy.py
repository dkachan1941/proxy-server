# -*- coding: utf-8 -*-

import socket
import urllib2
import re

def handleHtml(s_data):
   try:
      req = urllib2.Request(s_data[1])
      html=urllib2.urlopen(req).read()
      html_new = re.sub(r'(>.*\b([\w]{6}))(\b.*<(?!</script))', r"\1%s\3" % (u'\u2122'),html ,flags=re.U) # we modify content here
      if not isinstance(html_new, str):
          html_new = html_new.encode('utf-8')
   except (urllib2.URLError,urllib2.HTTPError) as e:
      html_new="<b> error occured: "+e.reason[1]+"</b>"
   return html_new

def handleProxy(conn):
   Request=conn.recv(4096) # receiving data from the socket
   s_data=Request.split()
   html = handleHtml(s_data)
   conn.send(html)
   print "Requested data:\n"+ Request

def main():
   port = 9090
   s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.bind(('',port))
   s.listen(1000)
   print 'Proxy server has launched at %d' % (port)
   while True:
      (conn, address)=s.accept()
      print address[0]+":"+str(address[1])+" connected!"
      handleProxy(conn)

if __name__ == '__main__':
    main()
