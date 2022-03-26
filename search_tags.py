#!/usr/bin/env python3
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
    for tag, counter in list(tag_results.items()):
        items.setItem(
            arg=tag, # we cannot yet send a hash character with `thearchive://match/{query}`
            subtitle="{0} Hit(s), (\u2318 Paste Into Frontmost Application)".format(counter),
            title=tag,
            valid=True,
        )
        items.setIcon('icons/hashtag.png', 'image')
        items.addMod(
            arg="#{0} ".format(tag),
            icon_path='icons/paste.png',
            icon_type='image',
            key='cmd',
            subtitle='Paste this tag into the frontmost application',
        )
        items.addItem()
else:
    items.setItem(
        subtitle="No Tags matches search term",
        title="No Tags found!",
        valid=False,
    )
    items.addItem()

items.write()
