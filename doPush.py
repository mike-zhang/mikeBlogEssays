#! /usr/bin/env python
#-*- coding: utf-8 -*-

import os

def doGitPush():
    bNameAll = os.popen("git branch -l").read()
    #print bNameAll
    bName = ""
    for item in bNameAll.split('\n'):            
        if item[0] == '*' :
            bName = item
            break
    #print bName
    bName = bName.split()[-1]
    print bName
    strCmd = "git push origin %s" % bName
    print strCmd
    os.system(strCmd)

doGitPush()
