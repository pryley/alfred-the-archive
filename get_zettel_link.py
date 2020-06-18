#!/usr/bin/env python
# encoding: utf-8

from Alfred import Tools
from Notes import Search
import sys

query = Tools.getArgv(1)
title = Search().getNoteTitle(query).strip()
output = '[[' + title + ']]'

sys.stdout.write(output)
