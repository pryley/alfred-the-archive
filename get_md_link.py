#!/usr/bin/env python
# encoding: utf-8

from Alfred import Tools
from Notes import Search
from urllib import pathname2url
import os
import sys

query = Tools.getArgv(1)
title = Search().getNoteTitle(query)
filename = pathname2url(os.path.basename(query))
output = '[' + title + '](' + filename + ')'

sys.stdout.write(output)
