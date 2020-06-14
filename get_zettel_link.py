#!/usr/bin/python
# encoding: utf-8

from Alfred import Tools
from Notes import Search
import sys

query = Tools.getArgv(1)
title = Search().getNoteTitle(query)
output = '[[' + title + ']]'

sys.stdout.write(output)
