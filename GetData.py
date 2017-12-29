#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import numpy as np
allFileNum = 0
str_name = ['HTC-1-M7', 'LG5x']
name_id = 0
train_file = open('train.txt', 'wb')
val_file = open('val.txt', 'wb')

def printPath(level, path):
    global allFileNum
    global name_id
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
        if fl == '.DS_Store':
            print "hehe"
            continue
        # print '-' * (int(dirList[0])), path, fl
        point_id = fl.index('.')
        start_id = len(str_name[name_id]) + 2 - 1
        pic_id = int(fl[start_id+1:point_id])
        # print pic_id
        flag = False
        for j in xrange(55):
            if pic_id == arr[j]:
                val_num += 1
                val_file.write(path + '/' + fl + ' ' + str(name_id) + '\n')
                flag = True

        if flag == False:
            train_file.write(path + '/' + fl + ' ' + str(name_id) + '\n')
        # 随便计算一下有多少个文件
        allFileNum = allFileNum + 1
    print "val_num is: ", val_num
    name_id += 1


if __name__ == '__main__':
    printPath(1, './train')
    print '总文件数 =', allFileNum