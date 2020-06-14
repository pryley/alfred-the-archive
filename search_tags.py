#!/usr/bin/python
# encoding: utf-8

from Alfred import Items, Tools
from Notes import Search

items = Items()
query = Tools.getArgv(1)
search = Search()

if query is str():
    tag_results = search.tags(query, 'tag', reverse=False)
else:
    tag_results = search.tags(query, 'count', reverse=True)

if bool(tag_results):
    for tag, counter in tag_results.items():
        items.setItem(
            arg = tag, # we cannot yet send a hash character with `thearchive://match/{query}`
            subtitle = u"{0} Hit(s), (\u2318 to paste tag into frontmost app)".format(counter),
            title = tag,
            valid = True,
        )
        items.setIcon('icons/hashtag.png', 'image')
        items.addMod(
            arg = u"#{0} ".format(tag),
            icon_path = 'icons/paste.png',
            icon_type = 'image',
            key = 'cmd',
            subtitle = 'Paste Tag into frontmost app',
        )
        items.addItem()
else:
    items.setItem(
        title = "No Tags found!",
        subtitle = "No Tags matches search term",
        valid = False
    )
    items.addItem()

items.write()
