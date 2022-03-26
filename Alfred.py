#!/usr/bin/env python3
# encoding: utf-8

from datetime import datetime, timedelta
from Plist import Plist
import json
import os
import re
import sys
import time
import urllib.request, urllib.error, urllib.parse

class Items(object):

    def __init__(self):
        self.item = {}
        self.items = []
        self.mods = {}

    def _defineIcon(self, path, m_type=""):
        icon = {}
        if m_type != "":
            icon.update({"type": m_type})
        icon.update({"path": path})
        return icon

    def addItem(self):
        self.addModsToItem()
        self.items.append(self.item)
        self.item = {}
        self.mods = {}

    def addMod(self, key, arg, subtitle, valid=True, icon_path="", icon_type=""):
        valid_keys = {"alt", "cmd", "shift", "ctrl", "fn", "cmd+alt"}
        if key not in valid_keys:
            raise ValueError("Key must be in: %s" % valid_keys)
        mod = {}
        mod.update({"arg": arg})
        mod.update({"subtitle": subtitle})
        mod.update({"valid": valid})
        if icon_path != "":
            the_icon = self._defineIcon(icon_path, icon_type)
            mod.update({"icon": the_icon})
        self.mods.update({key: mod})

    def addModsToItem(self):
        if bool(self.mods):
            self.setKeyValue("mods", self.mods)
        self.mods = dict()

    def getItem(self, d_type=""):
        if d_type == "":
            return self.item
        else:
            return json.dumps(self.item, indent=4)

    def getItems(self, response_type="json"):
        valid_keys = {"json", "dict"}
        if response_type not in valid_keys:
            raise ValueError("Type must be in: %s" % valid_keys)
        the_items = dict()
        the_items.update({"items": self.items})
        if response_type == "dict":
            return the_items
        elif response_type == "json":
            return json.dumps(the_items, indent=4)

    def setIcon(self, m_path, m_type=""):
        self.setKeyValue("icon", self._defineIcon(m_path, m_type))

    def setItem(self, **kwargs):
        for key, value in list(kwargs.items()):
            self.setKeyValue(key, value)

    def setKeyValue(self, key, value):
        self.item.update({key: value})

    def updateItem(self, id, key, value):
        dict_item = self.items[id]
        kv = dict_item[key]
        dict_item[key] = kv + value
        self.items[id] = dict_item

    def write(self, response_type='json'):
        output = self.getItems(response_type=response_type)
        sys.stdout.write(output)

class Tools(object):

    @staticmethod
    def chop(string, suffix):
        if string.endswith(suffix):
            return string[:-len(suffix)]
        return string

    @staticmethod
    def getArgv(i):
        try:
            return sys.argv[i]
        except IndexError:
            return str()
            pass

    @staticmethod
    def getDataDir():
        data_dir = os.getenv('alfred_workflow_data')
        if not(os.path.isdir(data_dir)):
            os.mkdir(data_dir)
        return data_dir

    @staticmethod
    def getDateStr(float_time, fmt='%Y-%m-%d'):
        return time.strftime(fmt, time.gmtime(float_time))

    @staticmethod
    def getEnv(var):
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def getNotesPath():
        archive_url = Tools.settings('archiveURL')
        path = urllib.parse.unquote(archive_url[len("file://"):])
        return path

    @staticmethod
    def getTodayDate(fmt="%d.%m.%Y"):
        default_date_format = os.getenv('default_date_format')
        date_format = fmt if default_date_format == str() else default_date_format
        now = datetime.now()
        return now.strftime(date_format)

    @staticmethod
    def getZettelId():
        default_zettel_id_format = os.getenv('default_zettel_id_format');
        zettel_id_format = "%Y%m%d%H%M" if default_zettel_id_format == str() else default_zettel_id_format
        now = datetime.now()
        zettel_id = now.strftime(zettel_id_format)
        if zettel_id.isdigit():
            path = Tools.getNotesPath()
            while Tools.zettelIdExists(path, zettel_id):
                zettel_id_date = datetime.strptime(zettel_id, zettel_id_format)
                new_zettel_id_date = zettel_id_date + timedelta(minutes=1)
                zettel_id = new_zettel_id_date.strftime(zettel_id_format)
        return zettel_id;

    @staticmethod
    def increment(file_name):
        increment = 1
        matches = re.search(r' \d+$', file_name)
        if matches:
            start, end = matches.span()
            increment = str(int(matches.group())+1) + file_name[end:]
            file_name = file_name[:max(end-len(increment), start)].rstrip()
        new_file_name = "{0} {1}".format(file_name, increment)
        return new_file_name

    @staticmethod
    def log(message):
        sys.stderr.write('{0}\n'.format(message))

    @staticmethod
    def normalize(value):
        if str(value).lower() in ("yes", "y", "tru", "true", "1"): return "True"
        if str(value).lower() in ("no",  "n", "fal", "fals", "false", "0"): return "False"
        return value

    @staticmethod
    def settings(key, fallback=str()):
        bundle_id=os.getenv('the_archive_bundle_id')
        team_id=os.getenv('the_archive_team_id')
        plist=os.path.expanduser("~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
        if os.path.exists(plist):
            data = Plist().readPlist(plist)
            for k, val in data.items():
                if key == k:
                    return val
            return fallback
        sys.stderr.write("Error: Cannot find the application settings, please verify the_archive_bundle_id.")
        sys.exit(0)

    @staticmethod
    def strJoin(*args):
        return str().join(args)

    @staticmethod
    def strReplace(text, replace_map, lowercase=True):
        for k in list(replace_map.keys()):
            text = text.replace(k, replace_map[k])
        return text.lower() if lowercase else text

    @staticmethod
    def zettelIdExists(path, zettelId):
        err = 0
        file_list = list()
        try:
            file_list = os.listdir(path)
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            for filename in file_list:
                if filename.startswith(zettelId):
                    return True
        return False
