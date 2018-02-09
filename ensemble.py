import numpy as np
import csv

# average
# npy = np.zeros((2640, 10), dtype='float32')
npy = []

weight = np.array([0.08274889,0.05304561,0.1398555,0.09125838,0.07600546,0.17150401,0.14777716,0.082215381,0.07388858,0.08170103], dtype='float32')
# weight = np.array([0.1071951, 0.16721977, 0.06342457, 0.09719957, 0.11670578, 0.05172051, 0.06002467, 0.1078907, 0.12004935, 0.10856993], dtype='float32')
for i in xrange(4):
    npy_name = './ensemble/prob{:0}.npy'.format(i)
    npy.append(np.load(npy_name))
npy_add = npy[0]+npy[1]+npy[2]+npy[3]
for i in xrange(2640):
    for j in xrange(10):
        npy_add[i][j]=npy_add[i][j]*weight[j]
txt_file = open('result.txt', 'wb')
for i in xrange(2640):
    res = int(np.where(npy_add[i] == np.max(npy_add[i]))[0][0])
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
print("over")