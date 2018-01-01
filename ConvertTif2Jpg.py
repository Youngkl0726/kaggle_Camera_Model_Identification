import os
from PIL import Image

num = 0
test_jpg_file = open('test_jpg0.txt', 'wb')
for infile in os.listdir("./test/"):
    print "file : " + infile
    if infile[-3:] == "tif":
       outfile = './test_jpg/' + infile[:-3] + "jpg"
       test_jpg_file.write(infile[:-3] + "jpg" + ' 0' + '\n')
       im = Image.open('./test/'+infile)
       print num, "new filename : " + outfile
       num += 1
       out = im.convert("RGB")
       out.save(outfile, "JPEG", quality=95)
test_jpg_file.close()
