#!/usr/bin/env python
# _*_ coding: utf-8 _*_
#coding= utf-8

import kinterbasdb
import sys, platform
import os
import re
import urllib2
from io import open
from optparse import OptionParser
from datetime import datetime, date, time
from BaseHTMLProcessor import BaseHTMLProcessor
from html_parser import HTMLFormat
from HTMLParser import HTMLParseError

system=platform.system()
print sys.getdefaultencoding()
#exit()
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

class HTMLFormatter(BaseHTMLProcessor):
	def reset(self):
		# extend (called from __init__ in ancestor)
		# Reset all data attributes
		self.verbatim = 0
		BaseHTMLProcessor.reset(self)

	def start_pre(self, attrs):
		# called for every <pre> tag in HTML source
		# Increment verbatim mode count, then handle tag like normal
		self.verbatim += 1
		self.unknown_starttag("pre", attrs)

	def end_pre(self):
		# called for every </pre> tag in HTML source
		# Decrement verbatim mode count
		self.unknown_endtag("pre")
		self.verbatim -= 1

	def handle_data(self, text):
		# override
		# called for every block of text in HTML source
		# If in verbatim mode, save text unaltered;
		# otherwise process the text with a series of substitutions
		self.pieces.append(self.verbatim and text or self.process(text))

	def unknown_starttag(self, tag, attrs):
		print "unknow_startag"

	def process(self, text):
		# called from handle_data
		# Process text block by performing series of regular expression
		# substitutions (actual substitions are defined in descendant)
		#for fromPattern, toPattern in self.subs:
		#	text = re.sub(fromPattern, toPattern, text)
		return text

def translate(content, outfile):
    formattor = BaseHTMLProcessor()
    formattor.feed(content)
    formattor.close()

    #outfile = "htmlformat/%s.html" % name
    file = None
    try:
        file = open(outfile, "wb")
        file.write(formattor.output())
    finally:
        if file != None:
            file.close()

def htmlformatter(source, outfile, dump):
    html = HTMLFormat()
    content = None
    try :
        html.feed(source)
        content = html.outHTML("utf-8")
    except TypeError as error:
        print outfile, error
        return None
    except HTMLParseError as (e):
        print e , outfile
        return None

    if not dump:
        return content

    if not os.path.exists(os.path.dirname(outfile)):
        os.mkdir(os.path.dirname(outfile), 0644)

    with open(outfile,'tw', 1, "utf-8") as f:
        try:
            f.write(content)
        except TypeError as error:
            print outfile, error
            return None

    return content

def origindata(data, outfile, dump):
    if not dump:
        return
    if not os.path.exists(os.path.dirname(outfile)):
        os.mkdir(os.path.dirname(outfile), 0644)

    #f = None
    #try:
    #    f=open(outfile,'tw', 1, "utf-8")
    #    f.write(data)
    #finally:
    #    if f != None:
    #        f.close()

    with open(outfile,'tw', 1, "utf-8") as f:
        f.write(data)

def stock_desc(cur, dump = False, delete_plugin = False):
    stock_ids = set([])
    # Execute the SELECT statement:
    cur.execute("select DESCRIPTION,NUM_IID,TITLE,SYNC_STATUS,MODIFIED from ITEM order by NUM_IID")
    for (desc, num, title,sync_status, modified) in cur:
        if num == None:
            continue

        udesc = unicode(desc, "utf-8")#不写utf-8, 系统默认的ascii
        #utitle = unicode(title, "gbk")
        #print type(desc), type(udesc)
        print title, "modified time:{0}, sync status {1}".\
                    format(modified, sync_status)


        #out = udesc.encode("GB2312") # out of encode is str type , not unicode
        origindata(udesc, os.path.join("out","base", str(num)+'.html'), dump)
        udesc = htmlformatter(udesc, "out/convert/" + str(num)+'.html', dump)
       # translate(out, "htmlformat/" + outfile)
        stock_ids.add((num, title, udesc))
    return stock_ids

def stock(con, dump = False, free_fare = False, delete_pulgin = False):
    # Create a Cursor object that operates in the context of Connection con:
    cur = con.cursor()

    #First, fetch all NUMM_IID, Then fetch each record.
    #we can not fetch all record in a time, read and write in a for block .
    #for cursor may be change by write.
    stock_items = stock_desc(cur, dump, delete_pulgin)
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S") #now.strftime("%Y-%m-%d %H:%M:%S")

    for (num, title, desc) in stock_items:
        #if system == "Windows" or system == "Linux":
        # the first title in encode to utf-8, so it error in windows,
        # normally in Linux. And the second title is all ok in both .
        # just like io.write TypeError: must be unicode, not str
        #print "today {0}, title {1}".format(now_str, title)  #not proper in windows
        #print u"today {0}, title {1}".format(now_str, title) #both ok
        #print title  #ok both
        if not re.search(ur"包邮", title):
            #print "not match baoyou", title
            if free_fare == False:
                continue
            title = u"【包邮】" + title
            cur.execute('''update ITEM
                set SYNC_STATUS=?,MODIFIED=?,TITLE=?
                where NUM_IID=?''',
                (1, now_str, title, num))
            con.commit()
        elif free_fare == False:
            #print "remove"
            title = re.sub(ur"(【包邮】)*", "", title)
            cur.execute('''update ITEM
                set SYNC_STATUS={1},MODIFIED='{2}',TITLE='{3}'
                where NUM_IID={0}'''
                .format(num, 1, now_str, title))
            con.commit()

        if delete_pulgin and desc != None:
            cur.execute('''update ITEM
                set SYNC_STATUS=?,MODIFIED=?,DESCRIPTION=?
                where NUM_IID=?''',
                (1, now_str, desc, num))
            con.commit()
    return

def picture(con):
    cur = con.cursor()
    cur.execute("select NUM_IID,ID,URL,CLIENT_ID,CLIENT_ITEMID from PICTURE order by ID")
    script_path = os.path.dirname(sys.argv[0])
    dest_dir = os.path.join(script_path, "out")
    if not os.path.exists(dest_dir):
		os.mkdir(dest_dir, 0644)
    for (num_iid, pid,url,cid,citemid) in cur:
        f=urllib2.urlopen(url) #print num_iid, pid,url,cid,citemid
        with open(os.path.join(dest_dir, cid+".jpg"), "wb") as code:
            code.write(f.read())
    cur.close()

def category(con):
    cur = con.cursor()
    cur.execute("select CID,NAME from CATEGORY order by CID")
    for (cid, name) in cur:
        print cid, name
    cur.close()

def trade(con):
    # Create a Cursor object that operates in the context of Connection con:
    cur = con.cursor()
    cur.execute("select RECEIVER_NAME,BUYER_MESSAGE from TRADE")
    print "trade"
    for (receiver, buyer_note) in cur:
        print receiver, buyer_note
    cur.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--title-free-fare", dest="fare_free",
            action="store_true", default=False, help=u"标题加上包邮")
    parser.add_option("-o", "--output-file",
                  action="store", type="string", dest="filename")

    parser.add_option("-s", "--delete-pulgin", dest="delete_pulgin",
            action="store_true", default=False, help=u"删除贝贝旺推介")
    parser.add_option("-d", "--dump-description-goods", dest="dump_desc",
            action="store_true", default=False, help=u"输入宝贝的描述")

    (options, args) = parser.parse_args()
    database = "localhost:/home/zen/work/ai-droid/Taobao/demo/taobao/APPITEM.DAT"
    #dsn='E:\\taobao\\APPITEM.DAT',
    con = kinterbasdb.connect(
        dsn=database,
        user='sysdba', password='masterkey',
        #dialect=1, # necessary for all dialect 1 databases
        #charset='UTF8' # specify a character set for the connection
      )
    category(con)
    #picture(con)
    #trade(con)
    #stock(con, options.dump_desc,options.fare_free, options.delete_pulgin)
