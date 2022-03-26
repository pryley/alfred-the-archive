#!/usr/bin/env python3
# encoding: utf-8

from Alfred import Tools
from collections import Counter, OrderedDict
from QuerySplitter import QuerySplitter
from unicodedata import normalize
import os
import re
import sys

class Notes(object):

    CHAR_REPLACEMENT_MAP = {
        '/': '-',
        '\\': '-',
        ':': '-',
        ',': '',
        '#': '-'
    }

    FALLBACK_CONTENT = "{tags}\n\n{content}"

    REPL_MAP = {
        '[': '',
        ']': ' ',
        '(': '',
        ')': ' ',
        '\n': ' ',
        '*': ' ',
        ',': ' ',
        '.': ' ',
        '-': ' ',
        ':': ' ',
        '?': ' ',
        '!': ' '
    }

    UMLAUT_REPL_MAP = {
        '\xc3\x84': 'Ae', # Ä
        '\xc3\x88': 'e',  # È
        '\xc3\x96': 'Oe', # Ö
        '\xc3\x9c': 'Ue', # Ü
        '\xc3\x9f': 'ss', # ß
        '\xc3\xa4': 'ae', # ä
        '\xc3\xa5': 'as', # å
        '\xc3\xb6': 'oe', # ö
        '\xc3\xbc': 'ue', # ü
    }

    def __init__(self):
        self.allowed_extensions = self._getAllowedExtensions()
        self.default_date_format = os.getenv('default_date_format')
        self.default_extension = self._getDefaultExtension()
        self.exact_match = True if os.getenv('exact_match') == 'True' else False
        self.path = Tools.getNotesPath()
        self.prefer_filename_to_title = True if os.getenv('prefer_filename_to_title') == 'True' else False
        self.prefer_zettel_id_links = True if os.getenv('prefer_zettel_id_links') == 'True' else False
        self.search_content = True if os.getenv('search_content') == 'True' else False
        self.search_yaml_tags_only = True if os.getenv('search_yaml_tags_only') == 'True' else False
        self.template_tag = os.getenv('template_tag')
        self.use_zettel_id = Tools.settings('isUsingIDForNewFiles', True)
        self.use_zettel_id_in_title = True if os.getenv('use_zettel_id_in_title') == 'True' else False

    @staticmethod
    def _getAllowedExtensions():
        extensions = Tools.settings('fileExtensions', ['md','txt'])
        allowed_extensions = [Notes.normalizeExt(ext) for ext in extensions]
        return tuple(allowed_extensions)

    @staticmethod
    def _getDefaultExtension():
        ext = Tools.settings('fileExtension', 'md')
        return Notes.normalizeExt(ext)

    def getAllowedExtensions(self):
        return self.allowed_extensions

    def getDefaultExtension(self):
        return self.default_extension

    @staticmethod
    def normalizeExt(ext):
        return ext if '.' in ext else str().join(['.', ext])

    def useZettelId(self):
        return self.use_zettel_id

class Note(Notes):

    def __init__(self, title, template_path=str(), tags=str(), content=str(), zettel_id=str()):
        super(Note, self).__init__()
        self.tags = tags
        self.content = content
        self.title = "{0} {1}".format(zettel_id, title).strip() if self.use_zettel_id_in_title else title
        self.zettel_id = zettel_id
        self.note_path = self.getTargetFilePath(self.normalizeFilename("{0} {1}".format(zettel_id, title)))
        self.template_path = template_path

    def createNote(self):
        try:
            with open(self.note_path, "w+") as f:
                file_content = self.readTemplate(
                    content=self.content,
                    date=Tools.getTodayDate(),
                    tags=self.tags,
                    title=self.title,
                    zettel_id=self.zettel_id,
                )
                f.write(file_content)
            return self.note_path
        except Exception as e:
            sys.stderr.write(e)

    def getTargetFilePath(self, file_name):
        file_name = file_name.rstrip().lstrip()
        file_path = os.path.join(self.path, file_name + self.default_extension)
        if os.path.isfile(file_path):
            new_file_name = Tools.increment(file_name)
            return self.getTargetFilePath(new_file_name)
        file_path = os.path.join(self.path, file_name + self.default_extension)
        return file_path

    def normalizeFilename(self, filename):
        self.CHAR_REPLACEMENT_MAP.update(self.UMLAUT_REPL_MAP)
        return Tools.strReplace(filename, self.CHAR_REPLACEMENT_MAP, lowercase=False)

    def readTemplate(self, **kwargs):
        if '#' not in self.template_tag or self.template_tag == str():
            self.template_tag = '#template'
        if os.path.exists(self.template_path):
            with open(self.template_path, "r") as file:
                content = file.read()
        else:
            content = self.FALLBACK_CONTENT
        content = content.replace(self.template_tag, '')
        for k, v in list(kwargs.items()):
            content = content.replace('{' + k + '}', v)
        return content

class Search(Notes):

    def __init__(self):
        super(Search, self).__init__()

    def _getFileContent(self, file_path):
        if file_path.endswith(self.allowed_extensions):
            with open(file_path, 'r') as c:
                content = c.read()
        else:
            content = str()
        return normalize('NFD', content)

    def _match(self, search_terms, content, operator):
        content = content.lower()
        content = Tools.strReplace(content, self.REPL_MAP)
        word_list = content.split(' ')
        word_list = [Tools.chop(w, '#') for w in word_list]
        search_terms = [s.lower() for s in search_terms]
        match = False
        matches = list()
        for st in search_terms:
            search_str = st.replace('*', str())
            # search if search term contains a whitespace
            if ' ' in st:
                regexp = re.compile(r'({0})'.format(st), re.I)
                match = True if len(re.findall(regexp, content)) > 0 else False
            # search if wildcard search in the end
            elif st.endswith('*'):
                match_list = [x for x in word_list if x.startswith(search_str)]
                match = True if len(match_list) > 0 else False
            # search if wildcard search in front
            elif st.startswith('*'):
                match_list = [x for x in word_list if x.endswith(search_str)]
                match = True if len(match_list) > 0 else False
            # search if exact match is true
            elif self.exact_match:
                match = True if search_str in word_list else False
            # search with exact match is false
            else:
                match = True if search_str in str(word_list) else False
            matches.append(match)
        match = all(matches) if operator == 'AND' else any(matches)
        return match

    def getFileMeta(self, path, item):
        file_stats = os.stat(path)
        switch = {
            'ctime': file_stats.st_birthtime,
            'mtime': file_stats.st_mtime,
            'size': file_stats.st_size
        }
        return switch[item]

    def getFilesListSorted(self, reverse=True):
        err = 0
        file_list = list()
        try:
            file_list = os.listdir(self.path)
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            seq = list()
            for filename in file_list:
                file_path = os.path.join(self.path, filename)
                not (filename.startswith('.')) and filename.endswith(self.allowed_extensions) and seq.append({
                    'filename': filename,
                    'path': file_path,
                    'title': self.getNoteTitle(file_path),
                    'ctime': self.getFileMeta(file_path, 'ctime'),
                    'mtime': self.getFileMeta(file_path, 'mtime'),
                    'size': self.getFileMeta(file_path, 'size')
                })
            sorted_file_list = sorted(seq, key=lambda k: k['mtime'], reverse=reverse)
            return sorted_file_list

    def getNoteFilename(self, file_path):
        file_basename = os.path.basename(file_path)
        return file_basename.rsplit('.', 1)[0]

    def getNoteLinkTitle(self, path):
        title = self.getNoteTitle(path)
        if self.prefer_zettel_id_links:
            qs = QuerySplitter(title)
            if qs.zettel_id:
                title = qs.zettel_id
        return title

    def getNoteTitle(self, path):
        content = self._getFileContent(path)
        title = self.getNoteFilename(path)
        if not self.prefer_filename_to_title:
            obj = re.search(r'^#{1}\s{1}(.*)', content, re.MULTILINE | re.UNICODE)
            if obj is not None:
                title = obj.group(1) if len(re.findall(r'\{.*\}', obj.group(1))) == 0 else title
        return title

    def getSearchConfig(self, query):
        if '&' in list(query):
            search_terms = query.split('&')
            search_type = 'and'
        elif '|' in list(query):
            search_terms = query.split('|')
            search_type = 'or'
        elif query == str():
            search_terms = list()
            search_type = 'or'
        else:
            search_terms = [query]
            search_type = 'or'
        return search_terms, search_type

    def getTemplateTag(self):
        tt = Tools.getEnv('template_tag')
        if '#' not in tt or tt == str():
            tt = '#template'
        return tt

    def isNoteTagged(self, file_path, tag):
        match = False
        with open(file_path, 'r') as c:
            lines = c.readlines()[0:10]
        for l in lines:
            match_obj = re.search(tag, l, re.IGNORECASE)
            if match_obj:
                match = True
                break
        return match

    def notes(self, search_terms, search_type):
        file_list = self.getFilesListSorted()
        search_terms = [normalize('NFD', s) for s in search_terms]
        new_list = list()
        if file_list is not None:
            for file in file_list:
                title = self.getNoteTitle(file['path'])
                if (search_type == 'and' and self._match(search_terms, title, 'AND')) or (search_type == 'or' and self._match(search_terms, title, 'OR')):
                    new_list.append(file)
                elif self.search_content:
                    content = self._getFileContent(file['path'])
                    if content != str() and (search_type == 'and' and self._match(search_terms, content, 'AND')) or (search_type == 'or' and self._match(search_terms, content, 'OR')):
                        new_list.append(file)
        return new_list

    def tags(self, tag, sort_by='tag', reverse=False):
        i = {'tag': 0, 'count': 1}
        tag = normalize('NFD', tag)
        matches = list()
        sorted_file_list = self.getFilesListSorted()
        regex = re.compile(r"#{1}([\w-]+)\s?", re.I) if tag == '' else re.compile(r'#{1}(' + tag + r'[\w-]*)\s?', re.I | re.UNICODE)
        for f in sorted_file_list:
            content = self._getFileContent(f['path'])
            if content != str():
                if self.search_yaml_tags_only:
                    match_obj = re.search(r"\b.*[\s\S](-{3,})", content, re.IGNORECASE | re.UNICODE)
                    if match_obj:
                        r = match_obj.group(0)
                        results = re.findall(regex, r)
                        matches.extend(results)
                else:
                    results = re.findall(regex, content)
                    matches.extend(results)
        counted_matches = Counter([v.lower() for v in matches])
        sorted_matches = OrderedDict(sorted(list(counted_matches.items()), key=lambda x: x[i[sort_by]], reverse=reverse))
        return sorted_matches

    def tasks(self, todo):
        matches = list()
        sorted_file_list = self.getFilesListSorted()
        regexPending = re.compile(r'[-|\*] {1}\[ \] {1}(.+)', re.I) if todo == '' else re.compile(r'[-|\*] {1}\[ \] {1}(.*' + todo + '.*)', re.I)
        regexDone = re.compile(r'[-|\*] {1}\[x\] {1}(.+)', re.I) if todo == '' else re.compile(r'[-|\*] {1}\[x\] {1}(.*' + todo + '.*)', re.I)
        for f in sorted_file_list:
            content = self._getFileContent(f['path'])
            if content != str():
                results = re.findall(regexPending, content)
                for i in results:
                    r_dict = {
                        'path': f['path'],
                        'todo': i,
                        'status': 'pending',
                        'filename': f['filename'],
                        'title': f['title'],
                        'mtime': self.getFileMeta(f['path'], 'mtime'),
                        'ctime': self.getFileMeta(f['path'], 'ctime')
                    }
                    matches.append(r_dict)
                results = re.findall(regexDone, content)
                for i in results:
                    r_dict = {
                        'path': f['path'],
                        'todo': i,
                        'status': 'done',
                        'filename': f['filename'],
                        'title': f['title'],
                        'mtime': self.getFileMeta(f['path'], 'mtime'),
                        'ctime': self.getFileMeta(f['path'], 'ctime')
                    }
                    matches.append(r_dict)
        ret_list_dict = sorted(matches, key=lambda k: k['ctime'], reverse=False)
        return ret_list_dict

    def templates(self):
        template_tag = self.getTemplateTag()
        file_list = self.getFilesListSorted()
        templates = list()
        if file_list is not None:
            for file in file_list:
                if self.isNoteTagged(file['path'], template_tag):
                    templates.append(file)
        return templates

    def zettelIdExists(self, zettelId):
        err = 0
        file_list = list()
        try:
            file_list = os.listdir(self.path)
        except OSError as e:
            err = e.errno
            pass
        if err == 0:
            for filename in file_list:
                if filename.startswith(zettelId):
                    return True
        return False
