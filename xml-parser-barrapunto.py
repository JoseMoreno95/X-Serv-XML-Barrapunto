#!/usr/bin/python

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
from urllib.request import urlopen

class myContentHandler(ContentHandler):

    def __init__ (self):
        self.inItem = False
        self.inContent = False
        self.theContent = ""

    def startElement (self, name, attrs):
        if name == 'item':
            self.inItem = True
        elif self.inItem:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.inContent = True

    def endElement (self, name):
        if name == 'item':
            self.inItem = False
        elif self.inItem:
            if name == 'title':
                line = "Title: " + self.theContent + ".<br/>"
                # To avoid Unicode trouble
                htmlFile.write (line)
                self.inContent = False
                self.theContent = ""
            elif name == 'link':
                htmlFile.write (" Link: " + "<a href=" + self.theContent)
                htmlFile.write (">" + self.theContent + "</a><br/><br/>")
                self.inContent = False
                self.theContent = ""

    def characters (self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

if len(sys.argv)!=1:
    print ("Usage: python3 xml-parser-barrapunto.py > barrapunto.html")
    print ("Next: open barrapunto.html file in your navigator")
    sys.exit(1)

theParser = make_parser()
theHandler = myContentHandler()
theParser.setContentHandler(theHandler)

url = "http://barrapunto.com/index.rss"
url = urlopen(url)
rss = url.read().decode("utf-8")
url.close()
xmlFile = open('barrapunto.rss', 'w')
xmlFile.write(rss)
xmlFile.close()

htmlFile = open('barrapunto.html', 'w')
htmlFile.write("<meta http-equiv='Content-Type' content='text/html; charset=utf-8'/>")
htmlFile.write("<h1>Titulares y links de barrapunto.com</h1>")

xmlFile = open('barrapunto.rss', "r")
theParser.parse(xmlFile)
