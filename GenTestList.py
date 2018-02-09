
ori_file = open("test0.txt")
ori_lines = ori_file.readlines()
length = len(ori_lines)
print length
for i in xrange(53):
    test_list = './TestList/testL{}.txt'.format(i)
    print test_list
    test_file = open(test_list, 'wb')
    if i==52:
        print ori_lines[i*50]
        for j in xrange(40):
            test_file.write(ori_lines[i*50+j])
        break
    for j in xrange(50):
        test_file.write(ori_lines[i*50+j])
