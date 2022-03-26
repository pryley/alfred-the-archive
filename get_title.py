#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
from Notes import Search
import sys

query = Tools.getArgv(1)
title = Search().getNoteTitle(query)

sys.stdout.write(title)
