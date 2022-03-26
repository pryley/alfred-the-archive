#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
from Notes import Search
import sys

query = Tools.getArgv(1)
title = Search().getNoteLinkTitle(query).strip()
output = '[[' + title + ']]'

sys.stdout.write(output)
