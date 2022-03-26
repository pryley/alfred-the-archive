#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
import re
import sys

def replace(file, pattern, subst):
    file_handle = open(file, 'r')
    file_string = file_handle.read()
    file_handle.close()
    file_string = (re.sub(pattern, subst, file_string))
    file_handle = open(file, 'w')
    file_handle.write(file_string)
    file_handle.close()

path = Tools.getArgv(1)
todo = Tools.getEnv('todo')
status = Tools.getEnv('todo_status')
query = Tools.getEnv('todo_query')

old_val = ' ' if status == 'pending' else 'x'
new_val = ' ' if old_val == 'x' else 'x'

replace(path, "([-|\*] \[){0}(\] {1})".format(old_val, todo), "\\1{0}\\2".format(new_val))

sys.stdout.write(query)
