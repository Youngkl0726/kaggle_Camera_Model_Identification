file = open("TrainAug2.txt")
cnt = [[] for i in range(10)]
for i in xrange(10):
    cnt[i] = 0
for i in xrange(68103):
    line = file.readline()
    line = line.strip()
    line = line.split(" ")
    id = int(line[1])
    cnt[id] += 1

for i in xrange(10):
    print i, cnt[i]

