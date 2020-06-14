#!/usr/bin/python
# encoding: utf-8

from Alfred import Tools
import HTMLParser
import os
import re
import urllib2

class Markdown(object):

    PANDOC = '/usr/local/bin/pandoc -f html-native_divs-native_spans -t gfm --strip-comments --atx-headers '

    def __init__(self, url):
        self.url = url
        self.html = self.__fetchHtml()
        self.md = self.__fetchMd()

    def __fetchHtml(self):
        try:
            r = urllib2.urlopen(self.url)
            response = r.read().decode('utf-8')
        except:
            response = "<html><body><a href=\"" + self.url + "\">" + self.url + "</a></body></html>"
            pass
        return response

    def __fetchMd(self):
        try:
            cmd = '{0} {1}'.format(self.PANDOC, self.url)
            md = os.popen(cmd)
            resp = md.read()
        except:
            resp = "[{0}]({0})".format(self.url)
            pass
        return resp

    @staticmethod
    def __htmlDecode(string):
        string = urllib2.unquote(string)
        # return string
        return HTMLParser.HTMLParser().unescape(string).encode('utf-8')

    def __markdownHeader(self):
        today = Tools.getTodayDate(fmt="%d.%m.%Y")
        return "---\n" \
               "Title: {title}\n" \
               "Created: {date}\n" \
               "Tags: #WebClip\n" \
               "Url: {url}\n" \
               "---\n".format(date=today, url=self.getMdUrl(), title=self.getTitle())

    def getHtml(self):
        return self.html

    def getMarkdownContent(self):
        out = self.__markdownHeader()
        out += self.getMd()
        return out

    def getMd(self):
        return self.md.decode('utf-8')

    def getMdUrl(self):
        page_url = u"[{0}]({1})".format(self.getTitle(), self.getUrl())
        return page_url

    def getTitle(self):
        res = re.findall(r'<title>[\n\t\s]*(.+)[\n\t\s]*</title>', self.html, re.MULTILINE)
        return self.__htmlDecode(''.join(res))

    def getUrl(self):
        return self.url.decode('utf-8')

    def parseFilename(self, filename):
        to_replace = ['/', '\\', ':', '|']
        tmp = filename.decode('utf-8').strip()
        for i in to_replace:
            tmp = tmp.replace(i, '-')
        return tmp.encode('utf-8')

    def writeMarkdown(self, content, path):
        with open(path, "w+") as file:
            file.write(content.encode('utf-8'))
