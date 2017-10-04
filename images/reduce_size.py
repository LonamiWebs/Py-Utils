#!/bin/env python2
# Written by https://github.com/Nitish18

import PIL
import Image


width_pixels = 1000  # new width
img_path = raw_input('Enter the image path: ')
img = Image.open(str(img_path))
widthper = (width_pixels / float(img.size[0]))
height_pixels = int((float(img.size[1]) * float(widthper)))
img = img.resize((width_pixels, height_pixels), PIL.Image.ANTIALIAS)

list1 = img_path.split("/")
img_name = list1.pop()
list2 = img_name.split(".")
img_extension = list2.pop()
q = img_path.replace(img_name, "")
final_img = q + 'compressed_image.' + img_extension

img.save(final_img)
