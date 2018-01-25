bt_file = open("BalanceTrain.txt", "wb")
file = open("data.txt")
file_lines = file.readlines()
len = len(file_lines)
cnt = [[] for i in range(10)]
for i in xrange(10):
    cnt[i] = 0
print len
for i in xrange(len):
    line = file_lines[i]
    line = line.strip()
    line = line.split(" ")
    id = int(line[1])
    cnt[id] += 1
    if cnt[id] < 6994:
        bt_file.write(file_lines[i])
