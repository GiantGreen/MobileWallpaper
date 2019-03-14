#图片裁剪脚本,将下载的高清壁纸解析成预览可预览的图片
# -*- coding: utf-8 -*-

import os
import imghdr
from PIL import Image


class image_aspect():

    def __init__(self, image_file, aspect_width, aspect_height):
        self.img = Image.open(image_file)
        self.aspect_width = aspect_width
        self.aspect_height = aspect_height
        self.result_image = None

    def change_aspect_rate(self):
        img_width = self.img.size[0]
        img_height = self.img.size[1]

        # if (img_width / img_height) > (self.aspect_width / self.aspect_height):
        #     rate = self.aspect_width / img_width
        # else:
        #     rate = self.aspect_height / img_height
        rate_width = self.aspect_width / img_width
        rate_height = self.aspect_height / img_height

        # rate = round(rate, 1)
        # print(rate)
        self.img = self.img.resize((int(img_width * rate_width), int(img_height * rate_height)))
        return self

    def past_background(self):
        self.result_image = Image.new("RGB", [self.aspect_width, self.aspect_height], (0, 0, 0, 255))
        self.result_image.paste(self.img, (
        int((self.aspect_width - self.img.size[0]) / 2), int((self.aspect_height - self.img.size[1]) / 2)))
        return self

    def save_result(self, file_name):
        self.result_image.save(file_name)

class file_scan():

    def __init__(self,basedir,outputdir):
        self.basedir = basedir
        self.outputdir = outputdir

    def is_jpg(self,filename):
        try:
            i = Image.open(filename)
            print(dir(i.format()))
            return True
        except IOError:
            return False

    def cut_all(self):
        result = []  # 所有的文件
        cutresult = [] #裁剪后的文件名
        for maindir, subdir, file_name_list in os.walk(self.basedir):
            for filename in file_name_list:
                apath = os.path.join(maindir, filename)  # 合并成一个完整路径
                temp_name = apath.split('/')[-1]
                newfile_name = self.outputdir+"/"+(temp_name.split('.')[0]+'_260_534.'+temp_name.split('.')[1])
                #判断剪切环境是否存在
                if os.path.exists(newfile_name):
                    print("文件:{0}已存在,不需要再次剪切".format(newfile_name))
                else:
                    try:
                        image_aspect(apath,260,534).change_aspect_rate().past_background().save_result(newfile_name)
                        print("文件:{0},裁剪完毕".format(apath))
                    except Exception as e:
                        print(e.args)

        return result,cutresult


if __name__ == "__main__":
    # image_aspect("./download/1-13997.jpg", 534, 260).change_aspect_rate().past_background().save_result(
    #     "./test.jpg")
    f1 = file_scan("/home/leimin/projects/myproject/MobileWallPaper/website/app/static/download","/home/leimin/projects/myproject/MobileWallPaper/website/app/static/previewimg")
    # print(f1.get_all())
    f1.cut_all()