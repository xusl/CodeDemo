#!/usr/bin/python
import os, fnmatch
import re
import logging
from datetime import datetime

def strip_ex(string):
    result = re.match(".*:\s+$", string)
    string = string.strip()
    if result is None:
        return string
    else:
        return string + " "

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

class LangCodeIdx(object):
    INVALID_IDX = -1
    def __init__(self, base = 0, android = True):
        self.idx_base = base
        self.current_idx = base + 1
        self.count = 0
        self.lang_idx = {}
        self.code_idx = {}
        self.code_lang_map = {}
        self.all_item = []
        self.setupDefault(android)

    def addItem(self, lang, *codes):
        if lang is None or codes is None or len(codes) == 0:
            return

        idx = self.current_idx + 1
        self.current_idx += 1

        if lang in self.lang_idx:
            if idx != self.lang_idx[lang]:
                print "Error, {0} index may be changed".format(lang)
                return
        else:
            self.lang_idx[lang] = idx

        for code in codes:
            self.code_idx[code] = idx
            self.count += 1
            self.all_item.append([lang, code, idx])
            self.code_lang_map[code] = lang

    def getLangOfCode(self, code):
        lang = self.code_lang_map.get(code, None)
        if lang is None:
            print "can not find the language for code ", code
            return code

        return lang

    def getLangCode(self, lang):
        for item in self.all_item:
            if lang.lower() == item[0].lower():
                return item[1]
        return lang

    def codeVariant(self, code, android_code=True):
        if android_code:
            if code == 'es-rCO' or code == 'es':
                return 'es-419'
            else:
                return code
        else:
            if code == 'es':
                return 'es-rES'
            else:
                return code

    def dump(self):
        for i in self.all_item:
            print "{0:<20} {1:<6} {2}".format(*i)

    def setupDefault(self, android):
        self.addItem('English','en')
        self.addItem('English: GB','en-rGB', 'en-GB')
        self.addItem('Arabic','ar')
        self.addItem('Bulgarian','bg')
        self.addItem('Czech','cs')
        self.addItem('Danish','da', 'da-rDK')
        self.addItem('German','de')
        self.addItem('Ewe','ee')
        self.addItem('Greek','el')
        #self.addItem('Spanish','es')
        self.addItem('Spanish','es-rES')
        self.addItem('Latam Spanish','es','es-419', 'es-rCO')
        self.addItem('Spanish: US','es-rUS') #TODO: Android fix it
        self.addItem('Spanish: Mexico','es-rMX')
        self.addItem('Estonian','et')
        #self.addItem('Persian','fa')
        self.addItem('Finnish','fi','fi-rFI')
        self.addItem('French','fr')
        #self.addItem('Croatian','hr')
        self.addItem('Hungarian','hu')
        #self.addItem('Indonesian','in')
        self.addItem('Italian','it')
        #self.addItem('Hebrew','iw')
        self.addItem('Lithuanian','lt')
        self.addItem('Latvian: Lettish','lv')
        #self.addItem('Macedonian','mk')
        self.addItem('Dutch','nl')
        self.addItem('Norwegian','no','nn-NO')
        self.addItem('Polish','pl')
        self.addItem('Portuguese','pt')
        self.addItem('Portuguese (Brazil)','pt-rBR','pt-BR')
        self.addItem('Romanian','ro','ro-rRO')
        self.addItem('Russian','ru','ru-rRU')
        self.addItem('Slovak','sk')
        self.addItem('Slovene','sl')
        self.addItem('Serbian','sr')
        self.addItem('Swedish','sv')
        self.addItem('Turkish','tr')
        self.addItem('Ukrainian','uk')
        self.addItem('Chinese: China','zh-rCN','zh-Hans')
        self.addItem('Chinese: Hong Kong','zh-rHK','zh-Hant')
        self.addItem('Chinese: Taiwan','zh-rTW')

class Id(object):
    SET = 1
    EMPTY = 0
    INVALID_ID = -1
    def __init__(self, base = 1, capacity=128):
        self.map = [self.EMPTY] * capacity
        self.indicator = 0
        self.capacity = capacity
        self.datum_len = 0
        self.base = base
        self.colIdCache = {}

    def assign_lang(self, lang):
        idx = self.colIdCache.get(lang, None)
        if idx is None:
            idx = self.get()
            self.colIdCache[lang] = idx
        return idx

    def get(self):
        id = self.indicator
        self.map[id] = self.SET
        self.indicator = self.next(self.indicator)
        self.datum_len += 1
        return id + self.base

    def put(self, idv):
        if idv is None:
            return
        if isinstance(idv, int):
            id = idv - self.base
        else:
            return

        if id < 0 or id >= self.capacity:
            return
        if self.map[id] == self.SET:
            return

        self.datum_len -= 1
        self.map[id] = self.EMPTY

    def next(self, now):
        i = now + 1
        while i < self.capacity:
            if self.map[i] == self.EMPTY:
                return i
            i += 1

        i = 0
        while i < now:
            if self.map[i] == self.EMPTY:
                return i
            i += 1

        i = self.capacity
        self.map += [self.EMPTY] * 32
        self.capacity += 32
        return i

    def __len__(self):
        return self.datum_len

def getColumnNumber(code, offset=2):
    #https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    android_sheet_cols = {
            'ar':     ['Arabic'              ,24],
            'bg':     ['Bulgarian'           ,5],
            'cs':     ['Czech'               ,7],
            'da':     ['Danish'              ,21],
            'de':     ['German'              ,15],
            'el':     ['Greek'               ,4],
            'es':     ['Spanish'             ,8],
            'es-rUS': ['Spanish (US)'         ,9],
            #'es-rMX': ['Spanish (Mexico)'         ,9],
            'et':     ['Estonian'            ,23],
            #'fa':     ['Persian'             ,15],
            'fi':     ['Finnish'             ,20],
            'fr':     ['French'              ,12],
            #'hr':     ['Croatian'            ,20],
            'hu':     ['Hungarian'           ,16],
            #'in':     ['Indonesian'          ,22],
            'it':     ['Italian'             ,11],
            #'iw':     ['Hebrew'              ,24],
            'lt':     ['Lithuanian'          ,22],
            'lv':     ['Latvian (Lettish)'   ,18],
            #'mk':     ['Macedonian'          ,26],
            'nl':     ['Dutch'               ,14],
            'no':     ['Norwegian'           ,19],
            'pl':     ['Polish'              ,10],
            #'pt':     ['Portuguese'          ,31],
            #'pt-rBR': ['Portuguese (Brazil)'   ,32],
            'ro':     ['Romanian'            ,17],
            'ru':     ['Russian'             ,25],
            'sk':     ['Slovak'              ,6],
            'sl':     ['Slovene'             ,13],
            'sr':     ['Serbian'             ,26],
            'sv':     ['Swedish'             ,27],
            'tr':     ['Turkish'             ,28],
            'uk':     ['Ukrainian'           ,29],
            'zh-rCN': ['Chinese: China'      ,30],
            'zh-rHK': ['Chinese: Hong Kong'  ,31],
            'zh-rTW': ['Chinese: Taiwan'     ,32]
            }
    result = android_sheet_cols.get(code, ['English', 3])
    result[1] -= offset
    return result

def getColumnAlphabet(code):
    #https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    android_sheet_cols = {
            'ar':     ['Arabic'              ,'X'],
            'bg':     ['Bulgarian'           ,'D'],
            'cs':     ['Czech'               ,'F'],
            'da':     ['Danish'              ,'U'],
            'de':     ['German'              ,'N'],
            'el':     ['Greek'               ,'C'],
            'es':     ['Spanish Latam'       ,'H'],
            'es-rES': ['Spanish'             ,'G'],
            'es-rUS': ['Spanish (US)'         ,'AA'],
            #'es-rMX': ['Spanish (Mexico)'         ,9],
            'et':     ['Estonian'            ,'W'],
            #'fa':     ['Persian'             ,15],
            'fi':     ['Finnish'             ,'T'],
            'fr':     ['French'              ,'K'],
            #'hr':     ['Croatian'            ,20],
            'hu':     ['Hungarian'           ,'O'],
            #'in':     ['Indonesian'          ,22],
            'it':     ['Italian'             ,'V'],
            #'iw':     ['Hebrew'              ,24],
            'lt':     ['Lithuanian'          ,'J'],
            'lv':     ['Latvian (Lettish)'   ,'R'],
            #'mk':     ['Macedonian'          ,26],
            'nl':     ['Dutch'               ,'M'],
            'no':     ['Norwegian'           ,'S'],
            'pl':     ['Polish'              ,'I'],
            'pt':     ['Portuguese'          ,'Z'],
            #'pt-rBR': ['Portuguese (Brazil)'   ,32],
            'ro':     ['Romanian'            ,'P'],
            'ru':     ['Russian'             ,'Y'],
            'sk':     ['Slovak'              ,'E'],
            'sl':     ['Slovene'             ,'L'],
            #'sr':     ['Serbian'             ,],
            'sv':     ['Swedish'             ,'Q'],
            #'tr':     ['Turkish'             ,28],
            #'uk':     ['Ukrainian'           ,29],
            'zh-rCN': ['Chinese: China'      ,'AC'],
            #'zh-rHK': ['Chinese: Hong Kong'  ,31],
            #'zh-rTW': ['Chinese: Taiwan'     ,32]
            }
    result = android_sheet_cols.get(code, ['English', 'B'])
    return result

#tag: any string
#debug: may be one of 'debug', 'info', 'warn', 'error', 'fatal'
def log_init(tag, debug, out_path="log"):
    logname = datetime.now().strftime(tag + '-%m-%d-%H-%M.log')
    logname = os.path.join(out_path, logname)
    if not os.path.exists(os.path.dirname(logname)):
        os.mkdir(os.path.dirname(logname), 0777)

    level_value =  eval('logging.' + debug.upper())
    file_level = level_value
    consoel_level = level_value

    logging.basicConfig(level=file_level,#logging.DEBUG,
                        #format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        format='%(name)-6s %(levelname)-5s %(module)10s %(lineno)4d %(message)s',
                        #datefmt='%m-%d %H:%M',
                        filename=logname,
                        filemode='a')
                        #filemode='w')
    console = logging.StreamHandler()
    console.setLevel(consoel_level)
    formatter = logging.Formatter('%(name)-6s: %(levelname)-5s %(module)10s %(lineno)4d %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(tag)
    return logger

if __name__ == '__main__':
    lci = LangCodeIdx()
    lci.dump()
