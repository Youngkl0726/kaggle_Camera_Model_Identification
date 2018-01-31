import numpy as np
import csv

txt_file = open('result.txt', 'wb')
npy_name = 'prob_1.npy'
print npy_name
npy = np.load(npy_name)
# print npy[0],npy[1]
# print np.where(npy[0] == np.max(npy[0]))[0][0]
len = npy.shape[0]
print len
for j in xrange(len):
    res = int(np.where(npy[j] == np.max(npy[j]))[0][0])
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

str_name = ['Motorola-X', 'Motorola-Nexus-6', 'Samsung-Galaxy-S4', 'Samsung-Galaxy-Note3', 'LG-Nexus-5x',\
            'iPhone-4s', 'Motorola-Droid-Maxx', 'HTC-1-M7', 'Sony-NEX-7', 'iPhone-6']
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
