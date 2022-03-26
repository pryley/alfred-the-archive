#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
import html.parser
import os
import re
import urllib.request, urllib.error, urllib.parse

class Markdown(object):

    PANDOC = '/usr/local/bin/pandoc -f html-native_divs-native_spans -t gfm --strip-comments --atx-headers '

    def __init__(self, url):
        self.url = url
        self.html = self._fetchHtml()
        self.md = self._fetchMd()

    def _fetchHtml(self):
        try:
            r = urllib.request.urlopen(self.url)
            response = r.read()
        except:
            response = "<html><body><a href=\"" + self.url + "\">" + self.url + "</a></body></html>"
            pass
        return response

    def _fetchMd(self):
        try:
            cmd = '{0} {1}'.format(self.PANDOC, self.url)
            md = os.popen(cmd)
            resp = md.read()
        except:
            resp = "[{0}]({0})".format(self.url)
            pass
        return resp

    @staticmethod
    def _htmlDecode(string):
        string = urllib.parse.unquote(string)
        # return string
        return html.parser.HTMLParser().unescape(string)

    def _markdownHeader(self):
        return "---\n" \
               "Title: {title}\n" \
               "Created: {date}\n" \
               "Tags: #WebClip\n" \
               "Url: {url}\n" \
               "---\n".format(date=Tools.getTodayDate(), url=self.getMdUrl(), title=self.getTitle())

    def getHtml(self):
        return self.html

    def getMarkdownContent(self):
        out = self._markdownHeader()
        out += self.getMd()
        return out

    def getMd(self):
        return self.md

    def getMdUrl(self):
        page_url = "[{0}]({1})".format(self.getTitle(), self.getUrl())
        return page_url

    def getTitle(self):
        res = re.findall(r'<title>[\n\t\s]*(.+)[\n\t\s]*</title>', self.html, re.MULTILINE)
        return self._htmlDecode(''.join(res))

    def getUrl(self):
        return self.url

    def parseFilename(self, filename):
        to_replace = ['/', '\\', ':']
        tmp = filename.strip()
        for i in to_replace:
            tmp = tmp.replace(i, '-')
        return tmp

    def writeMarkdown(self, content, path):
        with open(path, "w+") as file:
            file.write(content)
