#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Items, Tools
from Notes import Search

items = Items()
query = Tools.getArgv(1)
search = Search()

tasks = search.tasks(query)

if len(tasks) > 0:
    for file in tasks:
        file_title = file['title'] if file['title'] != str() else search.getNoteFilename(file['path'])
        items.setItem(
            arg=file['path'],
            subtitle="\u2192 {0} (\u2318 Open in The Archive, \u2325 Open in Default Editor)".format(file['filename']),
            title=file['todo'],
            type='file',
            valid=True,
            variables={
                "todo": file['todo'],
                "todo_query": query,
                "todo_status": file['status'],
            },
        )
        items.addMod(
            arg=file['path'],
            icon_path="icons/the-archive.png",
            icon_type="image",
            key="cmd",
            subtitle="Open \"{0}\" in The Archive".format(file['filename']),
        )
        items.addMod(
            arg=file['path'],
            icon_path="icons/editor.png",
            icon_type="image",
            key="alt",
            subtitle="Open \"{0}\" in the default editor".format(file['filename']),
        )
        items.setIcon('icons/todo.png' if file['status'] == 'pending' else 'icons/done.png', 'image')
        items.addItem()
else:
    items.setItem(
        title="No tasks found!",
        subtitle="No task matches the search term",
        valid=False,
    )
    items.addItem()
items.write()
