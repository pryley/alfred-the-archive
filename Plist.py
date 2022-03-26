#!/usr/bin/env python3
# encoding: utf-8

import plistlib

class Plist:

    def __init__(self):
        self.info = self.readPlist('info.plist')

    def deleteVariable(self, variable):
        try:
            del self.info['variables'][variable]
            self.writePlist(self.info, 'info.plist')
        except KeyError:
            pass

    def getConfig(self):
        return self.info['variables']

    def getVariable(self, variable):
        try:
            return self.info['variables'][variable]
        except KeyError:
            pass

    @staticmethod
    def readPlist(filepath):
        with open(filepath, 'rb') as fp:
            plistData = plistlib.load(fp)
        return plistData

    def setVariable(self, variable, value):
        self.info['variables'][variable] = value
        self.writePlist(self.info, 'info.plist')

    @staticmethod
    def writePlist(dataObject, filepath):
        with open(filepath, 'wb') as fp:
            plistlib.dump(dataObject, fp)
