#coding:utf-8

##
# author nanzhi<nanzhienai@163.com,http://www.12sui.cn>
# TODO 内联样式/脚本格式化
# TODO Doctype校验
# TODO 未闭合标签检查
# TODO 压缩html
##

from HTMLParser import HTMLParser
import re,os,sys

#设置缩进大小
indent = 4

#获取文件路径
dir = sys.argv

#自闭合标签，不包含注释
selfClosureTag = re.compile(r'(br|input|link|meta|hr|col|img|area|base|hr|embed|param)\b')

#半闭合标签
halfClosureTag = re.compile(r'p|td|li')

#不换行不留空标签
#nowrapTag = re.compile(r'(h1|h2|h3|h4|h5|h6|span|a|s|i|em|b|font|strong|title)\b')
#remove span
nowrapTag = re.compile(r'(h1|h2|h3|h4|h5|h6|a|s|i|em|b|font|strong|title)\b')

#匹配首尾标签
e2bTag = re.compile(r'>(.[^<]*)<')

#匹配所有标签
cpTag = re.compile(r'<.[^>]+>')

#匹配样式或者脚本标签
inlineS = re.compile(r'(style|script)\b')

tableTag = re.compile(r'table\b')

#一对无内容空标签
emptyTag = re.compile(r'(<(\w+)\b.*?>)\s*\n*\r*(<\/\2>)')

#无用行
useless = re.compile(r'\r|\n')

#空行
blankline = re.compile(r'\n\s*\n+')

#新的文件名
newFileName = re.compile(r'\/?(.+?)\.')

#空格
space = ' '

class HTMLFormat(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        #存储字符串
        self.result = []
        #缩进记录
        self.tab = 0
        #是否需要换行
        self.newline = True 
        #是否是内联样式或者脚本
        self.inline = False 
        self.table = False

    #开始标签
    def handle_starttag(self, tag, attrs):
        #style,script内标签
        if self.inline:
            return

        if self.table:
            return

        if tableTag.match(tag):
            if len(attrs) >=1 and \
                attrs[0][0] == "title" and \
                attrs[0][1] == "beibeiwang":
                print attrs
            self.table = True
            return

        #不需要换行的标签处理
        if nowrapTag.match(tag):
            self.newline = False

        #是否换行
        if self.newline:
            self.result.append('\n')
            self.result.append(self.tab * space)

        self.result.append(self.get_starttag_text())

        #非自闭合标签添加缩进，因为类中自闭合标签的判断
        #是根据xhtml来解析的，所以此处还是要加上判断
        if not selfClosureTag.match(tag):
            self.tab += indent

        #内联判断
        if inlineS.match(tag):
            self.inline = True


    #标签内数据处理    
    def handle_data(self, text):
        if self.table:
            return

        if self.newline:
            self.result.append('\n' + self.tab * space)
        self.result.append(text.strip())

    #结束标签
    def handle_endtag(self, tag):
        #内联判断
        if inlineS.match(tag):
            self.inline = False 

        if self.table:
            return

        if tableTag.match(tag):
            #print attrs
            self.table = False
            return

        #非style,script内标签
        if not self.inline: 
            self.tab -= indent 
            if self.newline:
                self.result.append('\n' + self.tab * space)
            elif (not nowrapTag.match(tag)):
                self.newline = True

        self.result.append('</' + tag + '>')

    #自闭合标签，此方法仅解析符合xhtml标准的自闭合标签
    def handle_startendtag(self, tag, attrs):
        if self.table:
            return

        self.result.append(self.get_starttag_text())

    #doctype处理
    def handle_decl(self, tag):
        self.result.append('<!' + tag + '>')

    #注释处理
    def handle_comment(self, comment):
        self.result.append('<!--' + comment + '-->')

    #自定义函数，html处理，输出html
    def outHTML(self, char):
        #转化为字符串
        html = ''.join(self.result)
        #去除空标签中的换行
        html = emptyTag.sub(r'\1\3', html, 0)
        #去除多余行
        html = blankline.sub('\n', html, 0)
        #return html.encode(char)# encode is return to str 
        return html 
