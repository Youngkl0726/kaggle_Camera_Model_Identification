file = open("train_aug.txt")
txt = open("TrainAug.txt", "wb")
for i in xrange(19800):
    line = file.readline()
    line = line.strip()
    line = line.split(" ")
    modified = "/train_aug"+line[0]
    txt.write(modified+" "+line[1]+'\n')
txt.close()
