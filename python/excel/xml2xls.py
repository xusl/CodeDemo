#!/usr/bin/env python
# coding=utf-8

import xlwt
import xlsxwriter
import sys
from xml.sax import *
import os
import re
#from  xml.dom import  minidom
import xml.dom.minidom
import StringIO
from utils import Id, LangCodeIdx, find, strip_ex, log_init
reload(sys)
sys.setdefaultencoding('utf-8')

if len(sys.argv) >= 2:
    #xml_name = sys.argv[1:]
    xml_name = find('strings.xml', sys.argv[1])
    xml_name += find('arrays.xml', sys.argv[1])
else:
    xml_name = find('*strings*.xml', '.')

xml_name = sorted(xml_name)
log = log_init("xml2xls", 'debug')
for files in xml_name:
    log.debug(files)

parser=make_parser()

#workbook = xlwt.Workbook(encoding = 'utf-8')
#worksheet = workbook.add_sheet('strings', cell_overwrite_ok=False)
#./strings-to-xls.py ~/workspace/MoveTime/Android/MoveBand/wristband/src/main/res/values-{fr,es,es-rMX,en,de,it,ro-rRO,pt-rBR,pt-rPT}/{strings.xml,strings_dfu.xml,arrays.xml,ssdk_strings.xml,umeng_common_strings.xml,umeng_update_string.xml}  ~/workspace/MoveTime/Android/MoveBand/sparkView/src/main/res/values-{fr,es,es-rMX,en,de,it,ro-rRO,pt-rBR,pt-rPT}/{strings.xml,arrays.xml} ~/workspace/MoveTime/Android/MoveBand/sparkView/src/main/res/values/{strings.xml,arrays.xml} ~/workspace/MoveTime/Android/MoveBand/wristband/src/main/res/values/{strings.xml,strings_dfu.xml,arrays.xml,ssdk_strings.xml,umeng_common_strings.xml,umeng_update_string.xml}

#python strings-to-xls.py ../KidsWatch/app/src/main/
workbook  = xlsxwriter.Workbook('Android-strings.xlsx')
worksheet = workbook.add_worksheet('strings')

random = True
add_lang = False
colId = Id(2)
codeLang = LangCodeIdx()
def getLangCol(xml_name):
    folder = os.path.basename(os.path.dirname(xml_name))
    xmlloc = folder.replace("values-", "")

    if not random :
        return utils.getColumn(xmlloc)

    if xmlloc == "values":
        xmlloc = "en"
        idx = 1
    else:
        idx = colId.assign_lang(xmlloc)
    if not add_lang:
        name = xmlloc
    else:
        lang = codeLang.getLangOfCode(xmlloc)
        if lang == xmlloc:
            name = lang
        else:
            name = "%s [%s]" % (lang, xmlloc)

    return [name, idx]

STRING_LEVEL = 2
class UserDecodeHandler(ContentHandler):
    data = ""
    currenttag = None
    row = 1
    column = 1
    sheet_items = {}
    depth = 0

    def setColumn(self, title, col):
        try:
            #worksheet.write(0, col, label = title)
            worksheet.write(0, col, title)
        except Exception as e:
            log.error(e)
        self.column = col

    def startDocument(self):
        self.depth = 0
        worksheet.write(0, 0, "android_key")
        log.info("start xml document")

    def endDocument(self):
        data = ""
        currenttag = None
        log.info("end xml document")
        if self.depth != 0:
            log.warning("the depth is not return to 0")

    def startElement(self,name,attrs):
        self.currenttag = name
        self.depth += 1
        if self.depth == STRING_LEVEL:
            if name == 'string' or name == 'string-array':
                item_row = self.sheet_items.get(attrs['name'], None)
                if item_row is None:
                    self.row = len(self.sheet_items) + 1
                    self.sheet_items[attrs['name']] = self.row
                    #worksheet.write(self.row, 0, label = attrs['name'])
                    worksheet.write(self.row, 0, attrs['name'])
                else:
                    self.row = item_row
        elif self.depth > STRING_LEVEL - 1:
            if not self.data.endswith(' '):
                self.data += ' '
            self.data += '<{0}'.format(name)
            for k, v in attrs.items():
                self.data += ' {0}="{1}"'.format(k,v)
            self.data += '>'

    def endElement(self,name):
        self.currenttag = None
        self.depth -= 1
        if self.depth == STRING_LEVEL - 1:
            if name=="string" or name == 'string-array':
                log.info("row:column={0}:{1} write {2}".format(self.row, \
                    self.column, self.data))
                #worksheet.write(self.row, self.column, label = self.data)
                worksheet.write(self.row, self.column, self.data.strip())
                self.data = ''
            else:
                log.error("error, can not handle tag {0}".format(name))
        elif self.depth > STRING_LEVEL - 1:
            self.data += '</{0}>'.format(name)
            if name == 'item':
                self.data += '\n      '

    def characters(self, content):
        strip_content = strip_ex(content)
        strip_content = re.sub(r"\\(?=')" , "", strip_content)
        if self.currenttag is None:
            if self.depth == STRING_LEVEL:
                self.data += strip_content
            return
        if self.currenttag == 'string':
            self.data += strip_content
        elif self.depth > STRING_LEVEL - 1:
            self.data += strip_content
            #if self.currenttag == 'item':
            #    if len(self.data) == 0:
            #        self.data = content
            #    else:
            #        self.data += '\n' + content

handler=UserDecodeHandler()
parser.setContentHandler(handler)
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

data=""
for name in xml_name:
    try:
        with open(name) as file:
            data=file.read().strip()
    except IOError as error:
        log.error(error)
        continue
	#StringIO模块用于将字符串转换成流数据，类似于Java的ByteArrayOutputStream和ByteArrayInputStream
    handler.setColumn(*getLangCol(name))
    parser.parse(StringIO.StringIO(data))

#workbook.save('strings.xls')
workbook.close()

'''
def androidxml_to_xls():
    xmlfile = sys.argv[2]
    xlsfile = sys.argv[3]

    if not os.path.exists(xmlfile):
        raw_input("\nThere is no Language.xml file in directory, please move file to %s" % xmlfile)
        return

    if os.path.exists(xlsfile):
        now_input = raw_input("String_Table.xls already exits, are you sure to recover it? [Y/N]Y")
        if(now_input in ["", "Y"]):
            stringtable_xml_to_xls(xmlfile, xlsfile)
    else:
        stringtable_xml_to_xls(xmlfile, xlsfile)

def stringtable_xml_to_xls(xmlfile, xlsfile):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1')
    sheet.write(0,0, 'key')

    dom = minidom.parse(xmlfile)
    root = dom.documentElement
    string_nodes = root.getElementsByTagName('string')

    nKeyIndex = 1
    for item in string_nodes:
        value = item.childNodes[0].nodeValue
        value = value.replace("\\'","\'")
        name = item.getAttribute("name")
        sheet.write(nKeyIndex, 0, name)
        sheet.write(nKeyIndex, 1, value)
        nKeyIndex+=1

    wbk.save(xlsfile)
'''
