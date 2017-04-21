#!/usr/bin/env python
# coding=utf-8
"""
" Author : Zen (Shenlong Xu, shecenon@gmail.com)
" Last Change: 2015-08-31 18:53:04
"""
from optparse import OptionGroup
from optparse import OptionParser
from difflib import get_close_matches
from datetime import datetime, date, timedelta
import time, os, logging, re
#from time import sleep
import ConfigParser
from subprocess import Popen
from textwrap import fill
from xlrd import open_workbook, cellname
#from xlrd.timemachine import xrange, REPR
import xlrd
import sys, glob, traceback, gc
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

class WorkBook():
    def __init__(self, filename, logger):
        if filename is None or logger is None:
            print "WorkBook initialization failed : invalid parameter."
            return
        self.workbook = open_workbook(filename)
        self.logger = logger
        self.sheet = None

    def get_sheets(self):
        return self.workbook.sheets()

    def unload_sheet(self):
        if self.sheet is not None:
            self.workbook.unload_sheet(self.sheet.name)
            self.sheet = None

    def get_named_cell(self, name):
        if name is None:
            return None
        nobj_list = self.workbook.name_map.get(name.lower())
        if not nobj_list:
            self.logger.error("%r: unknown name" % name)
            return None
        if len(nobj_list) == 0:
            self.logger.error("%r: not refenence any range" % name)
            return None
        try:
            return nobj_list[0].cell()
        except XLRDError as err:
            self.logger.error("%s is not a constant absolute reference to a single cell." % name)
            return None
        #for nobj in nobj_list:
        #    print nobj.cell().value
        #    print nobj.result.value

    def load_sheet(self, sheetname):
        if sheetname is None:
            self.logger("sheet name is None")
            return None
        sheetname = sheetname.lower()
        sheet = None
        for name in self.workbook.sheet_names():
            if name.lower().strip() == sheetname:
                self.unload_sheet()
                self.sheet = self.workbook.sheet_by_name(name)
                sheet = self.sheet
                break
        if sheet is None:
            logger.error("None profiles sheet found")
        return sheet

    def show_row(self, sh, rowx, colrange, printit):
        if self.workbook.ragged_rows:
            colrange = range(sh.row_len(rowx))
        if not colrange: return
        if printit: print()
        if self.workbook.formatting_info:
            for colx, ty, val, cxfx in self.get_row_data(sh, rowx, colrange):
                if printit:
                    print("cell %s%d: type=%d, data: %r, xfx: %s"
                        % (xlrd.colname(colx), rowx+1, ty, val, cxfx))
        else:
            for colx, ty, val, _unused in self.get_row_data(sh, rowx, colrange):
                if printit:
                    print("cell %s%d: type=%d, data: %r" % (xlrd.colname(colx), rowx+1, ty, val))

    def showable_cell_value(self, celltype, cellvalue, datemode):
        if celltype == xlrd.XL_CELL_DATE:
            try:
                showval = xlrd.xldate_as_tuple(cellvalue, datemode)
            except xlrd.XLDateError:
                e1, e2 = sys.exc_info()[:2]
                showval = "%s:%s" % (e1.__name__, e2)
        elif celltype == xlrd.XL_CELL_ERROR:
            showval = xlrd.error_text_from_code.get(
                cellvalue, '<Unknown error code 0x%02x>' % cellvalue)
        else:
            showval = cellvalue
        return showval

    def get_row_data(self, sh, rowx, colrange):
        result = []
        dmode = self.workbook.datemode
        ctys = sh.row_types(rowx)
        cvals = sh.row_values(rowx)
        for colx in colrange:
            cty = ctys[colx]
            cval = cvals[colx]
            if self.workbook.formatting_info:
                cxfx = str(sh.cell_xf_index(rowx, colx))
            else:
                cxfx = ''
            if cty == xlrd.XL_CELL_DATE:
                try:
                    showval = xlrd.xldate_as_tuple(cval, dmode)
                except xlrd.XLDateError:
                    e1, e2 = sys.exc_info()[:2]
                    showval = "%s:%s" % (e1.__name__, e2)
                    cty = xlrd.XL_CELL_ERROR
            elif cty == xlrd.XL_CELL_ERROR:
                showval = xlrd.error_text_from_code.get(cval, '<Unknown error code 0x%02x>' % cval)
            else:
                showval = cval
            result.append((colx, cty, showval, cxfx))
        return result

class DrvItem:
    SEC_NORMAL= u"Normal Customize"#This section is basic informatin. MANDATORY
    SEC_FW_INFO = u"PID_VID_FW"
    SEC_INSTALL_INFO = u"SpecialCode_IN_AppName"#Options for insall dashboard driver
    SEC_REMOVE_INFO = u"Remove_Function"#Options for uninstall dashboard driver
    SEC_ADD_FUNC = u"Add_Function"

    ITEM_CUSTOM_NAME = u"CustomName"
    ITEM_APP_NAME = u"AppName"
    ITEM_CDROM_NAME = u"CDRomName"
    ITEM_CDROM_ICON = u"CDRomICON"
    ITEM_CDROM_ICON_PATH = u"CDRomICONPath"
    ITEM_URL = u"Url"
    ITEM_MAC_VERSION = u"MacVer"
    ITEM_WIN_VERSION = u"WinVer"
    ITEM_LANGS = u"Language"
    ITEM_DEFAULT_LANG = u"DefaultLanguage"
    ITEM_DESKTOP_ICON_CUST = u"DesktopIconCust"
    ITEM_DESKTOP_ICON_PATH = u"DesktopIconPath"
    ITEM_AUTORUN_STYLE = u"AutoRunStyle"
    ITEM_WIZARD_IMAGE = u"WizardImageFile"
    ITEM_WIZARD_IMAGE_PATH = u"WizardImageFilePath"
    ITEM_WIZARD_SMALL_IMAGE = u"WizardSmallImageFile"
    ITEM_WIZARD_SMALL_IMAGE_PATH = u"WizardSmallImageFilePath"
    ITEM_APP_PUBLISHER = u"AppPublisher"
    ITEM_SPECIALCODE_IN_APPNAME = u"SpecialCode_IN_AppName"
    ITEM_DEFAULT_DIR_NAME = u"DefaultDirName"
    ITEM_DEFAULT_GROUP_NAME = u"DefaultGroupName"
    ITEM_RM_SPCODE_FOR_MACNAME = u"RemoveSpCode_For_MacName"
    ITEM_DISKVID = u"DiskVid"
    ITEM_DISKPID = u"DiskPid"
    ITEM_CDROMID = u"CDROMID"
    ITEM_RM_DESKTOP_ICON = u"Remove_DesktopIcon"
    ITEM_RM_GROUP_ICON = u"Remove_GroupIcon"
    ITEM_RM_MODEMLISTENER = u"Remove_ModemListener"
    ITEM_RM_OPEN_URL = u"Remove_OpenUrl"
    ITEM_RM_WAITING_CIRCLE = u"Remove_WaitingCircle"
    ITEM_USBHUBSWITCH = u"Add_USBHubSwitch"# 是否总线切换

class DriverConfig:
    def __init__(self, name="config.ini"):
        self.parser = ConfigParser.SafeConfigParser()
        self.filename = name
        if not os.path.exists(name):
            self.default_config()
            #with open(name, 'wb') as config:
            #    self.parser.write(config)
        else:
            #self.parser.read(name)
            with codecs.open(name, 'rb', 'utf-16le') as config:
                self.parser.readfp(config)

            #print "xxxxxxxxxxxxx", self.parser.get(DrvItem.SEC_ADD_FUNC, DrvItem.ITEM_USBHUBSWITCH)
            #print "xxxxxxxxxxxxx", self.parser.get(DrvItem.SEC_NORMAL, DrvItem.ITEM_LANGS)
            #os.exit(0)

    def getConfigParser(self):
        return self.parser

    def default_config(self):
        YES = u'YES'
        NO = u'NO'
        D = u'D'#default, to get information from project .ini file, not
        # a custom requirement Excel
        self.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_CDROM_ICON, YES)
        self.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_DESKTOP_ICON_CUST, YES)
        self.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_AUTORUN_STYLE, YES)
        self.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_LANGS, 'en')
        self.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_WIZARD_IMAGE, NO)
        self.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_WIZARD_SMALL_IMAGE, NO)
        self.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_APP_PUBLISHER, D)
        self.set(DrvItem.SEC_INSTALL_INFO, DrvItem.ITEM_SPECIALCODE_IN_APPNAME, D)
        self.set(DrvItem.SEC_INSTALL_INFO, DrvItem.ITEM_DEFAULT_DIR_NAME, D)
        self.set(DrvItem.SEC_INSTALL_INFO, DrvItem.ITEM_DEFAULT_GROUP_NAME, D)
        self.set(DrvItem.SEC_INSTALL_INFO, DrvItem.ITEM_RM_SPCODE_FOR_MACNAME, D)
        self.set(DrvItem.SEC_FW_INFO, DrvItem.ITEM_DISKVID, D)
        self.set(DrvItem.SEC_FW_INFO, DrvItem.ITEM_DISKPID, D)
        self.set(DrvItem.SEC_FW_INFO, DrvItem.ITEM_CDROMID, D)
        self.set(DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_DESKTOP_ICON, NO)
        self.set(DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_GROUP_ICON, NO)
        self.set(DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_MODEMLISTENER, NO)
        self.set(DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_OPEN_URL, NO)
        self.set(DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_WAITING_CIRCLE, NO)
        self.set(DrvItem.SEC_ADD_FUNC, DrvItem.ITEM_USBHUBSWITCH, NO)

    def set(self, section, item, value=""):
        try:
            self.parser.set(section, item, value)
        except ConfigParser.NoSectionError as err:
            self.parser.add_section(section)
            self.parser.set(section, item, value)

    def get(self, section, item, default=None):
        return self.parser.get(section, item, default)

    def check(self):
        pass

    def __del__(self):
        #try:
        #    with open(self.filename, 'wb') as config:
        #        self.parser.write(config)
        #except UnicodeEncodeError as err:
        #    print err
        with codecs.open(self.filename, 'wb', 'utf-16le') as config:
            self.parser.write(config)


class Profile:
    NA = "N/A"
    def __init__(self, plmn, name, apn, username, password, auth, type):
        if isinstance(plmn, str):
        #if isinstance(plmn, unicode):
            self.plmn = plmn
        else:
            self.plmn = "%d" % plmn #str(plmn)
        self.name = name
        self.apn = apn
        self.username = username
        self.password = password
        self.auth = auth
        self.type = type

    def isValidate(self):
        if self.plmn is None:
            return False
        if self.name is None:
            return False
        if self.apn is None:
            return False

        return True

class ProfileManager:
    def __init__(self, dir, logger):
        self.profiles = []
        self.column = {}
        self.out_dir = dir
        self.logger = logger

    def parse_items(self, sh, rowx=0):
        types = sh.row_types(rowx)
        values = sh.row_values(rowx)
        for index, type, value in zip(range(sh.ncols), types, values):
            if type == xlrd.XL_CELL_ERROR or type == xlrd.XL_CELL_EMPTY or \
               type == xlrd.XL_CELL_BLANK :
                   continue
            if type == xlrd.XL_CELL_TEXT:
                self.column[value.lower().strip()] = index

    #if not mandatory, set default to "", otherwise set None
    def get_data(self, name, types, values, default=None):
        if len(types) != len(values):
            self.logger.error("types in not match values")
            return default
        #isinstance("ss", str) => True
        #isinstance(u"ss", unicode) => True
        #isinstance(u"ss", str) => False
        if isinstance(name, unicode):
            index = self.column.get(name.lower().strip(), None)
        else:
            for n in name:
                index = self.column.get(n.lower().strip(), None)
                if index is not None:
                    break

        if index is None:
            self.logger.error("can not find column '%s' index" % name)
            return default

        if len(types) <= index:
            self.logger.error("column '%s' index exceed values boundary" % name)
            return default

        type, value = types[index], values[index]
        if type == xlrd.XL_CELL_EMPTY:
            return value
        elif type == xlrd.XL_CELL_TEXT:
            value = value.strip()
            if value.lower() == 'n/a':
                return Profile.NA
            else:
                return value
        elif type == xlrd.XL_CELL_DATE:
            return value # xlrd.xldate_as_tuple(value, dmode)
        elif type == xlrd.XL_CELL_NUMBER:
            return "%d" % value
        elif type == xlrd.XL_CELL_BOOLEAN:
            return value
        else: # type == XL_CELL_BLANK or type == XL_CELL_ERROR:
            return default

    def add_profile(self, sh, rowx):
        types, values = sh.row_types(rowx), sh.row_values(rowx)
        plmn = self.get_data(u"PLMN", types, values)
        name = self.get_data(u"Profile Name", types, values)
        apn = self.get_data(u"APN", types, values)
        username = self.get_data(u"Username", types, values)
        password = self.get_data(u"Password", types, values)
        auth = self.get_data([u"Auth.", u"Authentication"], types, values)
        type = self.get_data(u"Type", types, values)
        profile = Profile(plmn, name, apn, username, password, auth, type)
        self.profiles.append(profile)

    def write_profile(self):
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir, 0777)

        names = set([])
        for profile in self.profiles:
            if not profile.isValidate():
                continue

            filename = profile.plmn
            if filename in names:
                filename = u"_".join([profile.plmn, profile.name])
            suffix = 1
            while True:
                if filename not in names:
                    break
                filename = u"_".join([profile.plmn, profile.name, unicode(suffix)])
                suffix += 1

            names.add(filename)
            with open(os.path.join(self.out_dir, filename), 'wb') as fd:
                self.do_write(fd, profile)

    def do_write(self, fd, profile):
        fd.write("apn:")
        fd.write(profile.apn)
        fd.write("\r\n")
        fd.write("name:")
        fd.write(profile.name)
        fd.write("\r\n")
        fd.write("user:")
        fd.write(profile.username)
        fd.write("\r\n")
        fd.write("psw:")
        fd.write(profile.password)


def generate_profile_files(input_excel, out_dir, logger):
    if input_excel is None:
        logger.error("None input profile table document")
        return False

    if out_dir is None:
        out_dir = "."

    logger.info( "generate_profile_files %s" % input_excel)

    wb = WorkBook(input_excel, logger)
    sheet = wb.load_sheet('Profiles')
    if sheet is None:
        return

    pm = ProfileManager(out_dir, logger)
    pm.parse_items(sheet, 0)
    for row_index in range(1, sheet.nrows):
        pm.add_profile(sheet, row_index)
    pm.write_profile()

#        print wb.get_row_data(sheet, row_index, range(sheet.ncols))
#
#        for col_index in range(sheet.ncols):
#            print cellname(row_index, col_index), '-',
#            cell = sheet.cell(row_index, col_index)
#            print cell.value, cell.ctype
#            print sheet.cell_type(row_index, col_index),
#            print sheet.cell_value(row_index, col_index)

def require_check(require, logger):
    pass

def require_convert(input_excel, out_ini, logger):
    if input_excel is None or out_ini is None:
        logger.error("None input document, or none output filename")
        return False
    logger.info( "require_convert %s" % input_excel)
    config = DriverConfig(out_ini)
    wb = WorkBook(input_excel, logger)
    #sheet = wb.load_sheet('Dashboard')
    #if sheet is None:
    #    return
    #for r in range(sheet.nrows):
    #    wb.show_row(sheet, r, range( sheet.ncols), True)
    #print xlrd.cellname(1, 1)

    #for name in wb.workbook.name_map:
    #    print name

    baseinfo= {"Project": "PROJECT",
            "Platform": "PLATFORM",
            "Customer": "CUSTOMER",
            "Version": "VERSION"}
    for title, name in baseinfo.iteritems():
        cell = wb.get_named_cell(name)
        if cell is None:
            continue
        logger.info("%-16s: %s", title, cell.value)

    config_items = {"HOME_URL" : [DrvItem.SEC_NORMAL, DrvItem.ITEM_URL],
            "DEFAULT_LANGUAGE" : [DrvItem.SEC_NORMAL, DrvItem.ITEM_DEFAULT_LANG],
            "CUSTOMER":[DrvItem.SEC_NORMAL, DrvItem.ITEM_CUSTOM_NAME],
            "INSTALLER_EXE_NAME":[DrvItem.SEC_NORMAL, DrvItem.ITEM_APP_NAME],
            "CDROMICON_NAME":[DrvItem.SEC_NORMAL, DrvItem.ITEM_CDROM_NAME],
            "WINDOWS_VERSION":[DrvItem.SEC_NORMAL, DrvItem.ITEM_MAC_VERSION],
            "MAC_VERSION":[DrvItem.SEC_NORMAL, DrvItem.ITEM_WIN_VERSION],
            "AUTORUN_STYLE":[DrvItem.SEC_NORMAL, DrvItem.ITEM_AUTORUN_STYLE],
            "CDROM_ID":[DrvItem.SEC_FW_INFO, DrvItem.ITEM_CDROMID],
            "DISKVID":[DrvItem.SEC_FW_INFO, DrvItem.ITEM_DISKVID],
            "DISKPID":[DrvItem.SEC_FW_INFO, DrvItem.ITEM_DISKPID],
            "UNINSTALL_DESKTOP_ICON":[DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_DESKTOP_ICON],
            "UNINSTALL_GROUP_ICON":[DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_GROUP_ICON],
            "UNINSTALL_MODEMLISTENER":[DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_MODEMLISTENER],
            "UNINSTALL_HOMEURL":[DrvItem.SEC_REMOVE_INFO, DrvItem.ITEM_RM_OPEN_URL]}

    for name, ini_item in config_items.iteritems():
        cell = wb.get_named_cell(name)
        if cell is None:
            logger.error("Can not get value for cell '%s'" % name)
            continue
        ini_item.append(cell.value)
        config.set(*ini_item)

    switch_item =[
    [["DESKTOPICON_FLAG", DrvItem.SEC_NORMAL, DrvItem.ITEM_DESKTOP_ICON_CUST],
    ["DESKTOPICON_PATH", DrvItem.SEC_NORMAL, DrvItem.ITEM_DESKTOP_ICON_PATH]
    ],[["CDROMICON_FLAG", DrvItem.SEC_NORMAL, DrvItem.ITEM_CDROM_ICON],
    ["CDROMICON_PATH", DrvItem.SEC_NORMAL, DrvItem.ITEM_CDROM_ICON_PATH]
    ],[["WIZARD_IMAGE", DrvItem.SEC_NORMAL, DrvItem.ITEM_WIZARD_IMAGE],
    ["WIZARD_IMAGE_PATH", DrvItem.SEC_NORMAL, DrvItem.ITEM_WIZARD_IMAGE_PATH]
    ],[["WIZARD_SMALL_IMAGE", DrvItem.SEC_NORMAL, DrvItem.ITEM_WIZARD_SMALL_IMAGE],
    ["WIZARD_SMALL_IMAGE_PATH", DrvItem.SEC_NORMAL, DrvItem.ITEM_WIZARD_SMALL_IMAGE_PATH]
    ]]

    for flag_item, value_item in switch_item:
        flag_cell = wb.get_named_cell(flag_item[0])
        value_cell= wb.get_named_cell(value_item[0])
        if flag_cell is None or value_cell is None:
            logger.error("Can not get value for cell '%s' or '%s'",
                    flag_item[0], value_item[0])
            continue
        if flag_cell.value.lower() == 'yes':
            config.set(value_item[1], value_item[2], value_cell.value)
        else:
            config.set(value_item[1], value_item[2], '')
        config.set(flag_item[1], flag_item[2], flag_cell.value)


    #for compatible, set default language first in the languages list
    cell = wb.get_named_cell("LANGUAGES")
    if cell is None:
        logger.error("Can not get languages list")
    else:
        #languages = cell.value.split(" ")
        langs = re.split('\s+', cell.value)
        plang = config.get(DrvItem.SEC_NORMAL, DrvItem.ITEM_DEFAULT_LANG)
        if plang is not None:
            langs.sort()
            langs.remove(plang)
            langs.insert(0, plang)
            print "default language", plang
            print "support language", langs #sorted(langs)
            config.set(DrvItem.SEC_NORMAL, DrvItem.ITEM_LANGS, " ".join(langs))
        else:
            logger.error("Default language is not set")

    #wb = open_workbook(input_excel)
    #for s in wb.sheets():
    #    for r in range(2,s.nrows):
    #        for c in range(1, s.ncols):
    #            data = s.cell(r, c)
    #            logger.info( data.value)
    #            if data.value is None:
    #                print "data is empty"
    #                continue
    #            logger.info(data)

debug_mode = False
verbose_mode = False

def log_init(tag, debug=True, logname = datetime.now().strftime('log/%m-%d.log')):
    if not os.path.exists(os.path.dirname(logname)):
        os.mkdir(os.path.dirname(logname), 0777)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=logname,
                        filemode='a')  # #'w'
    logger = logging.getLogger(tag)
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if debug else logging.INFO)
    console.setFormatter(logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s'))
    logger.addHandler(console)
    return logger

class RequirementOption():
    def __init__(self, useage, desc, epilog="=" *78 + "\n"):
        self.cmd_actions = set([])
        self.begin = time.clock()
        self.parser = OptionParser(usage=u"\n\tpython %prog <action> [opts] [args]\n" + useage,
                description=desc, epilog=epilog)
        self.options(self.parser)

    def add_action(self, action):
        if isinstance(action, list):
            for a in action:
                self.cmd_actions.add(a)
        else:
            self.cmd_actions.add(action)

    def handle(self, tag):
        global debug_mode, verbose_mode
        self.parser.epilog = "actions: \r\n" +  ", ".join(self.cmd_actions) + "\n" + self.parser.epilog
        (opts, args) = self.parser.parse_args()
        debug_mode = opts.debug
        verbose_mode = opts.verbose
        logger = log_init(tag, opts.verbose)
        #logger.info("Options is {0}".format(opts))

        if len(args) < 1:
            action = None
        else:
            action = args[0]
            del args[0]

        if action is not None:
            candidate = get_close_matches(action, self.cmd_actions)
            if action not in candidate:
                if len(candidate) == 1:
                    logger.info("Correct action '%s' to '%s'." % (action, candidate[0]))
                    action = candidate[0]
                else:
                    logger.error("invalid action '%s'." % action)

        self.on_handle(action, opts, args, logger)
        logger.info("Elapsed: {0}".format(timedelta(seconds=time.clock() - self.begin)))

    def options(self, parser):
        #parser.add_option("-d", "--debug", action="store_const", const=1, help=u"debug")
        parser.add_option("-d", "--debug", action="store_false", default=True, help=u"debug")
        parser.add_option("-v", "--verbose", action="store_true", default=False, help=u"verbose")
        #parser.add_option("-n", "--num", action="store", default=5, type="int", dest="number")

        '''
        group = OptionGroup(parser, "Report Options",
            "Caution: these options just for report-* actions."
            " From 'report-help' give more information.")
        group.add_option("-a", action="store",
                help=u"属性，默认为None，"
                u"选项，以交互方式输入",
                choices = ["12", "34"], dest="attr", default=None)
        parser.add_option_group(group)
        '''

        group = OptionGroup(parser, "Basic Options")#, "Common Options.")
        group.add_option("-o", "--output", action="store", type="string",
                 help=u"输出的文件或路径")
        group.add_option("-i", "--input", action="store", type="string",
                metavar=u"\"Y900 VimpelCom Requirements.xls\"",
                help=u"输入的需求文档")
        parser.add_option_group(group)

        self.add_action(["convert", "check", "addproject", "profile"])

    def on_handle(self, action, opts, args, logger):
        if opts.input is None:
            if len(args) >= 1:
                opts.input = args[0]
                del args[0]
            else:
                self.parser.print_usage()
                return
        if len(args) >= 1:
            opts.output = args[0]
            del args[0]
        if action == "check":
            require_check(require, logger)
        elif action == "convert":
            require_convert(opts.input, opts.output, logger)
        elif action == "profile":
            generate_profile_files(opts.input, opts.output, logger)
        #action.startswith("focus-"):

if __name__ == '__main__':
    req = RequirementOption(u'''
 从需求表格生产配置文件, 可以执行下面任一命令：
\tpython %prog convert -i "Y900 VimpelCom Requirements.xls" -o Config_Cust_utf8.ini
\tpython %prog convert "Y900 VimpelCom Requirements.xls"  Config_Cust_utf8.ini
 检查SPM需求表格，可以执行下面命令:
\tpython %prog check -i "Y900 VimpelCom Requirements.xls"
\tpython %prog check "Y900 VimpelCom Requirements.xls"
从Excel表格中Profile表中生成profile文件，文件放在match目录
\tpython %prog profile "Y900 VimpelCom Requirements.xls" match
''',
        u"需求文档处理程序")

    req.handle("RequireConverter")
