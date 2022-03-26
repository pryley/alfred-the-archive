#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Items, Tools
from Notes import Search
from urllib.request import pathname2url
import os

items = Items()
query = Tools.getEnv("path_query2")
search = Search()
note_path = Tools.getEnv("path_query1")
note_title = search.getNoteTitle(note_path)
note_link_title = search.getNoteLinkTitle(note_path)
filename = pathname2url(os.path.basename(note_path))
back_query = "<EMPTY>" if not query else query

actions = [
    {
        "arg": "back|>{0}".format(query),
        "icon": "icons/back.png",
        "subtitle": "Back to Search with query: {0}".format(back_query),
        "title": "Back",
    },
    {
        "arg": "markdown_link|>[{0}]({1})".format(note_link_title, filename),
        "icon": "icons/link.png",
        "subtitle": "Copy a Markdown Link for \"{0}\" to the Clipboard".format(note_title),
        "title": "Markdown Link",
    },
    {
        "arg": "wiki_link|>[[{0}]]".format(note_link_title),
        "icon": "icons/link.png",
        "subtitle": "Copy a Wiki Link for \"{0}\" to the Clipboard".format(note_title),
        "title": "Wiki Link",
    },
    {
        "arg": "editor|>{0}".format(note_path),
        "icon": "icons/editor.png",
        "subtitle": "Open \"{0}\" with the default editor".format(os.path.basename(note_path)),
        "title": "External Editor",
    },
    {
        "arg": "delete|>{0}".format(note_path),
        "icon": "icons/delete.png",
        "subtitle": "Delete \"{0}\"".format(os.path.basename(note_path)),
        "title": "Delete Note",
    },
]

for a in actions:
    items.setItem(
        arg=a.get("arg"),
        subtitle=a.get("subtitle"),
        title=a.get("title"),
    )
    items.setIcon(a.get("icon"), "image")
    items.addItem()

items.write()
