#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Items, Tools
from Notes import Search

items = Items()
query = Tools.getArgv(1)
search = Search()
search_terms, search_type = search.getSearchConfig(query)

if len(search_terms) > 0:
    sorted_file_list = search.notes(search_terms, search_type)
else:
    sorted_file_list = search.getFilesListSorted()

for file in sorted_file_list:
    c_date = Tools.getDateStr(file['ctime'])
    m_date = Tools.getDateStr(file['mtime'])
    items.setItem(
        arg=file['path'],
        subtitle="Created: {0}, Modified: {1} (\u2318 Actions, \u2325 Paste Wiki Link, \u21E7 Quicklook)".format(c_date, m_date),
        title=file['title'],
        type="file",
    )
    items.addMod(
        arg="{0}|>{1}".format(file['path'], query),
        icon_path="icons/action.png",
        icon_type="image",
        key="cmd",
        subtitle="Enter Actions Menu for the Note...",
    )
    items.addMod(
        arg=file['title'],
        icon_path="icons/paste.png",
        icon_type="image",
        key="alt",
        subtitle="Paste wiki link into frontmost app",
    )
    items.addItem()

if len(items.getItems(response_type="dict")['items']) == 0:
    items.setItem(
        arg=query,
        subtitle="Create note with title \"{0}\"?".format(query),
        title="Nothing found...",
    )
    items.setIcon('icons/new.png', 'image')
    items.addItem()

items.write()
