import numpy as np
import csv

txt_file = open('result_val.txt', 'wb')
npy_name = 'prob_0.npy'
print npy_name
npy = np.load(npy_name)
# print npy[0]
# print np.where(npy[0] == np.max(npy[0]))[0][0]
len = npy.shape[0]
print len
for j in xrange(len):
    res = int(np.where(npy[j] == np.max(npy[j]))[0][0])
    txt_file.write(str(res)+'\n')
txt_file.close()

def get_id_gt(filename):
    file = open(filename)
    res_line = []
    for i in xrange(4950):
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        res_line.append(line[1])
    return res_line

def get_id_pd(filename):
    file = open(filename)
    res_line = []
    for i in xrange(4950):
        line = file.readline()
        line = line.strip()
        line = line.split(" ")
        res_line.append(line[0])
    return res_line

res_gt = get_id_gt("val_aug.txt")
res_pd = get_id_pd("result_val.txt")
num = 0
cnt = [[] for i in range(10)]
for i in xrange(10):
    cnt[i] = 0
for i in xrange(4950):
    if res_gt[i] != res_pd[i]:
        num += 1
        cnt[int(res_gt[i])] += 1
        print i, res_pd[i], res_gt[i]
print num
print (num*1.0) / 4950.0
print "loss: "
for i in xrange(10):
    print i, cnt[i]