#!/usr/bin/env python
# coding=utf-8
'''
Author        : zhenghaoming
Date          : 2022-11-01 01:42:18
FilePath      : \script\maFile_replace_content.py
version       : 
LastEditors   : zhenghaoming
LastEditTime  : 2022-11-01 09:06:56
'''

import os,json,sys,io

def readJson(path=None):
    '''
    @读取json文件
    '''
    if not path:
        return
    with open(path,'r') as f:
        data = json.load(f)
    return data

def content(json_file_path):
    json_file = readJson(json_file_path)

    contents = ''
    renderer = json_file.get("Arnold")
    if renderer is not None:
        contents += "createNode {0} -s -n \"{1}\";\r\n".format(renderer[0],renderer[1])
        # createNode aiOptions -s -n "defaultArnoldRenderOptions";
        samples = json_file.get("Sample")
        if samples is not None:
            for s in samples:
                contents += "setAttr \"{0}.{1}\" {2};\r\n".format(renderer[1],s[0],s[1])
        aovs = json_file.get("Aovs")
        if aovs is not None:
            contents += "setAttr \"{0}.{1}\" {2};\r\n".format(renderer[1],aovs[0],aovs[1])

    else:
        renderer = json_file.get("Redshift")
        if renderer is not None:
            contents += "createNode {0} -s -n \"{1}\";\r\n".format(renderer[0],renderer[1])
            UnifiedSample = json_file.get("UnifiedSample")
            if UnifiedSample is not None:
                for s in UnifiedSample:
                    contents +="setAttr \"{0}.{1}\" {2};\r\n".format(renderer[1],s[0],s[1])

            SampleOverride = json_file.get("SampleOverride")
            if SampleOverride is not None:
                for s in SampleOverride:
                    contents +="setAttr \"{0}.{1}\" {2};\r\n".format(renderer[1],s[0],s[1])

            aovs = json_file.get("Aovs")
            print (s[1])
            if aovs is not None:
                contents +="setAttr \"{0}.{1}\" {2};\r\n".format(renderer[1],aovs[0],aovs[1])            


    wh_size = json_file.get("size")
    wh_node = " :defaultResolution"
    if wh_size is not None:
        for wh in wh_size:
            contents += "setAttr \"{0}.{1}\" {2};\r\n".format(wh_node,wh[0],wh[1])

    return contents

