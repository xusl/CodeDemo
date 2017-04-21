#!/usr/bin/python
# coding=utf-8
import os
import sys
import types
from utils import LangCodeIdx, log_init
from collections import OrderedDict
import xlrd
import xlwt
#import json

reload(sys)
sys.setdefaultencoding('utf-8')

def usage_help(prompt, script=sys.argv[0]):
    print prompt
    print script, "merge    android.xls ios.xls [all.xls]"
    print script, "split    all.xls [android.xls] [ios.xls]"
    print script, "update   base.xls refer.xls [base-update.xls]"
    print "for example:",
    print "    ", script, "split all.xls"
    print "    ", script, "merge android.xls ios.xls"

def merge(log):
    androidxls = sys.argv[2]
    iosxls = sys.argv[3]
    if len(sys.argv) >= 5:
        resultxls = sys.argv[4]
        if not resultxls.endswith("xls"):
            log.error(resultxls + " does not end with '.xls'")
            return
    else:
        resultxls = "string-all.xls"

    log.info(androidxls)
    log.info(iosxls)
    log.info(resultxls)
    if not os.path.exists(androidxls):
        raw_input("\nThere is no android xls file in directory, please move file to %s" % androidxls)
        return
    if not os.path.exists(iosxls):
        raw_input("\nThere is no ios xls file in directory, please move file to %s" % iosxls)
        return

    if os.path.exists(resultxls):
        now_input = "Y"#raw_input("%s already exits, are you sure to recover it? [Y/N]Y" % resultxls)
        if(now_input in ["", "Y"]):
            merg_xls(androidxls, iosxls, resultxls, log)
    else:
        merg_xls(androidxls, iosxls, resultxls, log)
    sort_sheet(resultxls)
#python android_stringConvert.py merge KidsWatch-Android-strings.xlsx KidsWatch-iOS-Strings.xlsx KidsWatch-Strings.xlsx

def stripCellValue(value):
    try:
        return value.strip().strip('"').replace("\\'", "\'")
    except AttributeError as e:
        print e
        print value, str(value)
        return str(value)

def merg_xls(androidxls, iosxls, resultxls, log):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
    sheet.write(0, 0, 'android_key')
    sheet.write(0, 1, 'ios_key')
    #sheet.write(0, 2, 'en')
    sheet.write(0, 3, 'comment')
    langcode = LangCodeIdx()
    defaultlang = "English"

    book = xlrd.open_workbook(androidxls)
    androidsh = book.sheet_by_index(0)

    book = xlrd.open_workbook(iosxls)
    iossh = book.sheet_by_index(0)

    for rowIndex in range(1, iossh.nrows):
        stringId = iossh.row(rowIndex)[0].value
        if not stringId.startswith("IDS_"):
            print "There are invalid string Id in the iOS sheet"
            print "May be you swap Android / iOS file name"
            print "Or the string sheet is not the first sheet of the iOS string file"
            print "Now iOS ", iosxls
            print "And Android ", androidxls
            #return
            break

    nRowIndex = 1
    nEnCol = 1
    for iosCol in range(1, iossh.ncols):
        if iossh.row(0)[iosCol].value == "en":
            nEnCol = iosCol
            break

    ioslangidx = {}
    androidlangidx = {}
    mergedidx = {}
    codeoflang = {}

    for idx, cell in enumerate(iossh.row(0)[1:], 1):
        cell_language = langcode.getLangOfCode(cell.value)
        codeoflang[cell_language] = cell.value
        ioslangidx[cell_language] = idx
    for idx, cell in enumerate(androidsh.row(0)[1:], 1):
        cell_language = langcode.getLangOfCode(cell.value)
        codeoflang[cell_language] = cell.value
        androidlangidx[cell_language] = idx

    idx = 4
    for lang in sorted(set(androidlangidx.keys() + ioslangidx.keys())):
        if lang == "":
            continue
        elif lang == defaultlang:
            mergedidx[defaultlang] = 2
            continue
        mergedidx[lang] = idx
        idx += 1

    for lang, idx in mergedidx.iteritems():
        #sheet.write(0, idx, "%s [%s]" % (lang, codeoflang[lang]))
        sheet.write(0, idx, codeoflang[lang])

    log.info("android: %s" % androidlangidx)
    log.info("ios: %s" % ioslangidx)
    log.info("merge: %s" % mergedidx)

    iosBaseCol = ioslangidx.get(defaultlang, -1)
    log.info('nEnCol %d' % nEnCol)
    log.info('iosBaseCol %d' % iosBaseCol)
    androidBaseCol = androidlangidx.get(defaultlang, 1)

    for rowIndex in range(1, androidsh.nrows):
        sheet.write(nRowIndex, 0, androidsh.row(rowIndex)[0].value)
        #sheet.write(nRowIndex, 2, androidsh.row(rowIndex)[1].value)
        for lang, idx in mergedidx.iteritems():
            col = androidlangidx.get(lang, None)
            if col is None:
                continue
            androiValue = stripCellValue(androidsh.row(rowIndex)[col].value)
            sheet.write(nRowIndex, idx, androiValue)
        nRowIndex+=1

    for rowIndex in range(1, iossh.nrows):
        isFind = 0
        iosvalue = stripCellValue(iossh.row(rowIndex)[nEnCol].value)

        for newRowIndex in range(1, androidsh.nrows):
            basevalue = stripCellValue(androidsh.row(newRowIndex)[androidBaseCol].value)
            if iosvalue.lower() == basevalue.lower():
                isFind = 1
                sheet.write(newRowIndex, 1, iossh.row(rowIndex)[0].value)
                for lang, idx in mergedidx.iteritems():
                    icol = ioslangidx.get(lang, None)
                    if icol is None:
                        continue
                    iosvalue = stripCellValue(iossh.row(rowIndex)[icol].value)
                    acol = androidlangidx.get(lang, None)
                    if acol is None:
                        sheet.write(newRowIndex, idx, iosvalue)
                        continue
                    androidvalue = stripCellValue(androidsh.row(newRowIndex)[acol].value)
                    if len(androidvalue) == 0 and len(iosvalue) != 0:
                        sheet.write(newRowIndex, idx, iosvalue)

                    if lang == 'English':
                        continue
                    if iosvalue == basevalue:
                        if androidsh == basevalue:
                            diff = "android & ios missing '%s' translate" % lang
                        else:
                            diff = "ios missing '%s' translate" % lang
                        diff += " item: \"{0}\"".format(basevalue)
                        log.info(diff)
                        log.info("*" * 78)
                    elif androidsh == basevalue:
                        diff = "android missing '%s' translate " % lang
                        diff += " item: \"{0}\"".format(basevalue)
                        log.info(diff)
                        log.info("*" * 78)
                    #elif iosvalue != androidvalue:
                    elif iosvalue.lower() != androidvalue.lower():
                        log.info("{1} not match item: \"{0}\"".format(basevalue, lang))
                        log.info("    ios {0:3}/{1:3}: {2}".format( \
                                icol,rowIndex, iosvalue))
                        log.info("android {0:3}/{1:3}: {2}".format( \
                                acol, newRowIndex, androidvalue))
                        log.info("*" * 78)
                break
        if not isFind:
            sheet.write(nRowIndex, 1, iossh.row(rowIndex)[0].value)
            #sheet.write(nRowIndex, 2, iosvalue)
            for lang, idx in mergedidx.iteritems():
                col = ioslangidx.get(lang, None)
                if col is None:
                    continue
                value = stripCellValue(iossh.row(rowIndex)[col].value)
                sheet.write(nRowIndex, idx, value)
            nRowIndex+=1

    wbk.save(resultxls)

def split(log):
    if len(sys.argv) < 2:
        usage_help("split : no input xls file")
        return
    allxls = sys.argv[2]
    if len(sys.argv) >= 5:
        androidxls = sys.argv[3]
        iosxls = sys.argv[4]
    else:
        path_dir = os.path.dirname(allxls)
        fn_tuple = os.path.splitext(os.path.basename(allxls))
        #androidxls = os.path.join(path_dir, "{0}-Android.{1}".format(*fn_tuple))
        androidxls = os.path.join(path_dir, "{0}-Android.xls".format(fn_tuple[0]))
        iosxls = os.path.join(path_dir, "{0}-iOS.xls".format(fn_tuple[0]))

    if not os.path.exists(allxls):
        raw_input("\nThere is no xls file in directory, please move file to %s" % allxls)
        return
    if os.path.exists(iosxls):
        now_input = raw_input("\n%s already exits, are you sure to recover it? [Y/N]Y" % iosxls)
        if(now_input not in ["", "Y"]):
            return

    if os.path.exists(androidxls):
        now_input = raw_input("%s already exits, are you sure to recover it? [Y/N]Y" % androidxls)
        if(now_input in ["", "Y"]):
            split_xls(allxls, androidxls, iosxls)
    else:
        split_xls(allxls, androidxls, iosxls)

def split_xls(allxls, androidxls, iosxls):
    book = xlrd.open_workbook(allxls)
    allsh = book.sheet_by_index(0)
    locutil = LangCodeIdx()

    androidwb = xlwt.Workbook()
    androidsh = androidwb.add_sheet('sheet 1')
    androidsh.write(0, 0, 'key')
    for colIndex in range(2, allsh.ncols):
        androidsh.write(0, colIndex-1, locutil.codeVariant(allsh.row(0)[colIndex].value, True))

    ioswb = xlwt.Workbook()
    iossh = ioswb.add_sheet('sheet 1')
    iossh.write(0, 0, 'key')
    for colIndex in range(2, allsh.ncols):
        iossh.write(0, colIndex-1, locutil.codeVariant(allsh.row(0)[colIndex].value, False))

    androidRow = 1
    iosRow = 1
    for rowIndex in range(1, allsh.nrows):
        if allsh.row(rowIndex)[0].value != "":
            androidsh.write(androidRow, 0, allsh.row(rowIndex)[0].value)
            for colIndex in range(2, allsh.ncols):
                androidsh.write(androidRow, colIndex-1, allsh.row(rowIndex)[colIndex].value)
            androidRow+=1
        if allsh.row(rowIndex)[1].value != "":
            iossh.write(iosRow, 0, allsh.row(rowIndex)[1].value)
            for colIndex in range(2, allsh.ncols):
                iossh.write(iosRow, colIndex-1, allsh.row(rowIndex)[colIndex].value)
            iosRow+=1

    androidwb.save(androidxls)
    ioswb.save(iosxls)

def update(log):
    if len(sys.argv) < 4:
        usage_help("split : no input xls file")
        return
    baseXls = sys.argv[2]
    referXls = sys.argv[3]
    if len(sys.argv) == 4:
        path_dir = os.path.dirname(baseXls)
        fn_tuple = os.path.splitext(os.path.basename(baseXls))
        target = os.path.join(path_dir, "{0}-updated.xls".format(fn_tuple[0]))
    else:
        target = sys.argv[4]
    update_xls(target, baseXls, referXls)

def sort_sheet(xls):
    wbk = xlwt.Workbook()
    outSh = wbk.add_sheet('sheet 1 sort', cell_overwrite_ok=True)

    baseSh = xlrd.open_workbook(xls).sheet_by_index(0)
    langcode = LangCodeIdx()
    en_idx = None
    for idx, cell in enumerate(baseSh.row(0)[1:], 1):
        cell_language = langcode.getLangCode(cell.value)
        print cell.value, cell_language
        if cell_language == "en":
            en_idx = idx
            break

    if en_idx is None:
        print "can not find base text column, that means none column named 'en'"
        return
    #sheet = []
    #for i in range(1, baseSh.nrows):
    #    row = baseSh.row_values(i)
    #    sheet.append(sheet)
    #    print row[en_idx]
    for col_num, cell in enumerate(baseSh.row_values(0)):
        outSh.write(0, col_num, cell)

    row_num = 1
    for idx, stemCell in sorted(enumerate(baseSh.col_values(en_idx)[1:]), key=lambda i:i[1], reverse=False):
        col_num = 0
        for cell in baseSh.row_values(idx + 1):
            outSh.write(row_num, col_num, cell)
            col_num += 1
        row_num += 1
        print idx+1, stemCell
    #for row in sorted(baseSh.col_values(en_idx)[1:], key=lambda i:i, reverse=False):
    #    print row
    wbk.save(xls)

def update_xls(target, baseXls, referXls):
    wbk = xlwt.Workbook()
    outSh = wbk.add_sheet('sheet 1', cell_overwrite_ok=True)
    outSh.write(0, 0, 'android_key')
    langcode = LangCodeIdx()

    baseSh = xlrd.open_workbook(baseXls).sheet_by_index(0)
    referSh = xlrd.open_workbook(referXls).sheet_by_index(0)

    baseLangIdx = OrderedDict()
    referLangIdx = OrderedDict()
    for idx, cell in enumerate(baseSh.row(0)[1:], 1):
        cell_language = langcode.getLangCode(cell.value)
        baseLangIdx[cell_language.lower()] = idx
        outSh.write(0, idx, cell_language)
    for idx, cell in enumerate(referSh.row(0)[1:], 1):
        cell_language = langcode.getLangCode(cell.value)
        referLangIdx[cell_language.lower()] = idx
    baseDefaultCol = baseLangIdx.get("en")
    referDefaultCol = referLangIdx.get("en")
    print baseLangIdx
    print referLangIdx

    if baseDefaultCol is None or referDefaultCol is None:
        log.error("can not find default language item")
        return

    baseItems = baseSh.col_values(baseDefaultCol)[1:]
    referItems = referSh.col_values(referDefaultCol)[1:]
    baseItems = [stripCellValue(i) for i in baseItems]
    referItems = [stripCellValue(i) for i in referItems]
    commonItems = set(baseItems) & set(referItems)
    commonCursor = 1

    #len(baseItems) may not equal to len(set(baseItems))
    #add 10 lines as seperate
    dismatchCursor = commonCursor + 10
    for item in baseItems:
        if item in commonItems:
            dismatchCursor += 1

    #for row, item in enumerate(baseItems, 1):
    for row, item in sorted(enumerate(baseItems, 1), key=lambda i:i[1], reverse=False):
        if item in commonItems:
            cursor = commonCursor
            commonCursor += 1
            update = True
        else:
            cursor = dismatchCursor
            dismatchCursor += 1
            update = False

        outSh.write(cursor, 0, baseSh.cell(row,0).value)
        for lang, col in baseLangIdx.items():
        #for idx, cell in enumerate(baseSh.row(0)[1:], 1):
        #    lang = langcode.getLangOfCode(cell.value)
            if update:
                refRow = referItems.index(item) + 1
                refCol = referLangIdx.get(lang)
                if refCol is not None:
                    value = stripCellValue(referSh.cell(refRow, refCol).value)
                if refCol is None or value is None or len(value) == 0:
                    value = stripCellValue(baseSh.cell(row, col).value)
            else:
                value = stripCellValue(baseSh.cell(row, col).value)
            outSh.write(cursor, col, value)

    wbk.save(target)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage_help("please give the action")
        sys.exit()
    action = sys.argv[1]
    log = log_init("msxls", 'debug')
    if action == "xmltoxls":
        androidxml_to_xls()
    elif action == "merge":
        merge(log)
    elif action == "sort":
        sort_sheet(sys.argv[2])
    elif action == "split":
        split(log)
    elif action == "update":
        update(log)
    else:
        usage_help("invalid action '{0}'".format(action))

