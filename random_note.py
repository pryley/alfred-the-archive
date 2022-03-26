#!/usr/bin/env python3
# encoding: utf-8

import random
import sys
from Notes import Search

search = Search()
sorted_file_list = search.getFilesListSorted()
file = random.choice(sorted_file_list)
output = search.getNoteFilename(file['path'])

sys.stdout.write(output)
