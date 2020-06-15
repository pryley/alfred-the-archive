#!/usr/bin/python
# encoding: utf-8

from Plist import Plist
import datetime
import json
import os
import sys
import time

class Items(object):

    def __init__(self):
        self.item = {}
        self.items = []
        self.mods = {}

    def __defineIcon(self, path, m_type=""):
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
            the_icon = self.__defineIcon(icon_path, icon_type)
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
        self.setKeyValue("icon", self.__defineIcon(m_path, m_type))

    def setItem(self, **kwargs):
        for key, value in kwargs.items():
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
        reload(sys)
        sys.setdefaultencoding('utf-8')
        try:
            return sys.argv[i].encode('utf-8')
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
    def getDateStr(float_time, fmt='%d %b, %Y'):
        return time.strftime(fmt, time.gmtime(float_time))

    @staticmethod
    def getEnv(var):
        return os.getenv(var) if os.getenv(var) is not None else str()

    @staticmethod
    def getTodayDate(fmt="%d.%m.%Y"):
        default_date_format = os.getenv('default_date_format')
        date_format = fmt if default_date_format == str() else default_date_format
        now = datetime.datetime.now()
        return now.strftime(date_format)

    @staticmethod
    def getZettelId():
        default_zettel_id_format = os.getenv('default_zettel_id_format');
        zettel_id_format = "%Y%m%d%H%M" if default_zettel_id_format == str() else default_zettel_id_format
        now = datetime.datetime.now()
        return now.strftime(zettel_id_format)

    @staticmethod
    def log(message):
        sys.stderr.write('{0}\n'.format(message))

    @staticmethod
    def settings(key, fallback=str()):
        bundle_id=os.getenv('the_archive_bundle_id')
        team_id=os.getenv('the_archive_team_id')
        plist=os.path.expanduser("~/Library/Group Containers/{0}.{1}.prefs/Library/Preferences/{0}.{1}.prefs.plist".format(team_id, bundle_id))
        if os.path.exists(plist):
            data = Plist().readPlist(plist)
            try:
                return data[key]
            except KeyError:
                sys.stderr.write(u"Warning: Cannot get the application setting: {0} ".format(key))
                return fallback
        sys.stderr.write("Error: Cannot find the application settings, please verify the_archive_bundle_id.")
        sys.exit(0)

    @staticmethod
    def strJoin(*args):
        return str().join(args)

    @staticmethod
    def strReplace(text, replace_map, lowercase=True):
        for k in replace_map.keys():
            text = text.replace(k, replace_map[k])
        return text.lower() if lowercase else text
