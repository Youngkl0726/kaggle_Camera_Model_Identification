from skimage import data, exposure, img_as_float
import cv2
from PIL import Image

def get_pic(filename):
    pic_str = [[] for i in range(440)]
    file = open(filename)
    for i in xrange(440):
        line = file.readline()
        line = line.strip()
        # print line
        li = line.split(" ")
        # print li
        pic_str[i].append(li[0])
        pic_str[i].append(li[1])
    return pic_str

def gamma_corr(pic, para):
    point_id = pic.index('.')
    # print pic[0:point_id]
    if para == 0.8:
        gamma_name = 'gamma08'
    else:
        gamma_name = 'gamma12'
    new_pic = pic[0:point_id] + '_' + gamma_name + '.jpg'
    img = cv2.imread('./train'+pic)
    # print img.shape
    gamma_img = exposure.adjust_gamma(img, gamma=para)
    cv2.imwrite('./train_aug'+new_pic, gamma_img)
    return new_pic

def compression(pic, para):
    point_id = pic.index('.')
    # print pic[0:point_id]
    if para == 70:
        comp_name = 'comp70'
    else:
        comp_name = 'comp90'
    new_pic = pic[0:point_id] + '_' + comp_name + '.jpg'
    img = Image.open('./train'+pic)
    img.save('./train_aug'+new_pic, "JPEG", quality=para)
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
    img = Image.open('./train' + pic)
    # print img.size
    width, height = img.size
    # print width*para, height * para
    new_width = int(width * para)
    new_height = int(height * para)
    res_img = img.resize((new_width, new_height), Image.BICUBIC)
    res_img.save('./train_aug'+new_pic)
    return new_pic

def main():
    pic_str = get_pic('train.txt')
    aug_file = open('train_aug.txt', 'wb')
    # print pic_str
    for i in xrange(1):
        pic = pic_str[i][0]
        gt = pic_str[i][1]
        aug_file.write(pic + ' ' + gt + '\n')
        gamma_pic = gamma_corr(pic, 0.8)
        aug_file.write(gamma_pic+' '+gt+'\n')
        gamma_pic = gamma_corr(pic, 1.2)
        aug_file.write(gamma_pic+' '+gt+'\n')
        comp_pic = compression(pic, 70)
        aug_file.write(comp_pic+' '+gt+'\n')
        comp_pic = compression(pic, 90)
        aug_file.write(comp_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 0.5)
        aug_file.write(res_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 0.8)
        aug_file.write(res_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 1.5)
        aug_file.write(res_pic + ' ' + gt + '\n')
        res_pic = resize(pic, 2.0)
        aug_file.write(res_pic + ' ' + gt + '\n')
    aug_file.close()


if __name__ == '__main__':
    main()
