file = open("TrainAug2.txt")
motox_file = open("motoxFile.txt", "wb")
motoN6_file = open("motoN6_file.txt", "wb")
galaxy_S4_file = open("galaxy_S4_file.txt", "wb")
galaxy_N3_file = open("galaxy_N3_file.txt", "wb")
LG5x_file = open("LG5x_file.txt", "wb")
iphone4s_file = open("iphone4s_file.txt", "wb")
MDMaxx_file = open("MDMaxx_file.txt", "wb")
HTC1M7_file = open("HTC1M7_file.txt", "wb")
SonyN7_file = open("SonyN7_file.txt", "wb")
iphone6_file = open("iphone6_file.txt", "wb")
str_name = ['Motorola-X', 'Motorola-Nexus-6', 'Samsung-Galaxy-S4', 'Samsung-Galaxy-Note3', 'LG-Nexus-5x',\
            'iPhone-4s', 'Motorola-Droid-Maxx', 'HTC-1-M7', 'Sony-NEX-7', 'iPhone-6']
cnt = [[] for i in range(10)]
for i in xrange(10):
    cnt[i] = 0
file_lines = file.readlines()
len = len(file_lines)
print len
for i in xrange(len):
    line = file_lines[i]
    line = line.strip()
    line = line.split(" ")
    id = int(line[1])
    cnt[id] += 1
    if id == 0 and cnt[id] < 6994:
        motox_file.write(file_lines[i])
    if id == 1 and cnt[id] < 6994:
        motoN6_file.write(file_lines[i])
    if id == 2 and cnt[id] < 6994:
        galaxy_S4_file.write(file_lines[i])
    if id == 3 and cnt[id] < 6994:
        galaxy_N3_file.write(file_lines[i])
    if id == 4 and cnt[id] < 6994:
        LG5x_file.write(file_lines[i])
    if id == 5 and cnt[id] < 6994:
        iphone4s_file.write(file_lines[i])
    if id == 6 and cnt[id] < 6994:
        MDMaxx_file.write(file_lines[i])
    if id == 7 and cnt[id] < 6994:
        HTC1M7_file.write(file_lines[i])
    if id == 8 and cnt[id] < 6994:
        SonyN7_file.write(file_lines[i])
    if id == 9 and cnt[id] < 6994:
        iphone6_file.write(file_lines[i])


for i in xrange(10):
    print i, cnt[i]

