from skimage import data, exposure, img_as_float
import cv2
from PIL import Image
import os
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def get_pic(filename):
    pic_str = [[] for i in range(5376)]
    str_name = ['Motorola-X', 'Motorola-Nexus-6', 'Samsung-Galaxy-S4', 'Samsung-Galaxy-Note3', 'LG-Nexus-5x', \
                'iPhone-4s', 'Motorola-Droid-Maxx', 'HTC-1-M7', 'Sony-NEX-7', 'iPhone-6']
    file = open(filename)
    for i in xrange(5376):
        line = file.readline()
        line = line.strip()
        # print line
        li = line.split("/")
        # print li
        tag = li[1]
        id = 0
        for j in xrange(10):
            if tag == str_name[j]:
                id = j
                break
        pic_str[i].append('/'+li[1]+'/'+li[2])
        pic_str[i].append(str(id))
    return pic_str



def gamma_corr(pic, para):
    point_id = pic.index('.')
    # print pic[0:point_id]
    if para == 0.8:
        gamma_name = 'gamma08'
    else:
        gamma_name = 'gamma12'
    new_pic = pic[0:point_id] + '_' + gamma_name + '.jpg'
    if os.path.exists('./flickr_images'+new_pic) == True:
        print "exists"
        return new_pic
    img = cv2.imread('./flickr_images'+pic)
    # print img.shape
    gamma_img = exposure.adjust_gamma(img, gamma=para)
    cv2.imwrite('./flickr_images'+new_pic, gamma_img)
    return new_pic

def compression(pic, para):
    point_id = pic.index('.')
    # print pic[0:point_id]
    if para == 70:
        comp_name = 'comp70'
    else:
        comp_name = 'comp90'
    new_pic = pic[0:point_id] + '_' + comp_name + '.jpg'
    if os.path.exists('./flickr_images'+new_pic) == True:
        print "exists"
        return new_pic
    img = Image.open('./flickr_images'+pic)
    img.save('./flickr_images'+new_pic, "JPEG", quality=para)
    return new_pic

def resize(pic, para):
    point_id = pic.index('.')
    if para == 0.5:
        res_name = 'res05'
    elif para == 0.8:
        res_name = 'res08'
    elif para == 1.5:
        res_name = 'res15'
    else:
        res_name = 'res20'
    new_pic = pic[0:point_id] + '_' + res_name + '.jpg'
    if os.path.exists('./flickr_images'+new_pic) == True:
        print "exists"
        return new_pic
    img = Image.open('./flickr_images' + pic)
    # print img.size
    width, height = img.size
    # print width*para, height * para
    new_width = int(width * para)
    new_height = int(height * para)
    res_img = img.resize((new_width, new_height), Image.BICUBIC)
    res_img.save('./flickr_images'+new_pic)
    return new_pic

def main():
    pic_str = get_pic('./flickr_images/good_jpgs')
    # print pic_str
    aug_file = open('flickr_aug.txt', 'wb')
    # print pic_str
    num = 0
    for i in xrange(5376):
        pic = pic_str[i][0]
        gt = pic_str[i][1]
        if os.path.exists('./flickr_images'+pic) == False:
            print './flickr_images'+pic+'does not exist'
            continue
        print "num is: ", num, "  file is: ", pic
        aug_file.write('/flickr_images'+pic + ' ' + gt + '\n')
        gamma_pic = gamma_corr(pic, 0.8)
        aug_file.write('/flickr_images'+gamma_pic+' '+gt+'\n')
        gamma_pic = gamma_corr(pic, 1.2)
        aug_file.write('/flickr_images'+gamma_pic+' '+gt+'\n')
        comp_pic = compression(pic, 70)
        aug_file.write('/flickr_images'+comp_pic+' '+gt+'\n')
        comp_pic = compression(pic, 90)
        aug_file.write('/flickr_images'+comp_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 0.5)
        aug_file.write('/flickr_images'+res_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 0.8)
        aug_file.write('/flickr_images'+res_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 1.5)
        aug_file.write('/flickr_images'+res_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 2.0)
        aug_file.write('/flickr_images'+res_pic + ' ' + gt + '\n')
        num += 1
    aug_file.close()


if __name__ == '__main__':
    main()
