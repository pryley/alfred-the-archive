#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Items, Tools
from Notes import Notes, Search

items = Items()
notes = Notes()
search = Search()
zettel_id = Tools.getZettelId()
query = Tools.getArgv(1)
query_alt = "{0} {1}".format(zettel_id, query)
zettel_action = "\u2318 Add Zettel ID"
paste_action = "\u2325 Paste clipboard"
quicklook_action = "\u21E7 Quicklook"

if notes.useZettelId():
    query_alt = query
    query = "{0} {1}".format(zettel_id, query_alt)
    zettel_action = "\u2318 Remove Zettel ID"

items.setItem(
    arg="{0}|>|>".format(query),
    subtitle="\"{0}\" ({1}, {2})".format(query, zettel_action, paste_action),
    title="Create note",
)
items.addMod(
    arg="{0}|>|>".format(query_alt),
    key="cmd",
    subtitle="\"{0}\" ({1})".format(query_alt, paste_action),
)
items.addMod(
    arg="{0}|>|>paste".format(query),
    icon_path="icons/new_from_clipboard.png",
    icon_type="image",
    key="alt",
    subtitle="\"{0}\" ({1})".format(query, zettel_action),
)
items.addMod(
    arg="{0}|>|>paste".format(query_alt),
    icon_path="icons/new_from_clipboard.png",
    icon_type="image",
    key="cmd+alt",
    subtitle="\"{0}\"".format(query_alt),
)
items.setIcon('icons/new.png', 'image')
items.addItem()

templates_list = search.templates()

if len(templates_list) > 0:
    for file in templates_list:
        items.setItem(
            arg="{0}|>{1}|>".format(query, file['path']),
            subtitle="\"{0}\" ({1}, {2}. {3})".format(query, zettel_action, paste_action, quicklook_action),
            title="Create note from template: {0}".format(file['filename']),
            type='file',
            quicklookurl=file['path'],
        )
        items.addMod(
            arg="{0}|>{1}|>".format(query_alt, file['path']),
            key="cmd",
            subtitle="\"{0}\" ({1})".format(query_alt, paste_action),
        )
        items.addMod(
            arg="{0}|>{1}|>paste".format(query, file['path']),
            icon_path="icons/paste.png",
            icon_type="image",
            key="alt",
            subtitle="\"{0}\" ({1})".format(query, zettel_action),
        )
        items.addMod(
            arg="{0}|>{1}|>paste".format(query_alt, file['path']),
            icon_path="icons/paste.png",
            icon_type="image",
            key="cmd+alt",
            subtitle="\"{0}\"".format(query_alt),
        )
        items.setIcon('icons/template.png', 'image')
        items.addItem()

items.write()
