#!/usr/bin/python3

#
# Simple XML parser for YouTube XML channels
# César Borao Moratinos
#
# Based on "ytparser.py" code:
#
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# 2020
#
# The input is a valid channel ID. The parser produces a HTML document in standard output, with
# the list of videos on the channel
#

from urllib.error import URLError
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import urllib.request

videos = ""


class YTHandler(ContentHandler):

    def __init__(self):
        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = ""
        self.link = ""

    def startElement(self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')

    def endElement(self, name):
        global videos

        if name == 'entry':
            self.inEntry = False
            videos = videos \
                     + "    <li><a href='" + self.link + "'>" \
                     + self.title + "</a></li>\n"
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False

    def characters(self, chars):
        if self.inContent:
            self.content = self.content + chars


# Loading parser and driver
Parser = make_parser()
Parser.setContentHandler(YTHandler())

# --- Main prog
if __name__ == "__main__":

    PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h1>Youtube channel contents:</h1>
    <ul>
        {videos}
    </ul>
  </body>
</html>
"""

    if len(sys.argv) < 2:
        print("Usage: python youtube_parser.py <channel id>")
        print(" <channel id>: The unique ID of a youtube channel")
        sys.exit(1)

    # Reading the channel's xml file
    try:
        xmlFile = urllib.request.urlopen('https://www.youtube.com/feeds/videos.xml?channel_id=' + sys.argv[1])
        Parser.parse(xmlFile)
        page = PAGE.format(videos=videos)
        print(page)

    except URLError:
        print("Introduce a valid channel Id")
