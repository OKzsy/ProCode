#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os
import fnmatch
import glob


def SearchFiles(dirPath, partFileInfo, recursive=False):
    """列出符合要求的文件明（包含路径），当递归为False时不遍历子文件夹，默认不遍历子文件夹"""
    fileList = []
    pathList = glob.glob(os.path.join(os.path.sep, dirPath, '*'))  # windows path
    # print 'pathList = '
    # print pathList
    for mPath in pathList:
        # print mPath
        if fnmatch.fnmatch(mPath, partFileInfo):
            fileList.append(mPath)  # 符合条件条件加到列表
        elif os.path.isdir(mPath):
            if recursive:
                # print mPath
                fileList += SearchFiles(mPath, partFileInfo)  # 将返回的符合文件列表追加到上层
            else:
                pass
        else:
            pass
    return fileList


path = SearchFiles(r'F:\python_test_folder', "*.txt")  # windows path
print(path)
print(os.path.dirname(path[0]))
print(os.path.basename(path[0]))
print(os.path.splitext(os.path.basename(path[0]))[0])
