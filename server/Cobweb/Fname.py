#-*-coding: utf-8 -*-

import hashlib
import json
import os
import sys

class Fname:
    def __init__(self, dict_string):
        # dict_string for encryption
        self._dict_string_length = len(dict_string)
        self._dict_num = []
        for char in dict_string: self._dict_num.append(ord(char)-31)

        # directory for Modules
        self._root_path = os.path.join(sys.path[0], "Modules")


    # Module file's md5sum
    def _md5sum(self, filename):
        try:
            m = hashlib.md5()
            f = open(filename, 'r')
            m.update(f.read())
            f.close()
            return m.hexdigest()
        except:
            return False

    # Encryption text
    def encryption(self, text):
        try:
            count = 0
            result = ""
            for char in text:
                new_number = ord(char)
                if new_number >= 32 and new_number <= 126:
                    nn = new_number + self._dict_num[count]
                    if nn > 126: nn = nn - 126 + 31
                    new_char = chr(nn)
                else:
                    new_char = char
                result += new_char
                count += 1
                if count == self._dict_string_length: count = 0
            return result
        except:
            return False

    # Get modules list's cache
    def index(self):
        try:
            index_string = self._index_string
        except:
            index_string = self.newindex()
        finally:
            return index_string

    # Make modules list's cache
    def newindex(self):
        try:
            # list All files in the Modules direction
            root_len = len(self._root_path)
            items = []
            for root, dirs, files in os.walk(self._root_path):
                for fname in files:
                    filename = os.path.join(root, fname)
                    path = root[root_len+1:]
                    item = {
                        "path" : path,
                        "filename" : fname,
                        "md5sum" : self._md5sum(filename),
                        "timestamp" : os.path.getmtime(filename)
                    }
                    items.append(item)
            # encryption JSON String and cache
            index_string = self.encryption(json.dumps(items))
            self._index_string = index_string
            return index_string
        except:
            return False

    # Get modules file's source code
    def files(self, fname):
        try:
            filename = os.path.join(self._root_path, fname)
            if os.path.isfile(filename):
                f = open(filename, 'r')
                text = f.read()
                f.close()
                result = self.encryption(text)
            else:
                result = ""
        except:
            result = ""
        finally:
            return result