#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
from Markdown import Markdown
from Notes import Search
from urllib.request import pathname2url
import os
import sys

search = Search()
ext = search.getDefaultExtension()
path = Tools.getNotesPath()
query = Tools.getArgv(1)

markdown = Markdown(query)
today_time = Tools.getTodayDate(fmt="%Y-%m-%d %H-%M")
content = markdown.getMarkdownContent()
file_name = markdown.parseFilename(markdown.getTitle())
if file_name == str():
    file_name = Tools.strJoin('WebClip from ', today_time)
filepath = os.path.join(path, "{0}{1}".format(file_name, ext))
markdown.writeMarkdown(content, filepath)
title = pathname2url(search.getNoteTitle(filepath))

sys.stdout.write(title)
