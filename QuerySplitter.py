#!/usr/bin/python
# encoding: utf-8

class QuerySplitter(object):

    def __init__(self, query):
        self.tags = str()
        self.title = str()
        self.zettel_id = str()
        self.__split(query)

    def __isZettelId(self, text):
        zettel_id = str(text)
        return True if len(zettel_id) == 12 and zettel_id.isdigit() else False

    def __split(self, query):
        parts = query.split(' ')
        title_list = list()
        tag_list = list()
        for part in parts:
            if str(part).startswith('#'):
                tag_list.append(part)
            elif self.__isZettelId(part) and self.zettel_id == str():
                self.zettel_id = part
            else:
                title_list.append(part)
        self.title = ' '.join(title_list)
        self.tags = ' '.join(tag_list)
