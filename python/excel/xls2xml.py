#!/usr/bin/env python
# coding=utf-8

import re
import sys
import os
import utils
import xlrd
from  xml.dom import  minidom

reload(sys)
sys.setdefaultencoding('utf-8')
log = utils.log_init("xls2xml", 'debug')
if len(sys.argv) < 2:
    print "no enough input"
    sys.exit()
else:
    print "python ", sys.argv[0], " string.xls "
    print "or"
    print "python ", sys.argv[0], " string.xls app/src/main/res/"

#for xml in `find KidsWatch/app/ -name "strings.xml"`; do ./scripts/multilangreplace.py scripts/android.xls $xml; done
xls_name = sys.argv[1]
if not os.path.exists(xls_name):
    log.error("The xls file '%s' is not exist." % xls_name)
    sys.exit()
sheet_index = 0
log.info("xls file {0}, sheet index {1}".format(xls_name, sheet_index))
sheet = xlrd.open_workbook(xls_name).sheet_by_index(sheet_index)
langidx = {}
langcode = utils.LangCodeIdx()
for idx, cell in enumerate(sheet.row(0)[1:], 1):
    lower_value = cell.value.lower()
    log.debug(cell.value)
    if "latam" in lower_value and "spanish" in lower_value:
        langidx['es'] = idx
        continue

    found = False
    for pattern in [".* \[(\w+)\]", "[ \(\)\w]+-(\w{2}$)", "([a-zA-Z]{2}-r[a-zA-Z]{2})",
            "([a-zA-Z]{2}$)"]:
        result = re.match(pattern, cell.value.strip())
        if result is None:
            continue
        log.info("pattern:'{0}', cell value:'{1}'".format(pattern, cell.value))
        col_loc = result.group(1)
        locs = col_loc.split("-r")
        col_loc = locs[0].lower()
        if len(locs) == 3:
            col_loc = col_loc + locs[1] + locs[2].upper()
        if col_loc == "es":
            col_loc = "es-rCO"
        langidx[col_loc] = idx
        found = True
        break
    if found: continue
    langidx[langcode.getLangCode(cell.value)] = idx

log.info("language index is %s" % langidx)

'''
if len(sys.argv) >= 4:
    cols = sys.argv[3]
else:
    lang = folder.replace("values-", "")
    cols = 'A,B,{0}'.format(utils.getColumnAlphabet(lang)[1])
print "cols is :", cols
df = pd.read_excel(xls_name, sheetname=sheet_index, parse_cols=cols, engine='xlrd')
df = df.dropna(axis=0)
for row in df.iterrows():
    print "....", row[1], "..."
    item, origin, dest = row[1]
'''
'''
test = ["<string name=\"Notifications\">Notifications</string>",
        "        <item>Mon</item>",
        "ok",
        "\"about_title\"",
        "about_version>",
        "\"about_text\">",
        "<string name=\"state_connecting\">"
        ]
for item in test:
    item = item.strip()
    #print "xxx: ", item
    if re.match("<item>.+</item>", item) is not None:
        print item, "         match rule 1."
    result = re.match("<string\s*name=\"\w+\">", item)
    if result is not None:
        print item, "         match rule 2, stem is ", result.group(0)

    result = re.match("\"*(\w+)\"*>*", item)
    if result is not None:
        print item, "         match rule 3, stem is ", result.group(1)

    #result = re.match("(<string\s*name=\"\w+\">).*</string>", item)
    #if result is not None:
    #    print item, "         match rule 4, stem is ", result.group(1)
'''

indent = "    "
def update_strings_xmls(xml_name):
    log.info(xml_name)
    for xml_file in xml_name:
        strings = None
        with open(xml_file) as xfp:
            strings = xfp.read()
        if strings is None:
            log.error("{0} is not exist.".format(xml_file))
            #sys.exit()
            continue
        strings = re.sub(r'\n\s*\n', "\n", strings)

        folder = os.path.basename(os.path.dirname(xml_file))
        targetfolder = os.path.join('res', folder)
        if not os.path.exists('res'):
            os.mkdir('res')
        if not os.path.exists(targetfolder):
            os.mkdir(targetfolder)
        out = os.path.join(targetfolder, os.path.basename(xml_file))

        if folder == "values":
            targetCol = langidx.get("en", None)
        else:
            lang = folder.replace("values-", "")
            targetCol = langidx.get(lang, None)

        referCol = langidx.get("en", 1)

        if targetCol is None:# or targetCol == referCol:
            log.info("current res is {0},and {1} is not need to handle".format(folder, targetCol))
            continue

        log.info("target column {0}, refer column {1}".format(targetCol, referCol))

        for rowIndex in range(1, sheet.nrows):
            row = sheet.row(rowIndex)
            item, origin, dest = row[0].value, row[referCol].value, row[targetCol].value

            if (type(dest) != str and type(dest) != unicode) or \
                    (type(origin) != str and type(origin) != unicode) or \
                    (type(item) != str and type(item) != unicode) or \
                    len(dest) == 0 or len(origin) == 0 or len(item) == 0:
                #print type(origin), origin, " ========  ", type(dest), dest
                continue

            item = utils.strip_ex(item)
            #dest = dest.encode('raw_unicode_escape')
            dest = utils.strip_ex(dest)
            #dest = dest.replace('\\n', '&#10;')
            #dest = dest.replace(' ', '&nbsp;') #  &#160;
            dest = dest.replace('\\n', '\\\\n')
            dest = dest.replace('\\t', '\\\\t')
            #dest = dest.replace('–', '&#8211;')
            #dest = dest.replace('…', '&#8230;')
            #dest = dest.replace('©', '&copy;')# 	&#169;
            #dest = dest.replace('®', '&reg;')# 	&#169;
            dest = re.sub(r"(?<!\\)'" , "\\'", dest)
            dest = re.sub(r"(^\")|((?<!(\\|=))\"$)" , "", dest)
            dest = re.sub(r"(?<!(\\|=))\"(?!>)" , "&quot;", dest)
            dest = re.sub(r"&(?!(\w+|#\d+);)" , "&amp;", dest) # &#38;


            if targetCol == referCol:
                dest = "<string name=\"{0}\">{1}</string>".format(item, dest)
                if strings.find("name=\""+item+"\">") < 0:
                    strings=strings.replace("</resources>", indent + dest+"\n</resources>")
                else:
                    pattern = "<string\s+name=\"{0}\">.*</string>".format(item)
                    strings = re.sub(pattern, dest, strings, count=1, flags=re.M)
                continue

            if re.match("<item>.+</item>", item):
                origin = item
                dest = "\n\t<item>{0}</item>\n".format(dest)
                new_strings = strings.replace(origin, dest, 1)
            else:
                result = re.match("\"*(\w+)\"*>*", item)
                if strings.find("name=\""+item+"\">") < 0:
                    result = re.match("<string\s*name=\"(\w+)\">", item)
                    if result is None:
                        if re.match(r"<item>.+</item>", dest, re.S):
                            dest = "\n      " + dest + "\n  "
                        dest = "  <string name=\"{0}\">{1}</string>\n</resources>". \
                                format(item, dest)
                        log.info("add new item %s" % item)
                        strings=strings.replace("</resources>", dest)
                        continue
                    #prefix = result.group(0)
                log.info("'" + item + "'")
                name = result.group(1)
                prefix = "name=\"{0}\">".format(name)
                origin = prefix + origin + "</string>"
                dest = prefix + dest + "</string>"
                new_strings = strings.replace(origin, dest, 1)

                if new_strings == strings:
                    #print "no changes ...... ", " <> ".join(row[1])
                    pattern = "<string\s+name=\"{0}\">.*\n*</string>".format(name)
                    dest = "<string " + dest
                    new_strings = re.sub(pattern, dest, strings, count=1, flags=re.M)

            strings = new_strings

        with open(out, 'w+') as xfp:
            xfp.write(strings)

def stringtable_xls_to_xml(sheet, colIndex, xmlfile):
    impl = minidom.getDOMImplementation()
    dom = impl.createDocument(None, "resources", None)
    #dom.getElementsByTagName("resources")[0].setAttribute("xmlns:xliff", "urn:oasis:names:tc:xliff:document:1.2")
    dom.documentElement.setAttribute("xmlns:xliff", "urn:oasis:names:tc:xliff:document:1.2")

    for rowIndex in range(1, sheet.nrows):
        element = dom.createElement("string")
        xmlvalue = sheet.row(rowIndex)[colIndex].value
        if (type(xmlvalue) != str and type(xmlvalue) != unicode) or len(xmlvalue) == 0 :
            continue

        xmlvalue = xmlvalue.replace("\'", "\\'")
        #xmlvalue = xmlvalue.replace("\"", "&quot;")
        #xmlvalue = xmlvalue.replace("<", "&lt;")
        #xmlvalue = xmlvalue.replace(">", "&gt;")
        element.setAttribute("name", sheet.row(rowIndex)[0].value)
        element.appendChild(dom.createTextNode(xmlvalue))
        dom.documentElement.appendChild(element)

    f= open(xmlfile, 'w')
    dom.writexml(f, addindent='    ', newl='\n', encoding='utf-8')
    f.close()
    #dom.writexml(sys.stdout, addindent='    ', newl='\n', encoding='utf-8')
    #print dom.toxml()

def xls_to_androidxml():
    for loc, idx in langidx.iteritems():
        print loc, idx
        if loc == "en":
            folder = "values"
        else:
            folder = "values-" + loc
        targetfolder = os.path.join('res', folder)
        if not os.path.exists('res'):
            os.mkdir('res')
        if not os.path.exists(targetfolder):
            os.mkdir(targetfolder)
        out = os.path.join(targetfolder, "strings.xml")
        stringtable_xls_to_xml(sheet, idx, out)

if len(sys.argv) > 2:
    log.info("*" * 78)
    log.info("        USE REPLACE ALGORITHM           ")
    log.info("*" * 78)
    if os.path.isdir(sys.argv[2]):
        xml_name = utils.find('strings.xml', sys.argv[2])
        log.info("\n".join(xml_name))
        update_strings_xmls(sorted(xml_name))
        xml_name = utils.find('arrays.xml', sys.argv[2])
        update_strings_xmls(sorted(xml_name))
    elif os.path.isfile(sys.argv[2]):
        update_strings_xmls(sys.argv[2:])
    else:
        log.info("invalid parameter:%s, it must be a file or directory." %
                sys.argv[2])
else:
    log.info("*" * 78)
    log.info("        USE XML PARSER ALGORITHM           ")
    log.info("*" * 78)
    #xml_name = utils.find('*strings.xml', '.')
    xls_to_androidxml()
