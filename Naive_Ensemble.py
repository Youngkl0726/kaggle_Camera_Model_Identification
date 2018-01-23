import numpy as np
import csv

# average
npy = []
a = 1.0
b = 1.0
c = 1.1
for i in xrange(2):
    npy_name = 'prob_{:0}.npy'.format(i)
    npy.append(np.load(npy_name))
npy_add = a*npy[0] + b*npy[1]
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
print a, " and ", b, " average Ensemble over!"

# # max

# npy = []
# for i in xrange(2):
#     npy_name = 'prob_{:0}.npy'.format(i)
#     npy = np.load(npy_name)
#     txt_file = open('result_{:0}.txt'.format(i), 'wb')
#     for j in xrange(2640):
#         # print npy[j]
#         max_prob = npy[j].max()
#         # print max_prob
#         res = int(np.where(npy[j] == np.max(npy[j]))[0][0])
#         txt_file.write(str(max_prob)+' '+str(res)+'\n')
#     txt_file.close()
#
#
# def get_name(filename):
#     file = open(filename)
#     res_line = []
#     for i in xrange(2640):
#         line = file.readline()
#         line = line.strip()
#         line = line.split(" ")
#         res_line.append(line[0])
#     return res_line
#
# csvfile = open("result.csv", "w")
# fileheader = ["fname", "camera"]
# writer = csv.writer(csvfile)
# writer.writerow(fileheader)
#
# str_name = ['Motorola-X', 'Motorola-Nexus-6', 'Samsung-Galaxy-S4', 'Samsung-Galaxy-Note3', 'LG-Nexus-5x',\
#             'iPhone-4s', 'Motorola-Droid-Maxx', 'HTC-1-M7', 'Sony-NEX-7', 'iPhone-6']
# fname = get_name("test0.txt")
# res_file_1 = open('result_0.txt')
# res_file_2 = open('result_1.txt')
# for i in xrange(2640):
#     context = []
#     line1 = res_file_1.readline()
#     line1 = line1.strip()
#     line1 = line1.split(" ")
#     line2 = res_file_2.readline()
#     line2 = line2.strip()
#     line2 = line2.split(" ")
#
#     prob = []
#     prob.append(float(line1[0]))
#     # print type(line2[0])
#     prob.append(float(line2[0]))
#
#     id = []
#     id.append(line1[1])
#     id.append(line2[1])
#     # print prob, id
#     # print prob.index(max(prob))
#     # print id[prob.index(max(prob))]
#     ans_id = int(id[prob.index(max(prob))])
#
#     context.append(fname[i])
#     context.append(str_name[ans_id])
#     writer.writerow(context)
# csvfile.close()
# print "over"
