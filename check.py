import numpy as np

file_list = ['resnet50_aug2-2_190000', 'resnet101_aug2-2_208000', 'se_aug2-1_200000',\
             'inceptionResnetV2_aug2-1_200000', 'SE-aug2-2_194000', 'inceptionResnetV2_aug2-2_2_170000',\
             'resnet101_aug2-2_2_194000']

for j in xrange(7):
    print file_list[j]
    ori_file_path = "/Users/youngkl/Desktop/{}/train_prob/".format(file_list[j])
    # ori_file_path = "/Users/youngkl/Desktop/{}/train_prob/".format(file_list[j])
    val = []
    for i in xrange(150):
        file = "prob_train_{}.npy".format(i)
        # print file
        npy_file = np.load(ori_file_path + file)
        # print npy_file.shape
        if (len(val) > 0):
            val = np.concatenate((val, npy_file), axis=0)
        else:
            val = npy_file
            # print val.shape
    # gt_file = open("/Users/youngkl/Desktop/kaggle_Camera_Model_Identification/val_aug.txt")
    gt_file = open("/Users/youngkl/Desktop/kaggle_Camera_Model_Identification/TrainAug2_2.txt")
    gt_lines = gt_file.readlines()
    # print len(gt_lines)
    length = len(gt_lines)
    gt = []
    wrong_cnt = []
    for i in xrange(10):
        wrong_cnt.append(0)
    # print wrong_cnt
    for i in xrange(length):
        line = gt_lines[i]
        line = line.strip()
        line = line.split(" ")
        gt.append(int(line[1]))
    num = 0
    for i in xrange(length):
        pred = np.argmax(val[i])
        if int(pred) == gt[i]:
            num += 1
        else:
            wrong_cnt[gt[i]] += 1
    print("accuracy is: {}".format((num * 1.0) / (length*1.0)))
    # print("wrong number is: {}".format((length - num)))
    print("wrong cnt is: {}, total wrong number is : {}".format(wrong_cnt, (length - num)))

# training
# wrong cnt is: [9,   20, 5, 11, 25, 2, 0, 10, 14, 12], total wrong number is : 108
# wrong cnt is: [4,   16, 2,  5,  7, 0, 0,  9, 15, 11], total wrong number is : 69
# wrong cnt is: [12,   7, 0,  5,  8, 0, 0,  9,  1,  8], total wrong number is : 50
# wrong cnt is: [16, 285, 2,  8, 17, 4, 8, 14, 34, 12], total wrong number is : 400
# wrong cnt is: [0,   12, 1,  2,  8, 1, 1,  9,  3, 10], total wrong number is : 47
# wrong cnt is: [4,   22, 1, 12, 12, 1, 0, 12, 14,  9], total wrong number is : 87

# val
# wrong cnt is: [0,    0, 1,  4,  1, 0, 0,  0,  0,  0]
# wrong cnt is: [0,    0, 1,  2,  0, 0, 0,  0,  0,  0]
# wrong cnt is: [0,    0, 0,  1,  1, 0, 0,  0,  0,  0]
# wrong cnt is: [0,    7, 1,  5,  1, 0, 0,  0,  0,  0]

# cnt1 = np.array([9,20,5,11,25,2,0,10,14,12],dtype = 'float32')
# cnt2 = np.array([4,16,2,5,7,0,0,9,15,11], dtype = 'float32')
# cnt3 = np.array([12,7,0,5,8,0,0,9,1,8],dtype = 'float32')
# cnt4 = np.array([16,285,2,8,17,4,8,14,34,12],dtype = 'float32')
#
# # sum = []
# # for i in xrange(10):
# #     sum.append(0)
# # for i in xrange(10):
# #     sum[i] = cnt1[i]+cnt2[i]+cnt3[i]+cnt4[i]
# # print sum
#
#
# cnt =cnt1 + cnt2 + cnt3 +cnt4
# print cnt
# log_cnt = 1.0/np.log(cnt)
# print log_cnt
# k = log_cnt/np.sum(log_cnt)
# print k
