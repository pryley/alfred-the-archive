#!/usr/bin/python
# encoding: utf-8

from __future__ import absolute_import, print_function
from Foundation import NSData
from Foundation import NSPropertyListMutableContainers
from Foundation import NSPropertyListSerialization
from Foundation import NSPropertyListXMLFormat_v1_0

class FoundationPlistException(Exception):
    """Basic exception for plist errors"""
    pass

class NSPropertyListSerializationException(FoundationPlistException):
    """Read/parse error for plists"""
    pass

class NSPropertyListWriteException(FoundationPlistException):
    """Write error for plists"""
    pass

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
        plistData = NSData.dataWithContentsOfFile_(filepath)
        dataObject, dummy_plistFormat, error = (
            NSPropertyListSerialization.propertyListFromData_mutabilityOption_format_errorDescription_(
                plistData, NSPropertyListMutableContainers, None, None
            )
        )
        if dataObject is None:
            if error:
                error = error.encode('ascii', 'ignore')
            else:
                error = "Unknown error"
            errmsg = "{0} in file {1}".format(error, filepath)
            raise NSPropertyListSerializationException(errmsg)
        else:
            return dataObject

    def setVariable(self, variable, value):
        self.info['variables'][variable] = value
        self.writePlist(self.info, 'info.plist')

    @staticmethod
    def writePlist(dataObject, filepath):
        plistData, error = (
            NSPropertyListSerialization.dataFromPropertyList_format_errorDescription_(
                dataObject, NSPropertyListXMLFormat_v1_0, None
            )
        )
        if plistData is None:
            if error:
                error = error.encode('ascii', 'ignore')
            else:
                error = "Unknown error"
            raise NSPropertyListSerializationException(error)
        else:
            if plistData.writeToFile_atomically_(filepath, True):
                return
            else:
                raise NSPropertyListWriteException("Failed to write plist data to {0}".format(filepath))
