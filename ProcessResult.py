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
