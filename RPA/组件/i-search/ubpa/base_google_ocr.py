# -*- coding:utf-8 -*-
'''
Created on 2018-2-3

@author: Wu.Xin
使用 google 的  Tesseract
'''


from PIL import Image
import pytesseract

#设置tesseract的路径
#pytesseract.pytesseract= "" 

image = Image.open('C:/Users/ibm/Desktop/test.png')
code = pytesseract.image_to_string(image) 