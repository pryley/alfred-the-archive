#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
from Notes import Search
from urllib.request import pathname2url
import os
import sys

query = Tools.getArgv(1)
title = Search().getNoteTitle(query).strip()
filename = pathname2url(os.path.basename(query))
output = '[' + title + '](' + filename + ')'

sys.stdout.write(output)
