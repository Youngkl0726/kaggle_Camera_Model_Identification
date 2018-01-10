txt_file = open('test_aug0.txt', 'wb')
file = open('test0.txt')
for i in xrange(2640):
# for i in xrange(10):
    line = file.readline()
    print line
    for j in xrange(10):
        txt_file.write(line)
txt_file.close()