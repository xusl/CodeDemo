#!/usr/bin/env python
# coding=utf-8
from iss import ISSParser, CONTENTBLOCK
parser = ISSParser()
fp = parser.read("Update.iss")
files = parser.getFiles()
out = files.replace('Source', 'Origin')
parser.setSetupOption('AppSupportURL', 'www.alcatel-onetouch.com')
parser.setSetupOption('AppPublisher', "JRD Shenzhen")
parser.setFiles(out)
parser.writefile("test1.iss")

fp = parser.read("Update.iss")
print parser.get('Setup', 'DefaultDirName')
parser.set('Setup', 'AppSupportURL', 'www.alcatel.com')
print parser.get('Dirs', CONTENTBLOCK)
files = parser.get('Files', CONTENTBLOCK)
print files
out = files.replace('Source', 'From')
parser.set('Files', CONTENTBLOCK, out)
print parser.get('Languages', CONTENTBLOCK)
print parser.get('Registry', CONTENTBLOCK)
print parser.get('Tasks', CONTENTBLOCK)
print parser.get('Run', CONTENTBLOCK)
print parser.get('UninstallRun', CONTENTBLOCK)
#print parser.get('InstallDelete', CONTENTBLOCK)
print parser.get('UninstallDelete', CONTENTBLOCK)
print parser.get('Icons', CONTENTBLOCK)
print parser.get('Code', CONTENTBLOCK)

with open("test.iss", 'w') as fp:
    parser.write(fp)

