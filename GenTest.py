#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import numpy as np
allFileNum = 0
test_file = open('test.txt', 'wb')

def printPath(level, path):
    global allFileNum
    ''''' 
    打印一个目录下的所有文件夹和文件 
    '''
    # 所有文件夹，第一个字段是次目录的级别
    dirList = []
    # 所有文件
    fileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    # 先添加目录级别
    dirList.append(str(level))
    for f in files:
        if os.path.isdir(path + '/' + f):
            # 排除隐藏文件夹。因为隐藏文件夹过多
            if f[0] == '.':
                pass
            else:
                # 添加非隐藏文件夹
                dirList.append(f)
        if os.path.isfile(path + '/' + f):
            # 添加文件
            fileList.append(f)
            # 当一个标志使用，文件夹列表第一个级别不打印
    i_dl = 0
    for dl in dirList:
        # print "dl is: ", dirList
        if i_dl == 0:
            i_dl = i_dl + 1
        else:
            # 打印至控制台，不是第一个的目录
            print '-' * (int(dirList[0])), dl
            # 打印目录下的所有文件夹和文件，目录级别+1
            printPath((int(dirList[0]) + 1), path + '/' + dl)
    arr = np.arange(1, 276)
    np.random.shuffle(arr)
    val_num = 0
    val_hash = []
    for fl in fileList:
        # 打印文件
        # print allFileNum, fl
        test_file.write(fl + ' 0' + '\n')
        if fl == '.DS_Store':
            print "hehe"
            continue
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1


if __name__ == '__main__':
    printPath(0, './test')
    print '总文件数 =', allFileNum