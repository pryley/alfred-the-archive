#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
from shutil import copy2
import os
import re
import sys
import urllib.request, urllib.parse, urllib.error

def copyFile(source, target_dir):
    file_name = str()
    if os.path.isfile(source):
        file_name = os.path.basename(source)
        valid_file_name = re.sub('[^\w_.)(-]', '_', file_name)
        destination = os.path.join(target_dir, valid_file_name)
        copy2(source, destination)
        file_name = valid_file_name
    else:
        raise ValueError
    return os.path.join(target_dir, file_name)

def getMediaFolder():
    notes_path = Tools.getNotesPath()
    media_dir = Tools.settings('resourcesSubfolder', 'media')
    media_path = os.path.join(notes_path, media_dir)
    if not(os.path.exists(media_path)):
        os.mkdir(media_path)
    return media_path

source_file = Tools.getArgv(1)
target_dir = getMediaFolder()
image_file = copyFile(source_file, target_dir)
file_url = urllib.request.pathname2url(image_file)
link = '![{0}]({1})'.format(os.path.basename(image_file), file_url)

sys.stdout.write(link)
