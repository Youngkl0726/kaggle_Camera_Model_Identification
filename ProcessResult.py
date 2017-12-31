import numpy as np
import csv

txt_file = open('result.txt', 'wb')
npy_name = 'prob_0.npy'
print npy_name
npy = np.load(npy_name)
len = npy.shape[0]
print len
for j in xrange(len):
    res = int(npy[j][0])
    txt_file.write(str(res)+'\n')
txt_file.close()


def get_name(filename):
    file = open(filename)
    res_line = []
    for i in xrange(2640):
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        res_line.append(line[0])
    return res_line

str_name = ['MotoX', 'MotoNex6', 'GalaxyS4', 'GalaxyN3', 'LG5x',\
            'iP4s', 'MotoMax', 'HTC-1-M7', 'Nex7', 'iP6']
csvfile = open("result.csv", "w")
fname = get_name("test0.txt")
fileheader = ["fname", "camera"]
writer = csv.writer(csvfile)
writer.writerow(fileheader)
res_file = open('result.txt')
for i in xrange(2640):
    context = []
    line = res_file.readline()
    line = line.strip()
    line = line.split(" ")
    context.append(fname[i])
    context.append(str_name[int(line[0])])
    writer.writerow(context)
csvfile.close()
